"""add content column to posts table

Revision ID: 87db01a12528
Revises: 0e1919f48def
Create Date: 2022-09-12 20:32:27.898963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87db01a12528'
down_revision = '0e1919f48def'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
