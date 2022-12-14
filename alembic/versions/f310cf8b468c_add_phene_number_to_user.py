"""add phene number to user

Revision ID: f310cf8b468c
Revises: 975459833b75
Create Date: 2022-10-18 20:29:54.356102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f310cf8b468c"
down_revision = "975459833b75"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("phone_number", sa.String(255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "phone_number")
    # ### end Alembic commands ###
