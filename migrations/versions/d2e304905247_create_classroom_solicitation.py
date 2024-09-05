"""Create Classroom Solicitation

Revision ID: d2e304905247
Revises: c075df6534bb
Create Date: 2024-09-05 03:44:54.201116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd2e304905247'
down_revision: Union[str, None] = 'c075df6534bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classroomsolicitation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('classroom_id', sa.Integer(), nullable=False),
    sa.Column('building_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('denied', sa.Boolean(), nullable=False),
    sa.Column('closed', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['building_id'], ['building.id'], ),
    sa.ForeignKeyConstraint(['classroom_id'], ['classroom.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('classroomsolicitation')
    # ### end Alembic commands ###
