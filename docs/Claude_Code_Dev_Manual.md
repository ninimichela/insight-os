# INSight OS｜Claude Code 开发手册 V1.0

**AI Content Intelligence System**  
for 北京 in77 & 北京 in88

| 项目 | 内容 |
| --- | --- |
| 产品代号 | INSight OS |
| 文档类型 | Claude Code 开发手册 |
| Version | 1.0 |
| Owner | Michelle Ni |
| Created | 2026 |
| 开发目标 | 将 PRD 转化为可运行 MVP |

---

## 0. 项目目标

将 PRD 转化为一个可开发、可运行、可迭代的 MVP 系统。

开发原则：

```text
Every feature must improve a content decision.
If it only generates more content but does not improve a decision,
it does not belong in INSight OS.
```

MVP 前冻结规则：

```text
No New Engine Before MVP.
```

在 `v1.0` 之前，不新增 Engine、Database、Workflow 或 Prompt 分类，只完善已有模块。

第一版核心链路：

```text
用户导入竞品内容
        ↓
AI 摘要、标签、评分
        ↓
系统沉淀到内容库
        ↓
AI 生成热点分析
        ↓
AI 生成 in77 / in88 选题
        ↓
AI 生成周报
```

MVP 目标不是一开始实现全自动采集，而是先跑通：

**内容入库 → AI 分析 → 选题生成 → 周报输出。**

---

## 1. 技术栈建议

### 1.1 前端

- Next.js
- React
- Tailwind CSS
- shadcn/ui

### 1.2 后端

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### 1.3 数据库

- PostgreSQL
- pgvector

### 1.4 任务调度

V1 可选：

- Cron
- Celery
- n8n

推荐 MVP 初期先使用 Cron 或手动触发接口，n8n 在自动化阶段接入。

### 1.5 AI

- OpenAI API
- Embedding 用于语义搜索和相似内容识别

### 1.6 部署

- Vercel：前端
- Railway / Render：后端
- Supabase / Neon：PostgreSQL
- GitHub Actions：自动部署

---

## 2. 项目目录结构

```text
insight-os/
├── apps/
│   ├── web/
│   │   ├── app/
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── contents/
│   │   │   │   └── page.tsx
│   │   │   ├── competitors/
│   │   │   │   └── page.tsx
│   │   │   ├── trends/
│   │   │   │   └── page.tsx
│   │   │   ├── ideas/
│   │   │   │   └── page.tsx
│   │   │   ├── reports/
│   │   │   │   └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── tables/
│   │   │   ├── cards/
│   │   │   └── forms/
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── utils.ts
│   │   └── package.json
│   │
│   └── api/
│       ├── main.py
│       ├── database.py
│       ├── settings.py
│       ├── routers/
│       │   ├── contents.py
│       │   ├── competitors.py
│       │   ├── trends.py
│       │   ├── ideas.py
│       │   ├── reports.py
│       │   └── ai.py
│       ├── services/
│       │   ├── collector_service.py
│       │   ├── ai/
│       │   │   ├── summarizer.py
│       │   │   ├── tagger.py
│       │   │   ├── scorer.py
│       │   │   ├── classifier.py
│       │   │   ├── idea_generator.py
│       │   │   └── report_generator.py
│       │   ├── trend_service.py
│       │   ├── idea_service.py
│       │   └── report_service.py
│       ├── repositories/
│       │   ├── content_repository.py
│       │   ├── competitor_repository.py
│       │   ├── trend_repository.py
│       │   ├── idea_repository.py
│       │   └── report_repository.py
│       ├── models/
│       │   ├── content.py
│       │   ├── competitor.py
│       │   ├── trend.py
│       │   ├── idea.py
│       │   └── report.py
│       ├── schemas/
│       │   ├── content.py
│       │   ├── competitor.py
│       │   ├── trend.py
│       │   ├── idea.py
│       │   └── report.py
│       ├── scripts/
│       │   ├── import_csv.py
│       │   ├── run_daily_analysis.py
│       │   └── run_weekly_report.py
│       └── requirements.txt
│
├── packages/
│   ├── prompts/
│   │   ├── v1/
│   │   │   ├── analysis/
│   │   │   ├── idea/
│   │   │   └── report/
│   │   ├── summarize_content.md
│   │   ├── tag_content.md
│   │   ├── score_content.md
│   │   ├── generate_trends.md
│   │   ├── generate_ideas.md
│   │   ├── expand_content.md
│   │   └── weekly_report.md
│   │
│   └── config/
│       ├── competitors.json
│       ├── keywords.json
│       ├── brand_profiles.json
│       └── scoring_rules.json
│
├── workflows/
│   ├── daily_collect.json
│   ├── daily_ai_analysis.json
│   └── weekly_report.json
│
├── docs/
│   ├── PRD.md
│   └── CLAUDE_CODE_DEV_MANUAL.md
│
├── .env.example
└── README.md
```

---

## 3. 环境变量

创建 `.env.example`：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/insight_os
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-5.5
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
APP_ENV=development
API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

MVP 阶段可先不启用登录系统。

---

## 4. 数据库表设计

### 4.1 contents 内容库

```sql
CREATE TABLE contents (
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
  cover_image TEXT,
  tags TEXT[],
  keywords TEXT[],
  city TEXT,
  category TEXT,
  matched_brands TEXT[],
  suitable_for TEXT[],
  heat_score INTEGER DEFAULT 0,
  brand_fit_in77 INTEGER DEFAULT 0,
  brand_fit_in88 INTEGER DEFAULT 0,
  innovation_score INTEGER DEFAULT 0,
  execution_score INTEGER DEFAULT 0,
  ai_reason TEXT,
  reference_value TEXT,
  status TEXT DEFAULT 'new'
);
```

### 4.2 competitors 竞品库

```sql
CREATE TABLE competitors (
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
```

### 4.3 trends 热点库

```sql
CREATE TABLE trends (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  keyword TEXT NOT NULL,
  period TEXT,
  count INTEGER DEFAULT 0,
  growth_rate FLOAT DEFAULT 0,
  related_content_ids UUID[],
  score INTEGER DEFAULT 0,
  insight TEXT,
  recommendation TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.4 ideas 选题库

```sql
CREATE TABLE ideas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  project TEXT,
  angle TEXT,
  outline TEXT,
  reference_content_ids UUID[],
  suggested_platforms TEXT[],
  visual_suggestion TEXT,
  brand_suggestion TEXT,
  publish_timing TEXT,
  priority INTEGER DEFAULT 0,
  reason TEXT,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.5 reports 周报库

```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  week_start DATE,
  week_end DATE,
  markdown_content TEXT,
  pdf_url TEXT,
  ppt_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.6 content_embeddings 语义向量表（P2）

```sql
CREATE TABLE content_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content_id UUID REFERENCES contents(id),
  embedding vector(3072),
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 5. 核心接口设计

### 5.1 内容接口

```text
GET    /contents
GET    /contents/{id}
POST   /contents
POST   /contents/batch
POST   /contents/import-csv
POST   /contents/{id}/analyze
POST   /contents/analyze-batch
```

### 5.2 竞品接口

```text
GET    /competitors
POST   /competitors
PUT    /competitors/{id}
DELETE /competitors/{id}
```

### 5.3 热点接口

```text
GET    /trends?period=7d
POST   /trends/generate
```

### 5.4 选题接口

```text
GET    /ideas?project=in77
POST   /ideas/generate
POST   /ideas/{id}/expand
PUT    /ideas/{id}
```

### 5.5 周报接口

```text
GET    /reports
GET    /reports/{id}
POST   /reports/generate
```

### 5.6 AI 接口

```text
POST   /ai/summarize
POST   /ai/tag
POST   /ai/score
POST   /ai/generate-ideas
POST   /ai/generate-report
```

---

## 6. AI 任务流

### 6.1 内容分析流程

输入：一篇内容。

输出：

- 100 字摘要
- 标签
- 关键词
- 内容类型
- 是否适合 in77
- 是否适合 in88
- 爆款原因
- 可借鉴点
- AI 评分

Prompt 文件：

```text
packages/prompts/summarize_content.md
packages/prompts/tag_content.md
packages/prompts/score_content.md
```

返回结构：

```json
{
  "summary": "100字摘要",
  "tags": ["Citywalk", "艺术", "夏天"],
  "keywords": ["王府井", "展览", "周末"],
  "category": "生活方式",
  "suitable_for": ["in88"],
  "heat_score": 85,
  "brand_fit_in77": 62,
  "brand_fit_in88": 91,
  "innovation_score": 80,
  "execution_score": 88,
  "reference_value": "适合借鉴为室内漫游路线。",
  "ai_reason": "该内容兼具季节、地点和可拍摄性。"
}
```

### 6.2 热点分析流程

输入：过去 7 天内容。

输出：

- 热点 TOP10
- 增长最快话题
- 已经过度使用话题
- 值得跟进话题
- 不建议跟进话题

接口：

```text
POST /trends/generate
```

### 6.3 选题生成流程

输入：

- 热点
- 竞品案例
- in77 / in88 品牌调性
- 当前季节、节气、活动节点
- 可用品牌资源

输出：

每个项目 5 条选题：

- 选题标题
- 内容角度
- 内容大纲
- 图片建议
- 品牌结合建议
- 执行成本
- 推荐理由

接口：

```text
POST /ideas/generate
```

### 6.4 周报生成流程

输入：过去 7 天内容、热点、竞品、选题。

输出：

```text
北京商业内容观察｜Week XX

1. 本周热点 TOP10
2. 公众号内容观察
3. 小红书内容观察
4. 竞品案例拆解
5. in77 内容建议 ×5
6. in88 内容建议 ×5
7. 下周节点提醒
8. 执行优先级
```

接口：

```text
POST /reports/generate
```

---

## 7. 品牌配置

文件位置：

```text
packages/config/brand_profiles.json
```

建议内容：

```json
{
  "in77": {
    "name": "北京 in77",
    "tone": "城市、公园、CBD、艺术、品牌体验、松弛、开放",
    "avoid": "过度促销、口水化、强卖点堆叠",
    "keywords": ["CBD", "公园", "城市生活", "艺术", "品牌快闪", "夜晚", "松弛感"],
    "content_ratio": {
      "brand_dna": 0.8,
      "innovation": 0.2
    }
  },
  "in88": {
    "name": "北京王府井银泰 in88",
    "tone": "年轻、科技、动漫、潮流、室内漫游、王府井、生活方式",
    "avoid": "传统百货口吻、硬广、老派商场话术",
    "keywords": ["王府井", "科技", "动漫", "乐高", "高达", "华为", "宇树", "影石", "室内Citywalk"],
    "content_ratio": {
      "brand_dna": 0.8,
      "innovation": 0.2
    }
  }
}
```

---

## 8. 数据源配置

文件位置：

```text
packages/config/competitors.json
```

```json
[
  {
    "name": "北京SKP",
    "city": "北京",
    "type": "商业项目",
    "priority": 5
  },
  {
    "name": "三里屯太古里",
    "city": "北京",
    "type": "商业项目",
    "priority": 5
  },
  {
    "name": "北京THE BOX",
    "city": "北京",
    "type": "商业项目",
    "priority": 5
  },
  {
    "name": "北京LOOK",
    "city": "北京",
    "type": "城市媒体",
    "priority": 5
  }
]
```

关键词配置：

```text
packages/config/keywords.json
```

```json
{
  "xiaohongshu": ["北京商场", "北京周末", "北京探店", "北京展览", "北京生活方式", "北京艺术展", "北京Citywalk", "北京CBD", "北京王府井", "北京国贸"],
  "themes": ["夏天", "音乐", "艺术", "Citywalk", "餐饮", "IP", "科技", "亲子", "动漫", "运动", "夜生活", "展览"]
}
```

---

## 9. 页面说明

### 9.1 Dashboard 首页

展示：

- 今日采集数量
- 本周热点 TOP5
- 竞品更新数量
- 推荐选题数量
- 最新周报入口

### 9.2 内容库 Contents

功能：

- 按平台筛选
- 按标签筛选
- 按竞品筛选
- 搜索标题 / 关键词
- 查看 AI 摘要
- 查看可借鉴点
- 批量导入 CSV
- 批量 AI 分析

### 9.3 竞品中心 Competitors

功能：

- 添加竞品
- 设置监测优先级
- 查看竞品发文历史
- 查看竞品内容标签分布

### 9.4 热点趋势 Trends

功能：

- 查看 24h / 7d / 30d 热点
- 查看话题增长趋势
- 查看关联内容
- 一键生成选题

### 9.5 灵感池 Ideas

功能：

- 按 in77 / in88 筛选
- 查看选题标题
- 查看大纲
- 一键扩展为公众号
- 一键扩展为小红书
- 一键生成朋友圈文案
- 标记状态：待评估 / 已采用 / 已放弃

### 9.6 周报 Reports

功能：

- 查看历史周报
- 生成本周周报
- 导出 Markdown
- 导出 PDF
- 后续支持 PPT

---

## 10. 前端设计要求

前端应为内部工作台，不做营销型首页。

设计原则：

- 信息密度适中，适合每天打开看
- 首页突出“今天该看什么”和“本周该做什么”
- 表格、标签、筛选器、状态徽章要清晰
- 选题卡片要能快速判断是否值得执行
- 所有 AI 输出都要展示来源依据

推荐组件：

- Cards：核心指标和选题卡
- Table：内容库、竞品库、周报列表
- Badge：标签、平台、优先级
- Tabs：24h / 7d / 30d 热点
- Dialog：AI 生成内容预览
- Button：生成、分析、导入、导出

---

## 11. MVP 开发优先级

### P0 必须完成

- 内容库
- 竞品配置
- 手动录入 / 批量导入内容
- AI 摘要
- AI 标签
- AI 评分
- 生成 in77 / in88 选题
- 生成 Markdown 周报

### P1 第二阶段

- 自动采集公众号合规来源
- 自动采集公开资讯
- 小红书关键词监测
- 热点趋势图
- PDF 导出

### P2 第三阶段

- Dashboard 完整增强
- PPT 导出
- 语义搜索
- 品牌 DNA
- 内容表现数据回流

---

## 12. Claude Code 执行指令

### 第一步：初始化项目

```text
Create a monorepo project named insight-os.

Use:
- Next.js for frontend in apps/web
- FastAPI for backend in apps/api
- PostgreSQL as database
- Tailwind CSS and shadcn/ui for frontend UI
- SQLAlchemy for database ORM
```

### 第二步：创建数据库模型

```text
Create SQLAlchemy models for:
- contents
- competitors
- trends
- ideas
- reports

Use the fields defined in the PRD.
Also create Pydantic schemas and CRUD endpoints for each model.
```

### 第三步：创建 AI Service

```text
Create split AI service files under apps/api/services/ai.

They should include:
- summarize_content(content)
- tag_content(content)
- score_content(content)
- generate_trends(period)
- generate_ideas(project, trends, references)
- generate_weekly_report(start_date, end_date)

Use OpenAI API.
Read prompt templates from packages/prompts.
Return structured JSON.
```

Do not create one large ai_service.py.

### 第四步：创建前端页面

```text
Create pages:
- /dashboard
- /contents
- /competitors
- /trends
- /ideas
- /reports
- /settings

Use shadcn/ui cards, tables, badges, filters, dialogs, tabs and buttons.
```

### 第五步：创建 CSV 导入

```text
Create a CSV import feature for contents.

Required columns:
- title
- platform
- source_name
- source_type
- url
- author
- published_at
- raw_text

After import, save records with status = "new".
```

### 第六步：创建批量 AI 分析

```text
Create a batch analysis endpoint.

It should:
1. Query contents with status = "new"
2. Run summarize_content
3. Run tag_content
4. Run score_content
5. Update content fields
6. Change status to "analyzed"
```

### 第七步：创建周报生成

```text
Build a weekly report generator.

It should:
1. Query contents from the last 7 days
2. Query trends from the last 7 days
3. Query generated ideas for in77 and in88
4. Generate a Markdown report
5. Save it into reports table
```

---

## 13. 后端实现建议

### 13.1 FastAPI main.py

应包含：

- CORS 配置
- 路由注册
- 健康检查接口

```text
GET /health
```

返回：

```json
{
  "status": "ok",
  "service": "insight-os-api"
}
```

### 13.2 Service 分层

路由层只处理请求和响应。业务逻辑放入 services：

- `ai_service.py`：AI 调用与结构化返回
- `trend_service.py`：热点统计
- `idea_service.py`：选题生成
- `report_service.py`：周报生成
- `collector_service.py`：采集与导入

---

## 14. Prompt 文件要求

所有 Prompt 必须独立存放在：

```text
packages/prompts/
```

代码不得把品牌调性、评分标准和输出格式写死。

每个 Prompt 需要明确：

- 输入变量
- 输出 JSON Schema
- 判断标准
- 禁止事项
- 示例输出

---

## 15. 第一版验收标准

MVP 完成后，应支持：

- 手动导入 20 条竞品内容
- 自动生成摘要和标签
- 自动判断适合 in77 / in88
- 自动生成 5 条 in77 选题
- 自动生成 5 条 in88 选题
- 自动生成一份 Markdown 周报
- 可以在网页端查看内容库、选题库和周报
- 周报中每个建议都能追溯到参考内容或趋势依据

---

## 16. 注意事项

1. 小红书和微信公众号采集必须使用合规方式。
2. 第一版不强求完全自动抓取，允许人工导入链接或表格。
3. AI 输出必须结构化，方便前端展示。
4. 所有 Prompt 独立存放，方便后续调整。
5. 品牌调性不要写死在代码里，要放在配置文件中。
6. 周报先做 Markdown，后续再做 PDF / PPT。
7. MVP 重点不是“全自动”，而是先跑通内容分析闭环。
8. AI 生成内容必须保留来源依据，关键事实需要人工复核。
9. 所有时间字段统一使用 ISO 格式。
10. 项目命名统一使用 `INSight OS`，代码仓库使用 `insight-os`。

---

## 17. 最小可运行版本定义

只要下面这条链路跑通，INSight OS V1.0 就成立：

```text
用户导入竞品内容
        ↓
AI 摘要、标签、评分
        ↓
系统沉淀到内容库
        ↓
AI 生成热点分析
        ↓
AI 生成 in77 / in88 选题
        ↓
AI 生成周报
```

第一版的真正价值不是功能数量，而是让内容团队每周能稳定拿到一份有依据、可讨论、可执行的内容提报。
