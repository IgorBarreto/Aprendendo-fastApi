"""Add foreign-key to post table

Revision ID: 06628247a609
Revises: 86af3a1e6735
Create Date: 2022-10-18 19:53:27.374205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06628247a609"
down_revision = "86af3a1e6735"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        constraint_name="post_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
