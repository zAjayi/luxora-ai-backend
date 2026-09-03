"""Add pgvector extension, document_vectors, chat_sessions, chat_messages

Revision ID: f6e7d8c9b0a1
Revises: b4b3f5c2f1e4
Create Date: 2026-08-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6e7d8c9b0a1'
down_revision: Union[str, Sequence[str], None] = 'b4b3f5c2f1e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create document_vectors table (stores chunks/embeddings)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS document_vectors (
            id uuid PRIMARY KEY,
            job_id uuid REFERENCES repurpose_jobs(id) ON DELETE CASCADE,
            source text,
            metadata jsonb,
            embedding vector(1536),
            created_at timestamp with time zone DEFAULT now()
        );
        """
    )

    # ivfflat index for vector search (cosine)
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_document_vectors_embedding ON document_vectors USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"
    )

    # Create chat_sessions table
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id uuid PRIMARY KEY,
            job_id uuid REFERENCES repurpose_jobs(id) ON DELETE SET NULL,
            user_id uuid REFERENCES users(id) ON DELETE SET NULL,
            status varchar(50),
            created_at timestamp with time zone DEFAULT now(),
            updated_at timestamp with time zone DEFAULT now()
        );
        """
    )

    # Create chat_messages table
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id uuid PRIMARY KEY,
            session_id uuid REFERENCES chat_sessions(id) ON DELETE CASCADE,
            role varchar(50),
            content text,
            metadata jsonb,
            created_at timestamp with time zone DEFAULT now()
        );
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_chat_messages_session_id ON chat_messages (session_id);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_chat_sessions_created_at ON chat_sessions (created_at);")


def downgrade() -> None:
    # Drop tables and index
    op.execute("DROP INDEX IF EXISTS ix_chat_messages_session_id;")
    op.execute("DROP TABLE IF EXISTS chat_messages;")
    op.execute("DROP TABLE IF EXISTS chat_sessions;")
    op.execute("DROP INDEX IF EXISTS ix_document_vectors_embedding;")
    op.execute("DROP TABLE IF EXISTS document_vectors;")

    # Optionally remove extension (leave if other code depends on it)
    # op.execute("DROP EXTENSION IF EXISTS vector;")
