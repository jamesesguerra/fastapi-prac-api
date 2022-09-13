"""add foreign key to posts table

Revision ID: 70603b8f2aac
Revises: b4c031aafb9b
Create Date: 2022-09-12 20:44:37.795278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70603b8f2aac'
down_revision = 'b4c031aafb9b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
