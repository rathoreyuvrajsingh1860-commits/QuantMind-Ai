"""add database defaults

Revision ID: ce10a3acd6dd
Revises: 274a37b29df0
Create Date: 2026-09-25 13:09:01.408327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce10a3acd6dd'
down_revision: Union[str, Sequence[str], None] = '274a37b29df0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    for table in (
        "companies",
        "financial_instruments",
        "data_sources",
        "research_documents",
        "evidence",
        "research_runs",
        "price_history",
    ):
        op.execute(
            f"ALTER TABLE {table} "
            "ALTER COLUMN id SET DEFAULT gen_random_uuid()"
        )

    for table in (
        "companies",
        "financial_instruments",
        "data_sources",
        "research_documents",
        "evidence",
        "research_runs",
    ):
        op.execute(
            f"ALTER TABLE {table} "
            "ALTER COLUMN metadata_json SET DEFAULT '{}'::jsonb"
        )


def downgrade() -> None:
    for table in (
        "companies",
        "financial_instruments",
        "data_sources",
        "research_documents",
        "evidence",
        "research_runs",
        "price_history",
    ):
        op.execute(
            f"ALTER TABLE {table} "
            "ALTER COLUMN id DROP DEFAULT"
        )

    for table in (
        "companies",
        "financial_instruments",
        "data_sources",
        "research_documents",
        "evidence",
        "research_runs",
    ):
        op.execute(
            f"ALTER TABLE {table} "
            "ALTER COLUMN metadata_json DROP DEFAULT"
        )