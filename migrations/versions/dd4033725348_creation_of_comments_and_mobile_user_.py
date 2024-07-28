"""creation_of_comments_and_mobile_user_tables

Revision ID: dd4033725348
Revises: 42b0236b0310
Create Date: 2024-07-18 15:24:23.337557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dd4033725348'
down_revision: Union[str, None] = '42b0236b0310'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mobileuser', sa.Column('picture_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column('mobileuser', 'name')
    op.drop_column('mobileuser', 'picture')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mobileuser', sa.Column('picture', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('mobileuser', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('mobileuser', 'picture_url')
    # ### end Alembic commands ###