"""Add content column to posts

Revision ID: 15c121937342
Revises: 138e4e9dbf76
Create Date: 2022-10-18 02:57:08.880523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "15c121937342"
down_revision = "138e4e9dbf76"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
