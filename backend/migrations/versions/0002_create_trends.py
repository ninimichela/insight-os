"""create trends table

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trends",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("topic", sa.Text(), nullable=False),
        sa.Column("category", sa.String()),
        sa.Column("tags", sa.JSON()),
        sa.Column("keywords", sa.JSON()),
        sa.Column("content_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("growth_rate", sa.Float(), nullable=False, server_default="0"),
        sa.Column("trend_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("lifecycle", sa.String(), nullable=False, server_default="Emerging"),
        sa.Column("related_contents", sa.JSON()),
        sa.Column("recommended_projects", sa.JSON()),
        sa.Column("recommendation_reason", sa.Text()),
        sa.Column("generated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("analysis_trace", sa.JSON()),
    )
    op.create_index("idx_trends_topic", "trends", ["topic"])
    op.create_index("idx_trends_category", "trends", ["category"])
    op.create_index("idx_trends_lifecycle", "trends", ["lifecycle"])
    op.create_index("idx_trends_trend_score", "trends", ["trend_score"])
    op.create_index("idx_trends_generated_at", "trends", ["generated_at"])


def downgrade() -> None:
    op.drop_index("idx_trends_generated_at", table_name="trends")
    op.drop_index("idx_trends_trend_score", table_name="trends")
    op.drop_index("idx_trends_lifecycle", table_name="trends")
    op.drop_index("idx_trends_category", table_name="trends")
    op.drop_index("idx_trends_topic", table_name="trends")
    op.drop_table("trends")
