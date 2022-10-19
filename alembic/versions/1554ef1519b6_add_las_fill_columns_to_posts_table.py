"""Add las fill columns to posts table

Revision ID: 1554ef1519b6
Revises: 06628247a609
Create Date: 2022-10-18 20:14:58.257231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1554ef1519b6"
down_revision = "06628247a609"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
