"""create contents table

Revision ID: 0001
Revises:
Create Date: 2026-07-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "contents",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content_source", sa.String(), nullable=False, server_default="article"),
        sa.Column("platform", sa.String()),
        sa.Column("source_name", sa.String()),
        sa.Column("source_type", sa.String()),
        sa.Column("competitor_id", sa.String()),
        sa.Column("url", sa.Text(), unique=True),
        sa.Column("author", sa.String()),
        sa.Column("published_at", sa.DateTime()),
        sa.Column("collected_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("summary", sa.Text()),
        sa.Column("raw_text", sa.Text()),
        sa.Column("cover_image", sa.Text()),
        sa.Column("tags", sa.JSON()),
        sa.Column("keywords", sa.JSON()),
        sa.Column("city", sa.String()),
        sa.Column("business_area", sa.String()),
        sa.Column("category", sa.String()),
        sa.Column("matched_brands", sa.JSON()),
        sa.Column("suitable_for", sa.JSON()),
        sa.Column("heat_score", sa.Integer(), server_default="0"),
        sa.Column("brand_fit_in77", sa.Integer(), server_default="0"),
        sa.Column("brand_fit_in88", sa.Integer(), server_default="0"),
        sa.Column("innovation_score", sa.Integer(), server_default="0"),
        sa.Column("execution_score", sa.Integer(), server_default="0"),
        sa.Column("ai_reason", sa.Text()),
        sa.Column("evidence", sa.JSON()),
        sa.Column("analysis_version", sa.String()),
        sa.Column("prompt_version", sa.String()),
        sa.Column("brand_brain_version", sa.String()),
        sa.Column("score_version", sa.String()),
        sa.Column("workflow_version", sa.String()),
        sa.Column("analysis_trace", sa.JSON()),
        sa.Column("content_status", sa.String(), nullable=False, server_default="new"),
        sa.Column("analysis_status", sa.String(), nullable=False, server_default="pending"),
    )
    op.create_index("idx_contents_url", "contents", ["url"])
    op.create_index("idx_contents_status", "contents", ["content_status"])
    op.create_index("idx_contents_analysis_status", "contents", ["analysis_status"])
    op.create_index("idx_contents_platform", "contents", ["platform"])
    op.create_index("idx_contents_source_name", "contents", ["source_name"])


def downgrade() -> None:
    op.drop_index("idx_contents_source_name", table_name="contents")
    op.drop_index("idx_contents_platform", table_name="contents")
    op.drop_index("idx_contents_analysis_status", table_name="contents")
    op.drop_index("idx_contents_status", table_name="contents")
    op.drop_index("idx_contents_url", table_name="contents")
    op.drop_table("contents")

