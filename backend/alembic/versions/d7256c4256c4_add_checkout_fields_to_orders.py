"""add checkout fields to orders

Revision ID: d7256c4256c4
Revises: e358f7506ee3
Create Date: 2026-09-09 19:43:41.092675

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d7256c4256c4"
down_revision: Union[str, Sequence[str], None] = "e358f7506ee3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "orders",
        sa.Column("phone", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "orders",
        sa.Column("delivery_type", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "orders",
        sa.Column("address", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "orders",
        sa.Column("payment_method", sa.String(length=20), nullable=True),
    )

    # Valores temporários para pedidos antigos.
    op.execute(
        "UPDATE orders SET phone = 'Não informado' WHERE phone IS NULL"
    )

    op.execute(
        "UPDATE orders SET delivery_type = 'retirada' "
        "WHERE delivery_type IS NULL"
    )

    op.execute(
        "UPDATE orders SET payment_method = 'pix' "
        "WHERE payment_method IS NULL"
    )

    op.alter_column(
        "orders",
        "phone",
        existing_type=sa.String(length=20),
        nullable=False,
    )

    op.alter_column(
        "orders",
        "delivery_type",
        existing_type=sa.String(length=20),
        nullable=False,
    )

    op.alter_column(
        "orders",
        "payment_method",
        existing_type=sa.String(length=20),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("orders", "payment_method")
    op.drop_column("orders", "address")
    op.drop_column("orders", "delivery_type")
    op.drop_column("orders", "phone")