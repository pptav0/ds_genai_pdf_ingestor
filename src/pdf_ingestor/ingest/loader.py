# pdf_ingestor/src/pdf_ingestor/ingest/loader.py

from __future__ import annotations

import os
from pathlib import Path
from typing import List

from docling.datamodel.base_models import ConversionStatus
from docling.document_converter import DocumentConverter
from tqdm import tqdm

from .converter import build_converter
from .types import LoadedDoc, LoadedDocument
from .utils import compute_doc_id, extract_error, safe_attr


def load_files_from_path(path: str) -> List[LoadedDocument]:
    """
    Load a file or directory of files and convert them using Docling.

    Returns LoadedDocument wrappers to streamline downstream indexing/vectorization.
    """
    converter = build_converter()
    results: List[LoadedDocument] = []

    if os.path.isfile(path):
        results.append(_process_single_file(converter, path))
        return results

    if os.path.isdir(path):
        file_paths: List[str] = []
        for root, _, files in os.walk(path):
            for fname in files:
                if fname.startswith("."):
                    continue
                if not fname.lower().endswith(".pdf"):
                    continue

                file_paths.append(os.path.join(root, fname))

        for file_path in tqdm(file_paths, desc="Processing files", unit="file"):
            results.append(_process_single_file(converter, file_path))

        return results

    raise ValueError(
        f"The provided path '{path}' is neither a file nor a directory."
    )


def load_docs_as_records(path: str) -> List[LoadedDoc]:
    """Return serializable dict records (useful for saving ingestion outputs)."""
    docs = load_files_from_path(path)
    return [
        {
            "content": d.content,
            "metadata": d.metadata,
            "status": d.status,
            "error": d.error,
        }
        for d in docs
    ]


def _process_single_file(
    converter: DocumentConverter, file_path: str
) -> LoadedDocument:
    """
    Convert a single file and return a LoadedDocument wrapper.

    Notes:
    - Docling decides internally whether OCR is needed.
    - We capture `conversion_status` for debugging and optionally accept PARTIAL conversions.
    - We extract a robust error message (Docling sometimes returns non-success without error_message).
    """
    doc_id = compute_doc_id(file_path)
    path_metadata = _extract_path_metadata(file_path)

    metadata = {
        "doc_id": doc_id,
        "source_path": file_path,
        **path_metadata,
        "ocr_performed": None,
        "processing_notes": "OCR may be applied automatically by Docling if required.",
    }

    try:
        # Raises exceptions so failures are not silently swallowed
        result = converter.convert(file_path, raises_on_error=True)

        # Capture raw status for visibility
        status = safe_attr(result, "status", None)
        metadata["conversion_status"] = str(status)

        # Docling’s primary output is usually `result.document`
        doc = safe_attr(result, "document", None)
        if doc is None:
            # fall back to any legacy field if present
            legacy = safe_attr(result, "content", None)
            if legacy is None:
                return LoadedDocument(
                    doc_id=doc_id,
                    source_path=file_path,
                    content=None,
                    status="failed",
                    error="Conversion returned no document object.",
                    metadata=metadata,
                )
            return LoadedDocument(
                doc_id=doc_id,
                source_path=file_path,
                content=legacy,
                status="success",
                error=None,
                metadata=metadata,
            )

        # Export to markdown (matches docling docs)
        markdown = doc.export_to_markdown()
        if not isinstance(markdown, str) or not markdown.strip():
            return LoadedDocument(
                doc_id=doc_id,
                source_path=file_path,
                content=None,
                status="failed",
                error="Document export produced empty markdown.",
                metadata=metadata,
            )

        return LoadedDocument(
            doc_id=doc_id,
            source_path=file_path,
            content=markdown,
            status="success",
            error=None,
            metadata=metadata,
        )

    except Exception as e:
        # Fail per-file, not per-batch
        metadata["conversion_status"] = "EXCEPTION"
        return LoadedDocument(
            doc_id=doc_id,
            source_path=file_path,
            content=None,
            status="failed",
            error=str(e),
            metadata=metadata,
        )


def _extract_path_metadata(file_path: str) -> dict:
    p = Path(file_path).resolve()
    parts = p.parts

    metadata = {}

    for part in parts:
        if part.isdigit() and len(part) == 4:
            metadata["year"] = int(part)

    return metadata
