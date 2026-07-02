CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS competitors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  city TEXT,
  type TEXT,
  platform TEXT[],
  account_url TEXT,
  tags TEXT[],
  priority INTEGER DEFAULT 3,
  ai_score INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand_brains (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project TEXT NOT NULL,
  positioning TEXT,
  keywords TEXT[],
  avoid_words TEXT[],
  preferred_titles TEXT[],
  copy_tone TEXT,
  visual_style TEXT[],
  content_columns TEXT[],
  audience_profile TEXT,
  brand_partners TEXT[],
  kpi_preference TEXT[],
  content_ratio JSONB,
  version TEXT DEFAULT 'v1',
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content_source TEXT DEFAULT 'article' CHECK (
    content_source IN ('article', 'post', 'video', 'campaign', 'event', 'exhibition', 'news', 'other')
  ),
  platform TEXT,
  source_name TEXT,
  source_type TEXT,
  competitor_id UUID REFERENCES competitors(id) ON DELETE SET NULL,
  url TEXT UNIQUE,
  author TEXT,
  published_at TIMESTAMP,
  collected_at TIMESTAMP DEFAULT NOW(),
  summary TEXT,
  raw_text TEXT,
  cover_image TEXT,
  tags TEXT[],
  keywords TEXT[],
  city TEXT,
  business_area TEXT,
  category TEXT,
  matched_brands TEXT[],
  suitable_for TEXT[],
  heat_score INTEGER DEFAULT 0,
  brand_fit_in77 INTEGER DEFAULT 0,
  brand_fit_in88 INTEGER DEFAULT 0,
  innovation_score INTEGER DEFAULT 0,
  execution_score INTEGER DEFAULT 0,
  ai_reason TEXT,
  evidence JSONB,
  analysis_version TEXT,
  prompt_version TEXT,
  brand_brain_version TEXT,
  score_version TEXT,
  workflow_version TEXT,
  analysis_trace JSONB,
  content_status TEXT DEFAULT 'new' CHECK (
    content_status IN ('new', 'parsed', 'analyzed', 'selected', 'published', 'archived')
  ),
  analysis_status TEXT DEFAULT 'pending' CHECK (
    analysis_status IN ('pending', 'running', 'completed', 'failed')
  )
);

CREATE TABLE IF NOT EXISTS trends (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic TEXT NOT NULL,
  category TEXT,
  tags TEXT[],
  keywords TEXT[],
  content_count INTEGER DEFAULT 0,
  growth_rate FLOAT DEFAULT 0,
  trend_score INTEGER DEFAULT 0,
  lifecycle TEXT CHECK (
    lifecycle IS NULL OR lifecycle IN ('Emerging', 'Rising', 'Peak', 'Declining')
  ),
  related_contents UUID[],
  recommended_projects TEXT[],
  recommendation_reason TEXT,
  generated_at TIMESTAMP DEFAULT NOW(),
  analysis_trace JSONB
);

CREATE TABLE IF NOT EXISTS ideas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  project TEXT,
  angle TEXT,
  outline TEXT,
  suggested_platforms TEXT[],
  visual_suggestion TEXT,
  brand_suggestion TEXT,
  publish_timing TEXT,
  priority INTEGER DEFAULT 0,
  reason TEXT,
  decision TEXT DEFAULT 'discuss' CHECK (
    decision IN ('recommend', 'discuss', 'hold', 'reject', 'rewrite', 'archive')
  ),
  confidence FLOAT DEFAULT 0,
  explainability JSONB,
  status TEXT DEFAULT 'draft' CHECK (
    status IN ('draft', 'discussed', 'selected', 'scheduled', 'published', 'archived')
  ),
  brand_brain_id UUID REFERENCES brand_brains(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  report_type TEXT DEFAULT 'weekly' CHECK (
    report_type IN ('weekly', 'monthly', 'campaign')
  ),
  week_start DATE,
  week_end DATE,
  markdown_content TEXT,
  pdf_url TEXT,
  ppt_url TEXT,
  status TEXT DEFAULT 'draft' CHECK (
    status IN ('draft', 'completed', 'archived')
  ),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project TEXT NOT NULL,
  memory_type TEXT CHECK (
    memory_type IS NULL OR memory_type IN ('column', 'node_review', 'success_reason', 'failure_reason', 'comment_insight')
  ),
  related_topic TEXT,
  related_date DATE,
  related_content_id UUID REFERENCES contents(id) ON DELETE SET NULL,
  insight TEXT,
  recommendation TEXT,
  avoid_repeat BOOLEAN DEFAULT FALSE,
  reusable BOOLEAN DEFAULT TRUE,
  confidence FLOAT DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS performances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project TEXT NOT NULL,
  platform TEXT,
  content_id UUID REFERENCES contents(id) ON DELETE SET NULL,
  idea_id UUID REFERENCES ideas(id) ON DELETE SET NULL,
  publish_date DATE,
  reads INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  saves INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  engagement_rate FLOAT DEFAULT 0,
  comment_keywords TEXT[],
  kpi_result TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content_trends (
  content_id UUID NOT NULL REFERENCES contents(id) ON DELETE CASCADE,
  trend_id UUID NOT NULL REFERENCES trends(id) ON DELETE CASCADE,
  PRIMARY KEY (content_id, trend_id)
);

CREATE TABLE IF NOT EXISTS idea_contents (
  idea_id UUID NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  content_id UUID NOT NULL REFERENCES contents(id) ON DELETE CASCADE,
  PRIMARY KEY (idea_id, content_id)
);

CREATE TABLE IF NOT EXISTS idea_trends (
  idea_id UUID NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  trend_id UUID NOT NULL REFERENCES trends(id) ON DELETE CASCADE,
  PRIMARY KEY (idea_id, trend_id)
);

CREATE TABLE IF NOT EXISTS report_contents (
  report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  content_id UUID NOT NULL REFERENCES contents(id) ON DELETE CASCADE,
  PRIMARY KEY (report_id, content_id)
);

CREATE TABLE IF NOT EXISTS report_ideas (
  report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  idea_id UUID NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  PRIMARY KEY (report_id, idea_id)
);

CREATE INDEX IF NOT EXISTS idx_contents_url ON contents(url);
CREATE INDEX IF NOT EXISTS idx_contents_published_at ON contents(published_at);
CREATE INDEX IF NOT EXISTS idx_contents_status ON contents(content_status);
CREATE INDEX IF NOT EXISTS idx_contents_analysis_status ON contents(analysis_status);
CREATE INDEX IF NOT EXISTS idx_contents_platform ON contents(platform);
CREATE INDEX IF NOT EXISTS idx_contents_city ON contents(city);
CREATE INDEX IF NOT EXISTS idx_contents_category ON contents(category);
CREATE INDEX IF NOT EXISTS idx_contents_competitor_id ON contents(competitor_id);
CREATE INDEX IF NOT EXISTS idx_contents_analysis_version ON contents(analysis_version);
CREATE INDEX IF NOT EXISTS idx_contents_prompt_version ON contents(prompt_version);
CREATE INDEX IF NOT EXISTS idx_contents_brand_brain_version ON contents(brand_brain_version);

CREATE INDEX IF NOT EXISTS idx_competitors_name ON competitors(name);
CREATE INDEX IF NOT EXISTS idx_competitors_city ON competitors(city);
CREATE INDEX IF NOT EXISTS idx_competitors_type ON competitors(type);
CREATE INDEX IF NOT EXISTS idx_competitors_priority ON competitors(priority);

CREATE INDEX IF NOT EXISTS idx_trends_topic ON trends(topic);
CREATE INDEX IF NOT EXISTS idx_trends_category ON trends(category);
CREATE INDEX IF NOT EXISTS idx_trends_lifecycle ON trends(lifecycle);
CREATE INDEX IF NOT EXISTS idx_trends_trend_score ON trends(trend_score);
CREATE INDEX IF NOT EXISTS idx_trends_generated_at ON trends(generated_at);

CREATE INDEX IF NOT EXISTS idx_ideas_project ON ideas(project);
CREATE INDEX IF NOT EXISTS idx_ideas_priority ON ideas(priority);
CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
CREATE INDEX IF NOT EXISTS idx_ideas_decision ON ideas(decision);
CREATE INDEX IF NOT EXISTS idx_ideas_created_at ON ideas(created_at);

CREATE INDEX IF NOT EXISTS idx_reports_type ON reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_week_start ON reports(week_start);
CREATE INDEX IF NOT EXISTS idx_reports_week_end ON reports(week_end);
CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at);

CREATE INDEX IF NOT EXISTS idx_brand_brains_project ON brand_brains(project);
CREATE INDEX IF NOT EXISTS idx_brand_brains_version ON brand_brains(version);
CREATE INDEX IF NOT EXISTS idx_brand_brains_updated_at ON brand_brains(updated_at);

CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_memories_topic ON memories(related_topic);
CREATE INDEX IF NOT EXISTS idx_memories_date ON memories(related_date);

CREATE INDEX IF NOT EXISTS idx_performances_project ON performances(project);
CREATE INDEX IF NOT EXISTS idx_performances_platform ON performances(platform);
CREATE INDEX IF NOT EXISTS idx_performances_publish_date ON performances(publish_date);
CREATE INDEX IF NOT EXISTS idx_performances_content_id ON performances(content_id);
CREATE INDEX IF NOT EXISTS idx_performances_idea_id ON performances(idea_id);
