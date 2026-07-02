CREATE TEMP TABLE seed_competitors (
  name TEXT,
  city TEXT,
  type TEXT,
  priority INTEGER,
  tags_raw TEXT
);

COPY seed_competitors(name, city, type, priority, tags_raw)
FROM '/docker-entrypoint-initdb.d/seed/competitors.csv'
WITH (FORMAT csv, HEADER true);

INSERT INTO competitors (name, city, type, priority, tags)
SELECT
  name,
  city,
  type,
  priority,
  string_to_array(tags_raw, ';')
FROM seed_competitors
ON CONFLICT DO NOTHING;

CREATE TEMP TABLE seed_projects (
  project TEXT,
  name TEXT,
  city TEXT,
  positioning TEXT,
  keywords_raw TEXT,
  avoid_words_raw TEXT
);

COPY seed_projects(project, name, city, positioning, keywords_raw, avoid_words_raw)
FROM '/docker-entrypoint-initdb.d/seed/projects.csv'
WITH (FORMAT csv, HEADER true);

INSERT INTO brand_brains (
  project,
  positioning,
  keywords,
  avoid_words,
  version
)
SELECT
  project,
  positioning,
  string_to_array(keywords_raw, ';'),
  string_to_array(avoid_words_raw, ';'),
  '1.0'
FROM seed_projects;
