# pdf_ingestor/src/pdf_ingestor/retrieval/embeddings.py

from __future__ import annotations

import requests


def assert_ollama_running(host: str = "http://localhost:11434") -> None:
    """
    Raises a RuntimeError if Ollama is not reachable.
    """
    try:
        r = requests.get(f"{host}/api/tags", timeout=2)
        r.raise_for_status()

        print("Ollama is running!")

    except Exception as e:
        raise RuntimeError(
            f"Ollama is not reachable at {host}. Start it with `ollama serve` "
            f"or open the Ollama app. Underlying error: {e}"
        )


def assert_ollama_model_available(
    model_name: str,
    host: str = "http://localhost:11434",
) -> str:
    """
    Verify that Ollama is running and that the requested model
    (with or without tag) is available locally.

    Returns:
        str: The resolved full model name (e.g. 'llama3.2:latest')

    Raises:
        RuntimeError: if Ollama is not reachable or the model is missing.
    """
    try:
        response = requests.get(f"{host}/api/tags", timeout=5)
        response.raise_for_status()
        payload = response.json()
    except Exception as e:
        raise RuntimeError(
            f"Ollama is not reachable at {host}. "
            f"Ensure it is running (`ollama serve`). "
            f"Underlying error: {e}"
        )

    # All available model names (fully-qualified)
    available_models = [
        m.get("name") for m in payload.get("models", []) if "name" in m
    ]

    # Exact match (user passed full tag)
    if model_name in available_models:
        print(f"✓ Ollama model '{model_name}' is available.")
        return model_name

    # Base-name match (e.g. 'llama3.2' → 'llama3.2:latest')
    base_matches = [
        m for m in available_models if m.startswith(f"{model_name}:")
    ]

    if base_matches:
        resolved = base_matches[0]
        print(f"✓ Ollama model '{model_name}' resolved to '{resolved}'.")
        return resolved

    raise RuntimeError(
        f"Ollama model '{model_name}' not found.\n\n"
        f"Available models: {available_models}\n\n"
        f"Fix by running:\n  ollama pull {model_name}"
    )
