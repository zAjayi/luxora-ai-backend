from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.ai.inference_client import client


async def embed_query(text_query: str, model: str = "text-embedding-3-small") -> List[float]:
    resp = await client.embeddings.create(model=model, input=[text_query])
    return resp.data[0].embedding


async def search_vectors(
    db: AsyncSession,
    query: Optional[str] = None,
    query_embedding: Optional[List[float]] = None,
    job_id: Optional[str] = None,
    k: int = 5,
) -> List[Dict[str, Any]]:
    """Return top-k document_vectors nearest the query (by cosine distance).

    Each result contains: id, job_id, source, metadata, distance
    """
    if query_embedding is None:
        if not query:
            raise ValueError("Either query or query_embedding must be provided")
        query_embedding = await embed_query(query)

    # build a pgvector literal like '[0.1,0.2,...]'
    vector_literal = "'[" + ",".join(str(float(x)) for x in query_embedding) + "]'::vector"

    where_clause = ""
    params = {}
    if job_id:
        where_clause = "WHERE job_id = :job_id"
        params["job_id"] = job_id

    sql = text(f"SELECT id, job_id, source, metadata, created_at, embedding <=> {vector_literal} AS distance FROM document_vectors {where_clause} ORDER BY distance ASC LIMIT :k")
    params["k"] = k

    result = await db.execute(sql, params)
    rows = result.fetchall()

    out: List[Dict[str, Any]] = []
    for row in rows:
        out.append({
            "id": str(row[0]),
            "job_id": str(row[1]) if row[1] is not None else None,
            "source": row[2],
            "metadata": row[3],
            "created_at": row[4].isoformat() if row[4] is not None else None,
            "distance": float(row[5]) if row[5] is not None else None,
        })

    return out


def build_rag_prompt(system_prompt: str, user_question: str, retrieved: List[Dict[str, Any]], max_snippets: int = 5) -> str:
    """Assemble a RAG-style prompt: system + retrieved snippets + user question.

    Retrieved items should include snippet text inside metadata['text'] when available.
    """
    snippets_texts = []
    for r in retrieved[:max_snippets]:
        md = r.get("metadata") or {}
        text_snip = md.get("text") if isinstance(md, dict) else None
        if text_snip:
            snippets_texts.append(text_snip)
        else:
            # fallback to source field
            if r.get("source"):
                snippets_texts.append(r.get("source"))

    retrieved_block = "\n\n--- Retrieved Context ---\n\n" + "\n\n".join(snippets_texts) if snippets_texts else ""

    prompt = system_prompt + "\n\n" + "Use the retrieved context to help answer the user's query. " + retrieved_block + "\n\nUser query:\n" + user_question
    return prompt
