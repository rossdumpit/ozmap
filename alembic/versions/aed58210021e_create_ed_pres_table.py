"""create ed_pres table

Revision ID: aed58210021e
Revises: 
Create Date: 2026-06-07 09:12:39.744903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aed58210021e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ed_pres',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('reporting_unit', sa.String(255)),
        sa.Column('reporting_unit_type', sa.String(50)),
        sa.Column('state', sa.String(10)),
        sa.Column('year', sa.SmallInteger()),
        sa.Column('triage_cat', sa.String(50)),
        sa.Column('presentation', sa.Integer()),
        sa.UniqueConstraint('reporting_unit', 'reporting_unit_type', 'state', 'year', 'triage_cat')
    )

def downgrade() -> None:
    op.drop_table('ed_pres')
