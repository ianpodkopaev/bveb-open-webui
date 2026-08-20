"""Add subdivision column to user table

Revision ID: 4f8a1b2c3d4e
Revises: a0b1c2d3e4f5
Create Date: 2026-08-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

revision = '4f8a1b2c3d4e'
down_revision = 'a0b1c2d3e4f5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('subdivision', sa.String(), nullable=True))


def downgrade():
    op.drop_column('user', 'subdivision')
