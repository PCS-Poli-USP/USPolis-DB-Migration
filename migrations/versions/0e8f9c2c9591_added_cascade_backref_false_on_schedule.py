"""added cascade backref false on schedule

Revision ID: 0e8f9c2c9591
Revises: 98694a68dbb0
Create Date: 2024-07-09 13:05:56.706340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0e8f9c2c9591'
down_revision: Union[str, None] = '98694a68dbb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
