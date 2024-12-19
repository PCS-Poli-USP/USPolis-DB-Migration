"""Add holiday name

Revision ID: cf3211559b61
Revises: 2a4d06849f24
Create Date: 2024-07-29 14:01:10.072493

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "cf3211559b61"
down_revision: Union[str, None] = "2a4d06849f24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "classroom", "created_by_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "classroom", "building_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.add_column(
        "holiday",
        sa.Column(
            "name",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="Sem nome",
        ),
    )
    # ### end Alembic commands ###

    # Atualizando registros existentes com o valor padrão
    op.execute("UPDATE holiday SET name = 'Sem nome' WHERE name IS NULL")

    # Removendo o valor padrão da coluna
    op.alter_column("holiday", "name", server_default=None)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("holiday", "name")
    op.alter_column(
        "classroom", "building_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "classroom", "created_by_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###