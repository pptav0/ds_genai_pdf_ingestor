# pdf_ingestor/src/pdf_ingestor/ingest/converter.py

from docling.document_converter import DocumentConverter


def build_converter() -> DocumentConverter:
    """
    Build a DocumentConverter instance.

    Note: Docling handles pipeline configuration internally.
    """
    return DocumentConverter()
