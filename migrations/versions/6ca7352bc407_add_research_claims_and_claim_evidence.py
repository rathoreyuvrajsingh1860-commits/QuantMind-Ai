"""add research claims and claim evidence

Revision ID: 6ca7352bc407
Revises: ce10a3acd6dd
Create Date: 2026-10-01 01:55:04.113397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "6ca7352bc407"
down_revision: Union[str, Sequence[str], None] = "ce10a3acd6dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create research claims and claim-to-evidence relationships."""

    op.create_table(
        "research_claims",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "research_run_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column("claim_type", sa.String(length=50), nullable=False),
        sa.Column("claim_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column(
            "metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["research_run_id"],
            ["research_runs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "claim_evidence",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("claim_id", sa.UUID(), nullable=False),
        sa.Column("evidence_id", sa.UUID(), nullable=False),
        sa.Column("relationship", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["claim_id"],
            ["research_claims.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["evidence_id"],
            ["evidence.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "claim_id",
            "evidence_id",
            "relationship",
            name="uq_claim_evidence_relationship",
        ),
    )


def downgrade() -> None:
    """Drop research claims and claim-to-evidence relationships."""

    op.drop_table("claim_evidence")
    op.drop_table("research_claims")