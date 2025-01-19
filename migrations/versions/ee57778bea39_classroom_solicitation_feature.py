"""classroom solicitation feature

Revision ID: ee57778bea39
Revises: 4abbc03d3542
Create Date: 2024-11-29 02:14:13.082106

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "ee57778bea39"
down_revision: Union[str, None] = "3c251cc63118"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "classroomsolicitation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("classroom_id", sa.Integer(), nullable=True),
        sa.Column("required_classroom", sa.Boolean(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("reservation_id", sa.Integer(), nullable=True),
        sa.Column("reason", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "reservation_title", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "reservation_type",
            sa.Enum("EXAM", "MEETING", "EVENT", "OTHER", name="reservationtype"),
            nullable=False,
        ),
        sa.Column("dates", sa.ARRAY(sa.Date()), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("approved", sa.Boolean(), nullable=False),
        sa.Column("denied", sa.Boolean(), nullable=False),
        sa.Column("closed", sa.Boolean(), nullable=False),
        sa.Column("closed_by", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "(classroom_id IS NOT NULL) OR (required_classroom = FALSE)",
            name="check_required_classroom_with_classroom_id_not_null",
        ),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["building.id"],
        ),
        sa.ForeignKeyConstraint(
            ["classroom_id"],
            ["classroom.id"],
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservation.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "reservation",
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.add_column(
        "reservation",
        sa.Column("reason", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.drop_constraint(
        "unique_reservation_name_for_classroom", "reservation", type_="unique"
    )
    op.drop_column("reservation", "description")
    op.drop_column("reservation", "name")
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.add_column(
        "reservation",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "reservation",
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.create_unique_constraint(
        "unique_reservation_name_for_classroom", "reservation", ["name", "classroom_id"]
    )
    op.drop_column("reservation", "reason")
    op.drop_column("reservation", "title")
    op.drop_table("classroomsolicitation")
    # ### end Alembic commands ###
