"""create ideas table

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ideas",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("project", sa.String(), nullable=False),
        sa.Column("trend_id", sa.String()),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("outline", sa.Text()),
        sa.Column("references", sa.JSON()),
        sa.Column("recommendation_reason", sa.Text()),
        sa.Column("execution_cost", sa.String(), nullable=False, server_default="medium"),
        sa.Column("platforms", sa.JSON()),
        sa.Column("status", sa.String(), nullable=False, server_default="draft"),
        sa.Column("source_trends", sa.JSON()),
        sa.Column("source_contents", sa.JSON()),
        sa.Column("ai_trace", sa.JSON()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_ideas_project", "ideas", ["project"])
    op.create_index("idx_ideas_trend_id", "ideas", ["trend_id"])
    op.create_index("idx_ideas_priority", "ideas", ["priority"])
    op.create_index("idx_ideas_status", "ideas", ["status"])
    op.create_index("idx_ideas_execution_cost", "ideas", ["execution_cost"])
    op.create_index("idx_ideas_created_at", "ideas", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_ideas_created_at", table_name="ideas")
    op.drop_index("idx_ideas_execution_cost", table_name="ideas")
    op.drop_index("idx_ideas_status", table_name="ideas")
    op.drop_index("idx_ideas_priority", table_name="ideas")
    op.drop_index("idx_ideas_trend_id", table_name="ideas")
    op.drop_index("idx_ideas_project", table_name="ideas")
    op.drop_table("ideas")
