"""backfill price history source urls

Revision ID: c3e438cbbb09
Revises: c2d48bc7bb91
"""

from alembic import op


revision = "c3e438cbbb09"
down_revision = "c2d48bc7bb91"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        UPDATE price_history
        SET source_url = CASE
            WHEN source = 'alpha_vantage'
                THEN 'https://www.alphavantage.co/documentation/#daily'
            WHEN source = 'twelve_data'
                THEN 'https://twelvedata.com/docs#time-series'
            ELSE source_url
        END
        WHERE source_url IS NULL
    """)


def downgrade() -> None:
    op.execute("""
        UPDATE price_history
        SET source_url = NULL
        WHERE source IN ('alpha_vantage', 'twelve_data')
    """)
