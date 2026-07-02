CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS contents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  platform TEXT,
  source_name TEXT,
  source_type TEXT,
  url TEXT UNIQUE,
  author TEXT,
  published_at TIMESTAMP,
  collected_at TIMESTAMP DEFAULT NOW(),
  summary TEXT,
  raw_text TEXT,
  tags TEXT[],
  keywords TEXT[],
  category TEXT,
  heat_score INTEGER DEFAULT 0,
  brand_fit_in77 INTEGER DEFAULT 0,
  brand_fit_in88 INTEGER DEFAULT 0,
  innovation_score INTEGER DEFAULT 0,
  execution_score INTEGER DEFAULT 0,
  ai_reason TEXT,
  status TEXT DEFAULT 'new'
);

CREATE TABLE IF NOT EXISTS competitors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  city TEXT,
  type TEXT,
  platform TEXT[],
  account_url TEXT,
  tags TEXT[],
  priority INTEGER DEFAULT 3,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trends (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  keyword TEXT NOT NULL,
  period TEXT,
  count INTEGER DEFAULT 0,
  growth_rate FLOAT DEFAULT 0,
  score INTEGER DEFAULT 0,
  insight TEXT,
  created_at TIMESTAMP DEFAULT NOW()
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
  priority INTEGER DEFAULT 0,
  reason TEXT,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  week_start DATE,
  week_end DATE,
  markdown_content TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

