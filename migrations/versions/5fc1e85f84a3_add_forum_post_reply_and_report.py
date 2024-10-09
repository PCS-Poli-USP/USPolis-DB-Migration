"""add forum post reply and report

Revision ID: 5fc1e85f84a3
Revises: c075df6534bb
Create Date: 2024-09-09 14:24:07.711038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5fc1e85f84a3'
down_revision: Union[str, None] = 'c075df6534bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forumpostreportlink',
    sa.Column('forum_post_id', sa.Integer(), nullable=False),
    sa.Column('mobile_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['forum_post_id'], ['forumpost.id'], ),
    sa.ForeignKeyConstraint(['mobile_user_id'], ['mobileuser.id'], ),
    sa.PrimaryKeyConstraint('forum_post_id', 'mobile_user_id')
    )
    op.add_column('forumpost', sa.Column('reply_of_post_id', sa.Integer(), nullable=True))
    op.add_column('forumpost', sa.Column('replies_count', sa.Integer(), nullable=True))
    op.add_column('forumpost', sa.Column('enabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###
    op.execute("UPDATE forumpost SET replies_count = 0, enabled = true")
    op.alter_column('forumpost', 'replies_count', nullable=False)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('forumpost', 'replies_count')
    op.drop_column('forumpost', 'reply_of_post_id')
    op.drop_column('forumpost', 'enabled')
    op.drop_table('forumpostreportlink')
    # ### end Alembic commands ###
