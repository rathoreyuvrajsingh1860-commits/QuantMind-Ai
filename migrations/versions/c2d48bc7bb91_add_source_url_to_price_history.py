"""add source url to price history

Revision ID: c2d48bc7bb91
Revises: 4bd5652d7d70
"""

from alembic import op
import sqlalchemy as sa


revision = "c2d48bc7bb91"
down_revision = "4bd5652d7d70"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "price_history",
        sa.Column(
            "source_url",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("price_history", "source_url")
