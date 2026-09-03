from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Iterable, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.inference_client import client
from app.models.document_vector import DocumentVector


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks (character-based approximation).

    Args:
        text: source text to chunk
        chunk_size: max characters per chunk
        overlap: characters of overlap between consecutive chunks

    Returns:
        list of text chunks
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: List[str] = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == text_len:
            break
        start = end - overlap

    return chunks


async def _embed_batch(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Call the async embeddings API for a batch of texts and return vectors.

    Uses the shared `client` from `app.ai.inference_client` which is an
    `AsyncOpenAI` instance configured for the project's provider.
    """
    if not texts:
        return []

    resp = await client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]


async def ingest_document(
    db: AsyncSession,
    job_id: UUID | None,
    source: str,
    text: str,
    metadata: Optional[dict] = None,
    chunk_size: int = 2000,
    overlap: int = 200,
    batch_size: int = 32,
    model: str = "text-embedding-3-small",
) -> int:
    """Chunk `text`, compute embeddings in batches, and persist DocumentVector rows.

    Returns number of vectors inserted.
    """
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    total_inserted = 0

    # feature-detect pgvector availability; if not present, fall back to JSON string
    try:
        import pgvector  # type: ignore

        has_pgvector = True
    except Exception:
        has_pgvector = False

    # process in batches
    for i in range(0, len(chunks), batch_size):
        batch_texts = chunks[i : i + batch_size]
        embeddings = await _embed_batch(batch_texts, model=model)

        rows = []
        for chunk_text_val, embedding in zip(batch_texts, embeddings):
            # store the chunk text inside metadata so retrieval can return the snippet
            row_metadata = dict(metadata or {})
            row_metadata["text"] = chunk_text_val

            row = DocumentVector(
                job_id=job_id,
                source=source,
                metadata_=row_metadata,
                embedding=(embedding if has_pgvector else json.dumps(embedding)),
            )
            rows.append(row)

        db.add_all(rows)
        await db.commit()
        total_inserted += len(rows)

    return total_inserted


def ingest_document_background(*, loop: Optional[asyncio.AbstractEventLoop] = None, **kwargs: Any) -> asyncio.Task:
    """Schedule ingestion in background using `asyncio.create_task`.

    Usage:
        ingest_document_background(db=db, job_id=..., source=..., text=...)

    The caller must ensure the `db` argument is an `AsyncSession` that is
    valid for use in the running event loop.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.create_task(ingest_document(**kwargs))
