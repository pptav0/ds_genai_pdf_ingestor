# PDF Ingestor — Local PDF → Metadata + RAG (Ollama)

## Project Scope

This project is part of a Data Science & AI portfolio and focuses on building a local document-intelligence MVP. The goal is to demonstrate the ability to process PDF documents (including scanned PDFs) into structured metadata and enable Retrieval-Augmented Generation (RAG) for grounded Q&A. The emphasis is on traceability, reproducibility, and offline functionality.

The project is designed for research and portfolio purposes, showcasing skills in operationalizing document pipelines, integrating OCR, and leveraging local LLMs for metadata extraction and Q&A.

## Overview

**PDF Ingestor** is a local document-intelligence MVP that ingests **PDF reports** and transforms them into:

- **Structured metadata (JSON)** with page-level evidence  
- **Retrieval-Augmented Generation (RAG)** for grounded Q&A over the document

The system is designed for **offline / on-prem usage**, using **OCR, vector retrieval, and a local LLM via Ollama**, with an emphasis on traceability and reproducibility rather than black-box extraction.

---

## MVP Scope

The MVP focuses on a reliable, auditable pipeline:

**Ingest → OCR (if needed) → Chunk → Index → Extract Metadata → Ask Questions**

Out of scope (by design):
- Model fine-tuning
- Multi-document reasoning
- Cloud dependencies

---

## MVP Features

### 1. PDF Ingestion
- Accepts local PDF files or file paths
- Automatically detects:
  - **Text-based PDFs**
  - **Scanned PDFs** (image-only)
- Runs OCR only when required

---

### 2. Text Normalisation & Chunking
- Page-aware chunking (no blind token splitting)
- Each chunk retains provenance:
  - page number
  - document ID
- Enables citation-based retrieval and extraction

---

### 3. Local Vector Index
- Builds a local vector index per document
- Supports semantic retrieval for:
  - metadata extraction
  - question answering
- Designed to run fully offline

---

### 4. Metadata Extraction (LLM-assisted)
- Uses Ollama-hosted LLMs to:
  - classify document type (optional)
  - extract metadata into a **strict JSON schema**
- Each metadata field includes:
  - extracted value
  - confidence score
  - page-level evidence snippet  
- Fields without evidence are returned as `null` to prevent hallucination

---

### 5. RAG-Based Question Answering
- Questions are answered **only from retrieved document chunks**
- Responses include page references
- Suitable for validation, review, and exploration workflows

---

## Folder Structure

```raw
pdf_ingestor/
├── data/
│   ├── index/
│   │   └── chroma_wef/          # Persisted Chroma vector database (local)
│   └── WEF/                     # Raw PDF datasets (organized by year/source)
│
├── notebook/
│   └── pdf_ingestor.ipynb       # End-to-end workflow:
│                                # ingestion → chunking → embeddings → RAG
│
├── src/
│   │  
│   └── pdf_ingestor/
│       │
│       ├── __init__.py
│       │
│       ├── helpers/
│       │   ├── __init__.py      # Shared utilities (e.g. environment checks)
│
│       ├── ingest/
│       │   ├── __init__.py
│       │   ├── converter.py     # Docling DocumentConverter factory
│       │   ├── loader.py        # PDF discovery, conversion, normalization
│       │   ├── types.py         # LoadedDocument wrapper + iter_chunks()
│       │   └── utils.py         # Hashing, safe attribute access, error helpers
│       │
│       ├── processing/
│       │   └── __init__.py      # (Reserved for future chunking/metadata logic)
│       │
│       ├── retrieval/
│       │   ├── __init__.py
│       │   ├── embeddings.py    # Embedding backends (Ollama / HF, local)
│       │   └── vectordb.py      # ChromaDB build/load helpers
│       │
│       ├── llm/
│       │   └── __init__.py      # (Reserved for LLM adapters / policies)
│       │
│       └── ui/
│           └── __init__.py      # (Reserved for Streamlit / egui frontends)
│
├── tests/
│   └── __init__.py              # (Test scaffolding; no tests yet)
│
├── README.md                    # Project overview & architecture
├── pyproject.toml               # Poetry configuration
├── poetry.lock
└── .gitignore
```

---

## Design Principles

* **Local-first**: no external APIs or cloud services
* **Evidence-driven**: every extracted field must be traceable to the source document
* **Composable**: OCR, chunking, retrieval, and LLM layers are decoupled
* **Human-review friendly**: outputs are structured, inspectable, and editable

---

## Definition of Done (MVP)

* Ingests both scanned and text-based PDFs
* Produces valid, schema-compliant metadata JSON
* Metadata fields include page-level evidence or are explicitly `null`
* Supports document-grounded Q&A with citations
* Runs fully locally using Ollama

---

## Future Extensions (Out of Scope for MVP)

* Template-aware extraction
* Confidence-based human review queue
* Desktop UI using Rust (`egui`)
* Lightweight fine-tuning or LoRA adapters
* Multi-document indexing

---

## Author

Developed as part of a Data Science & AI portfolio focused on operational analytics, document processing, and agentic systems.

## Disclaimer

This project is intended for research, educational, and portfolio purposes only.

The models and insights presented here are designed to demonstrate document processing and retrieval capabilities, not to serve as a production-ready system. Outputs should not be interpreted as guarantees of accuracy or completeness.

Any operational decisions should always rely on domain expertise, live data, and established procedures.
