"""Update user_token table

Revision ID: 9e09f2a57ee3
Revises: 02836b38eab0
Create Date: 2024-12-12 21:40:25.925676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e09f2a57ee3'
down_revision: Union[str, None] = '02836b38eab0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_token', sa.Column('reset_password_token', sa.String(length=255), nullable=True))
    op.add_column('user_token', sa.Column('email_token', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_token', 'email_token')
    op.drop_column('user_token', 'reset_password_token')
    # ### end Alembic commands ###
