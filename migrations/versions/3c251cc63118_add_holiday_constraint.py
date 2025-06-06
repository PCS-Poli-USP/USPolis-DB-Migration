"""Add holiday constraint

Revision ID: 3c251cc63118
Revises: cf3211559b61
Create Date: 2024-07-29 22:31:31.459444

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "3c251cc63118"
down_revision: Union[str, None] = "cf3211559b61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "unique_holiday_date_for_category", "holiday", ["date", "category_id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unique_holiday_date_for_category", "holiday", type_="unique")
    # ### end Alembic commands ###
