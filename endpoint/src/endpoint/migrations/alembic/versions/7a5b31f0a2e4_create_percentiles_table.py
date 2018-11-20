"""create percentiles table

Revision ID: 7a5b31f0a2e4
Revises: 
Create Date: 2018-11-18 15:51:59.173781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a5b31f0a2e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'percentiles',
        sa.Column('percentile_log_date', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('percentile_25', sa.FLOAT, nullable=False),
        sa.Column('percentile_50', sa.FLOAT, nullable=False),
        sa.Column('percentile_75', sa.FLOAT, nullable=False),
    )


def downgrade():
    op.drop_table('percentiles')
