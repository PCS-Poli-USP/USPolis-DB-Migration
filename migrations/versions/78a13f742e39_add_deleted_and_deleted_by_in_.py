"""Add deleted and deleted by in ClassroomSolicitation

Revision ID: 78a13f742e39
Revises: 9a116629041b
Create Date: 2025-03-14 18:03:34.733340

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "78a13f742e39"
down_revision: str | None = "9a116629041b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "classroomsolicitation", sa.Column("deleted", sa.Boolean(), nullable=True)
    )
    op.execute("UPDATE classroomsolicitation SET deleted = FALSE")
    op.alter_column("classroomsolicitation", "deleted", nullable=False)
    op.add_column(
        "classroomsolicitation",
        sa.Column("deleted_by", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("classroomsolicitation", "deleted_by")
    op.drop_column("classroomsolicitation", "deleted")
    # ### end Alembic commands ###
