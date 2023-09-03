"""empty message

Revision ID: bf6f6ab92ace
Revises: 997e8969befc
Create Date: 2023-08-16 16:00:22.900088

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'bf6f6ab92ace'
down_revision = '997e8969befc'
branch_labels = None
depends_on = None


def upgrade():
    user_type = postgresql.ENUM('system', 'regular', 'inactive', name='usertypeenum', create_type=False)
    user_type.create(op.get_bind())
    op.add_column('user', sa.Column('user_type', sa.Enum('system', 'regular', 'inactive', name='usertypeenum'), nullable=False))


def downgrade():
    op.drop_column('user', 'user_type')
    banner_status = postgresql.ENUM('system', 'regular', 'inactive', name='usertypeenum')
    banner_status.drop(op.get_bind())
