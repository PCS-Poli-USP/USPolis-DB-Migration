"""try1

Revision ID: f3e6c251a952
Revises: 0e8f9c2c9591
Create Date: 2024-07-09 13:12:58.564862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f3e6c251a952'
down_revision: Union[str, None] = '0e8f9c2c9591'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('schedule_class_id_fkey', 'schedule', type_='foreignkey')
    op.create_foreign_key(None, 'schedule', 'class', ['class_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.create_foreign_key('schedule_class_id_fkey', 'schedule', 'class', ['class_id'], ['id'])
    # ### end Alembic commands ###