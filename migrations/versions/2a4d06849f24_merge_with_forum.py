"""merge_with_forum

Revision ID: 2a4d06849f24
Revises:
Create Date: 2024-07-28 21:36:02.117503

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2a4d06849f24"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "institutionalevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("category", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("start", sa.DateTime(), nullable=False),
        sa.Column("end", sa.DateTime(), nullable=False),
        sa.Column("location", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("building", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("classroom", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("external_link", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("likes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mobileuser",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sub", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("given_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("family_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("picture_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subject",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("professors", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column(
            "type",
            sa.Enum("BIANNUAL", "FOUR_MONTHLY", "OTHER", name="subjecttype"),
            nullable=True,
        ),
        sa.Column("class_credit", sa.Integer(), nullable=False),
        sa.Column("work_credit", sa.Integer(), nullable=False),
        sa.Column("activation", sa.Date(), nullable=False),
        sa.Column("deactivation", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_subject_code"), "subject", ["code"], unique=True)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("cognito_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "building",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_building_name"), "building", ["name"], unique=True)
    op.create_table(
        "calendar",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_calendar_name"), "calendar", ["name"], unique=True)
    op.create_table(
        "class",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("professors", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "type",
            sa.Enum(
                "PRACTIC",
                "THEORIC",
                "VINCULATED_THEORIC",
                "VINCULATED_PRACTIC",
                name="classtype",
            ),
            nullable=False,
        ),
        sa.Column("vacancies", sa.Integer(), nullable=False),
        sa.Column("subscribers", sa.Integer(), nullable=False),
        sa.Column("pendings", sa.Integer(), nullable=False),
        sa.Column("air_conditionating", sa.Boolean(), nullable=False),
        sa.Column("accessibility", sa.Boolean(), nullable=False),
        sa.Column("projector", sa.Boolean(), nullable=False),
        sa.Column("ignore_to_allocate", sa.Boolean(), nullable=False),
        sa.Column("full_allocated", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subject.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", "subject_id", name="unique_class_code_for_subject"),
    )
    op.create_index(op.f("ix_class_subject_id"), "class", ["subject_id"], unique=False)
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("comment", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["mobileuser.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "holidaycategory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_holidaycategory_name"), "holidaycategory", ["name"], unique=True
    )
    op.create_table(
        "calendarholidaycategorylink",
        sa.Column("calendar_id", sa.Integer(), nullable=False),
        sa.Column("holiday_category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["calendar_id"],
            ["calendar.id"],
        ),
        sa.ForeignKeyConstraint(
            ["holiday_category_id"],
            ["holidaycategory.id"],
        ),
        sa.PrimaryKeyConstraint("calendar_id", "holiday_category_id"),
    )
    op.create_table(
        "classcalendarlink",
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("calendar_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["calendar_id"],
            ["calendar.id"],
        ),
        sa.ForeignKeyConstraint(
            ["class_id"],
            ["class.id"],
        ),
        sa.PrimaryKeyConstraint("class_id", "calendar_id"),
    )
    op.create_table(
        "classroom",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=False),
        sa.Column("ignore_to_allocate", sa.Boolean(), nullable=False),
        sa.Column("accessibility", sa.Boolean(), nullable=False),
        sa.Column("projector", sa.Boolean(), nullable=False),
        sa.Column("air_conditioning", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("building_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["building.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "name", "building_id", name="unique_classroom_name_for_building"
        ),
    )
    op.create_table(
        "forumpost",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.Date(), nullable=False),
        sa.Column("report_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["class_id"],
            ["class.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["mobileuser.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "holiday",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["holidaycategory.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subjectbuildinglink",
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["building.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subject.id"],
        ),
        sa.PrimaryKeyConstraint("subject_id", "building_id"),
    )
    op.create_table(
        "userbuildinglink",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["building.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "building_id"),
    )
    op.create_table(
        "reservation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("EXAM", "MEETING", "EVENT", "OTHER", name="reservationtype"),
            nullable=False,
        ),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("classroom_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["classroom_id"],
            ["classroom.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "name", "classroom_id", name="unique_reservation_name_for_classroom"
        ),
    )
    op.create_index(
        op.f("ix_reservation_created_by_id"),
        "reservation",
        ["created_by_id"],
        unique=False,
    )
    op.create_table(
        "schedule",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column(
            "week_day",
            sa.Enum(
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
                "SUNDAY",
                name="weekday",
            ),
            nullable=True,
        ),
        sa.Column("allocated", sa.Boolean(), nullable=False),
        sa.Column(
            "recurrence",
            sa.Enum(
                "DAILY",
                "WEEKLY",
                "BIWEEKLY",
                "MONTHLY",
                "NONE",
                "CUSTOM",
                name="recurrence",
            ),
            nullable=False,
        ),
        sa.Column(
            "month_week",
            sa.Enum("FIRST", "SECOND", "THIRD", "LAST", name="monthweek"),
            nullable=True,
        ),
        sa.Column("all_day", sa.Boolean(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=True),
        sa.Column("classroom_id", sa.Integer(), nullable=True),
        sa.Column("reservation_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["class_id"], ["class.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["classroom_id"],
            ["classroom.id"],
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservation.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "occurrence",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("classroom_id", sa.Integer(), nullable=True),
        sa.Column("schedule_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["classroom_id"],
            ["classroom.id"],
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedule.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_occurrence_schedule_id"), "occurrence", ["schedule_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_occurrence_schedule_id"), table_name="occurrence")
    op.drop_table("occurrence")
    op.drop_table("schedule")
    op.drop_index(op.f("ix_reservation_created_by_id"), table_name="reservation")
    op.drop_table("reservation")
    op.drop_table("userbuildinglink")
    op.drop_table("subjectbuildinglink")
    op.drop_table("holiday")
    op.drop_table("forumpost")
    op.drop_table("classroom")
    op.drop_table("classcalendarlink")
    op.drop_table("calendarholidaycategorylink")
    op.drop_index(op.f("ix_holidaycategory_name"), table_name="holidaycategory")
    op.drop_table("holidaycategory")
    op.drop_table("comment")
    op.drop_index(op.f("ix_class_subject_id"), table_name="class")
    op.drop_table("class")
    op.drop_index(op.f("ix_calendar_name"), table_name="calendar")
    op.drop_table("calendar")
    op.drop_index(op.f("ix_building_name"), table_name="building")
    op.drop_table("building")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_subject_code"), table_name="subject")
    op.drop_table("subject")
    op.drop_table("mobileuser")
    op.drop_table("institutionalevent")
    # ### end Alembic commands ###
