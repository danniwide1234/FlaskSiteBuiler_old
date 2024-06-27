"""Add password reset table

Revision ID: 0987654321cd
Revises: 1234567890ab
Create Date: 2024-06-27 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '0987654321cd'
down_revision = '1234567890ab'
branch_labels = None
depends_on = None

def upgrade():
    # Create password_reset table
    op.create_table(
        'password_reset',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(length=128), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    )

def downgrade():
    # Drop password_reset table
    op.drop_table('password_reset')

