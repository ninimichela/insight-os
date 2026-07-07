"""add content intelligence fields

Revision ID: 0005
Revises: 0004
Create Date: 2026-07-07
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("contents", sa.Column("freshness_score", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("contents", sa.Column("relevance_score", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("contents", sa.Column("novelty_score", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("contents", sa.Column("trend_score", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("contents", sa.Column("duplicate_status", sa.String(), nullable=False, server_default="unique"))
    op.add_column("contents", sa.Column("insight", sa.Text()))
    op.add_column("contents", sa.Column("business_opportunity", sa.Text()))
    op.create_index("idx_contents_duplicate_status", "contents", ["duplicate_status"])
    op.create_index("idx_contents_freshness_score", "contents", ["freshness_score"])
    op.create_index("idx_contents_relevance_score", "contents", ["relevance_score"])
    op.create_index("idx_contents_trend_score", "contents", ["trend_score"])


def downgrade() -> None:
    op.drop_index("idx_contents_trend_score", table_name="contents")
    op.drop_index("idx_contents_relevance_score", table_name="contents")
    op.drop_index("idx_contents_freshness_score", table_name="contents")
    op.drop_index("idx_contents_duplicate_status", table_name="contents")
    op.drop_column("contents", "business_opportunity")
    op.drop_column("contents", "insight")
    op.drop_column("contents", "duplicate_status")
    op.drop_column("contents", "trend_score")
    op.drop_column("contents", "novelty_score")
    op.drop_column("contents", "relevance_score")
    op.drop_column("contents", "freshness_score")
