""" load tables

Revision ID: e526f6394ef5
Revises: ab71ff761f29
Create Date: 2024-11-05 12:43:51.118427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e526f6394ef5'
down_revision: Union[str, None] = 'ab71ff761f29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
