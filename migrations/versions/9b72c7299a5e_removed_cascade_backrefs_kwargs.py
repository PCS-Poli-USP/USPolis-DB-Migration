"""removed cascade backrefs kwargs

Revision ID: 9b72c7299a5e
Revises: f3e6c251a952
Create Date: 2024-07-09 13:16:03.432897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9b72c7299a5e'
down_revision: Union[str, None] = 'f3e6c251a952'
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
