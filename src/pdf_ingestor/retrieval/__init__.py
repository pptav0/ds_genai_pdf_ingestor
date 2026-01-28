# pdf_ingestor/src/pdf_ingestor/retrieval/__init__.py

from .embeddings import assert_ollama_model_available, assert_ollama_running

__all__ = ["assert_ollama_running", "assert_ollama_model_available"]
