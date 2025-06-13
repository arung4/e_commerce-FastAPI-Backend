"""Add Password reset token model

Revision ID: 606d7b096b75
Revises: 
Create Date: 2025-06-12 22:46:26.098052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '606d7b096b75'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('password_reset_token', sa.Column('token', sa.String(), unique= True, index = True,nullable=True))
    op.add_column('password_reset_token', sa.Column('expiration_time', sa.DateTime(), nullable=False))
    op.add_column('password_reset_token', sa.Column('used', sa.Boolean(), default=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('password_reset_token', 'used')
    op.drop_column('password_reset_token', 'expiration_time')
    op.drop_column('password_reset_token', 'token')
