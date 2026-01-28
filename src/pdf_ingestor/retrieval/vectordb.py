# pdf_ingestor/src/pdf_ingestor/retrieval/vectordb.py

from __future__ import annotations

from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def build_chroma_from_documents(
    documents: list[Document],
    embeddings: Embeddings,
    persist_dir: str | Path,
    collection_name: str = "default",
) -> Chroma:
    """
    Create (or overwrite) a Chroma collection from documents and persist it locally.
    """
    persist_path = Path(persist_dir)
    persist_path.mkdir(parents=True, exist_ok=True)

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(persist_path),
        collection_name=collection_name,
    )
    vectordb.persist()
    return vectordb


def load_chroma(
    embeddings: Embeddings,
    persist_dir: str | Path,
    collection_name: str = "default",
) -> Chroma:
    """
    Load an existing persisted Chroma collection.
    """
    persist_path = Path(persist_dir)
    return Chroma(
        persist_directory=str(persist_path),
        collection_name=collection_name,
        embedding_function=embeddings,
    )
