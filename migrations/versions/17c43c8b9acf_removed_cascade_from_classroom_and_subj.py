"""removed cascade from classroom and subj

Revision ID: 17c43c8b9acf
Revises: 9e9dc7c058c5
Create Date: 2024-06-18 21:19:45.726620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '17c43c8b9acf'
down_revision: Union[str, None] = '9e9dc7c058c5'
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