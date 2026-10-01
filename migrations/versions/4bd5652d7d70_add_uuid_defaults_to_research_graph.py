"""add UUID defaults to research graph

Revision ID: 4bd5652d7d70
Revises: 6ca7352bc407
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "4bd5652d7d70"
down_revision = "6ca7352bc407"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE research_claims
        ALTER COLUMN id SET DEFAULT gen_random_uuid()
        """
    )

    op.execute(
        """
        ALTER TABLE claim_evidence
        ALTER COLUMN id SET DEFAULT gen_random_uuid()
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE claim_evidence
        ALTER COLUMN id DROP DEFAULT
        """
    )

    op.execute(
        """
        ALTER TABLE research_claims
        ALTER COLUMN id DROP DEFAULT
        """
    )