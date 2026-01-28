# pdf_ingestor/src/pdf_ingestor/ingest/utils.py

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def safe_attr(obj: object, name: str, default: Any = None) -> Any:
    """Safely retrieve an attribute from an object (Pyright-friendly)."""
    return getattr(obj, name, default)


def compute_doc_id(file_path: str, max_bytes: int = 8 * 1024 * 1024) -> str:
    """
    Compute a stable doc_id from file bytes (capped for very large files).
    Returns a short SHA-256 digest (16 chars).
    """
    p = Path(file_path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        h.update(f.read(max_bytes))
    return h.hexdigest()[:16]


def extract_error(conversion_result: object) -> str:
    # Try likely attribute names
    for name in ("error_message", "error", "message", "reason"):
        val = safe_attr(conversion_result, name, None)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # Some libraries store exceptions/details in nested structures
    details = safe_attr(conversion_result, "details", None)
    if details is not None:
        return str(details)

    # Final fallback
    return "Conversion failed (no error message provided by Docling)."
