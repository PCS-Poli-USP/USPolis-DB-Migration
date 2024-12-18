"""forum_global

Revision ID: 64a70f848243
Revises: 49bd2f582a5a
Create Date: 2024-11-21 22:36:19.346377

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "64a70f848243"
down_revision: Union[str, None] = "49bd2f582a5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("forumpost", "class_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("forumpost", "class_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
