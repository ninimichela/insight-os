"""create reports table

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("week_start", sa.Date()),
        sa.Column("week_end", sa.Date()),
        sa.Column("markdown_content", sa.Text()),
        sa.Column("trend_ids", sa.JSON()),
        sa.Column("idea_ids", sa.JSON()),
        sa.Column("content_ids", sa.JSON()),
        sa.Column("status", sa.String(), nullable=False, server_default="completed"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_reports_status", "reports", ["status"])
    op.create_index("idx_reports_created_at", "reports", ["created_at"])
    op.create_index("idx_reports_week_start", "reports", ["week_start"])
    op.create_index("idx_reports_week_end", "reports", ["week_end"])


def downgrade() -> None:
    op.drop_index("idx_reports_week_end", table_name="reports")
    op.drop_index("idx_reports_week_start", table_name="reports")
    op.drop_index("idx_reports_created_at", table_name="reports")
    op.drop_index("idx_reports_status", table_name="reports")
    op.drop_table("reports")
