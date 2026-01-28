# pdf_ingestor/src/pdf_ingestor/ingest/types.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional, TypedDict


class LoadedDoc(TypedDict):
    content: Optional[Any]
    metadata: Dict[str, Any]
    status: str
    error: Optional[str]


@dataclass(frozen=True)
class LoadedDocument:
    doc_id: str
    source_path: str
    content: Optional[Any]
    status: str
    error: Optional[str]
    metadata: Dict[str, Any]

    @property
    def ok(self) -> bool:
        return self.status == "success" and self.content is not None

    def text(self) -> str:
        if not self.ok:
            return ""

        if isinstance(self.content, str):
            return self.content

        candidate = getattr(self.content, "text", None)
        if isinstance(candidate, str):
            return candidate

        return str(self.content)

    def iter_chunks(
        self, chunk_size: int = 1200, overlap: int = 150
    ) -> Iterator[Dict[str, Any]]:
        text = self.text()
        if not text:
            return

        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if overlap < 0:
            raise ValueError("overlap must be >= 0")
        if overlap >= chunk_size:
            raise ValueError("overlap must be < chunk_size")

        n = len(text)
        start = 0
        while start < n:
            end = min(start + chunk_size, n)
            yield {
                "doc_id": self.doc_id,
                "source_path": self.source_path,
                "text": text[start:end],
                "start": start,
                "end": end,
            }
            if end >= n:
                break
            start = end - overlap
