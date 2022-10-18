"""Add User table

Revision ID: 86af3a1e6735
Revises: 15c121937342
Create Date: 2022-10-18 03:11:28.574938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "86af3a1e6735"
down_revision = "15c121937342"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
