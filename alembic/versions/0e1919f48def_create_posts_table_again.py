"""create posts table AGAIN

Revision ID: 0e1919f48def
Revises: b47e49e56c5e
Create Date: 2022-09-12 20:31:06.530568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e1919f48def'
down_revision = 'b47e49e56c5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
