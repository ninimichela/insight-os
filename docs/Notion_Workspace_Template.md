# INSight OS｜Notion Workspace Template V1.0

**AI Content Intelligence System**  
for 北京 in77 & 北京 in88

| 项目 | 内容 |
| --- | --- |
| 产品代号 | INSight OS |
| 文档类型 | Notion Workspace 模板说明 |
| Version | 1.0 |
| Owner | Michelle Ni |
| Created | 2026 |
| 核心用途 | 内容库、竞品库、趋势库、选题池、排期、周报、品牌记忆 |

---

## 0. Workspace 总结构

建议整个 Notion Workspace 分成八个核心数据库。

```text
🏠 INSight OS

├── 📚 Content Library
├── 🏬 Competitor Library
├── 💡 Idea Pool
├── 📈 Trend Center
├── 🗓 Content Calendar
├── 🤝 Brand Library
├── 📖 Weekly Reports
└── ⚙ Settings
```

V2 增加：

```text
└── 🧬 Brand Brain Database
```

---

## 1. Dashboard 首页

首页不要直接堆数据库，而是做成每日工作台。

### 1.1 首页标题

```text
👋 Good Morning Michelle
```

### 1.2 顶部数据卡片

| 指标 | 示例 |
| --- | --- |
| 今日新增 | 18 |
| 本周热点 | Citywalk |
| 竞品更新 | 12 |
| 推荐选题 | 8 |

### 1.3 快捷入口

四个主按钮：

- 📚 Content
- 💡 Ideas
- 📈 Trends
- 📖 Reports

### 1.4 今日推荐区

展示 AI 推荐的高优先级选题。

示例：

```text
🔥 今日推荐

★★★★★
CBD今天最好坐的一张椅子
```

点击后进入对应 Idea 页面，可查看推荐理由、参考案例、趋势依据和执行建议。

---

## 2. Database 01：📚 Content Library

Content Library 是整个系统最大的数据库。所有公众号、小红书、新闻、媒体、商业资讯、竞品内容都进入这里。

### 2.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 标题 | Title | 内容标题 |
| 来源 | Select | 如 北京LOOK、赢商网、小红书博主 |
| 平台 | Select | 公众号、小红书、新闻、微博、其他 |
| 发布时间 | Date | 原始发布时间 |
| 竞品 | Relation | 关联 Competitor Library |
| 城市 | Select | 北京、上海、杭州、成都等 |
| 分类 | Multi-select | 商业地产、生活方式、艺术、餐饮、科技等 |
| 关键词 | Multi-select | AI 提取关键词 |
| 摘要 | Text | AI 摘要 |
| AI标签 | Multi-select | AI 自动标签 |
| 适合平台 | Multi-select | 公众号、小红书、朋友圈、视频 |
| 参考价值 | Number | 0-100 |
| 执行成本 | Select | 低、中、高 |
| AI建议 | Text | 可借鉴点和建议 |
| 链接 | URL | 原文链接 |
| 封面 | Files | 封面图 |
| AI分析状态 | Status | 未分析、已分析、需要复核 |
| 是否采用 | Checkbox | 是否进入选题或排期 |

### 2.2 推荐视图

| View | 说明 |
| --- | --- |
| All | 全部内容 |
| 今天新增 | 今日采集内容 |
| 本周新增 | 最近 7 天内容 |
| in77 | 适合 in77 的内容 |
| in88 | 适合 in88 的内容 |
| 高价值 | 参考价值 ≥ 80 |
| 未分析 | AI分析状态 = 未分析 |
| 已采用 | 是否采用 = YES |

### 2.3 使用方式

每天采集或导入内容后，先进入 Content Library。AI 分析后，内容会被打标签、评分，并推荐是否进入 Idea Pool。

---

## 3. Database 02：🏬 Competitor Library

Competitor Library 只放项目、媒体和重点账号。

### 3.1 示例对象

- 北京 SKP
- THE BOX
- 北京坊
- 北京 LOOK
- 北京 DT51
- 三里屯太古里
- 798
- 檀谷
- 郎园

### 3.2 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 名称 | Title | 竞品或媒体名称 |
| 城市 | Select | 北京、上海、杭州、成都 |
| 类型 | Select | 媒体、商业项目、艺术空间、街区、品牌 |
| 账号 | URL | 官方账号或主页 |
| 更新频率 | Select | 高频、中频、低频 |
| 调性 | Multi-select | 高端、年轻、潮流、艺术、生活方式等 |
| 内容方向 | Multi-select | 餐饮、展览、活动、Citywalk 等 |
| 值得学习 | Text | 可借鉴点 |
| 优先级 | Number | 1-5 |
| AI评分 | Number | 0-100 |

### 3.3 推荐视图

| View | 说明 |
| --- | --- |
| 北京 | 北京竞品 |
| 上海 | 上海竞品 |
| 杭州 | 杭州竞品 |
| 成都 | 成都竞品 |
| 媒体 | 城市媒体与行业媒体 |
| 商业项目 | 商业地产项目 |
| 高优先级 | 优先级 ≥ 4 |

---

## 4. Database 03：💡 Idea Pool

Idea Pool 是以后每天最常看的地方。每一条都是 AI 生成或人工补充的选题。

### 4.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 标题 | Title | 选题标题 |
| 适合项目 | Select | in77、in88、山每、其他 |
| 栏目 | Select | 项目栏目 |
| 内容方向 | Select | Citywalk、餐饮、艺术、科技等 |
| 推荐理由 | Text | 为什么值得做 |
| 优先级 | Number | 1-5 或 0-100 |
| 参考案例 | Relation | 关联 Content Library |
| 关联热点 | Relation | 关联 Trend Center |
| 发布时间 | Date | 建议发布时间 |
| 状态 | Status | 待讨论、已采用、已发布、废弃 |

### 4.2 状态

- 待讨论
- 已采用
- 已发布
- 废弃

### 4.3 推荐视图

| View | 说明 |
| --- | --- |
| in77 | 适合 in77 的选题 |
| in88 | 适合 in88 的选题 |
| 本周 | 本周建议执行 |
| 高优先级 | 优先级 ≥ 4 |
| 待讨论 | 内容会待评估 |
| 已采用 | 已进入排期 |

---

## 5. Database 04：📈 Trend Center

Trend Center 每天自动更新，用来保存热点、趋势和话题生命周期。

### 5.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 热点 | Title | 热点名称 |
| 来源 | Multi-select | 公众号、小红书、新闻、竞品等 |
| 增长率 | Number | 话题增长速度 |
| 生命周期 | Select | 上升期、高峰期、衰退期、过时 |
| 推荐指数 | Number | 0-100 |
| 是否建议跟 | Checkbox | 是否建议 in77 / in88 跟进 |
| AI分析 | Text | AI 趋势判断 |
| 关联内容 | Relation | 关联 Content Library |

### 5.2 推荐视图

| View | 说明 |
| --- | --- |
| 今日 | 过去 24 小时 |
| 7天 | 过去 7 天 |
| 30天 | 过去 30 天 |
| 值得跟 | 是否建议跟 = YES |
| 上升期 | 生命周期 = 上升期 |

---

## 6. Database 05：🗓 Content Calendar

Content Calendar 用于内容排期。

### 6.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 日期 | Date | 计划发布时间 |
| 标题 | Title | 内容标题 |
| 项目 | Select | in77、in88、山每 |
| 平台 | Multi-select | 公众号、小红书、朋友圈、视频 |
| 负责人 | Person | 内容负责人 |
| 状态 | Status | 策划、制作、审核、已发布 |
| 对应Idea | Relation | 关联 Idea Pool |

### 6.2 状态

- 策划
- 制作
- 审核
- 已发布

### 6.3 推荐视图

- Calendar View：按月查看七月、八月、九月等内容排期。
- Board View：按状态查看内容生产流程。
- Table View：查看全部排期。

---

## 7. Database 06：🤝 Brand Library

Brand Library 是初期 Brand Brain 的基础。这里保存项目和品牌的调性资料。

### 7.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 品牌 | Title | 品牌或项目名称 |
| 所属项目 | Select | in77、in88、山每 |
| 调性 | Text | 品牌语气和内容风格 |
| 禁用词 | Text | 不建议使用的表达 |
| 关键词 | Multi-select | 核心关键词 |
| 合作案例 | Relation | 关联 Content Library 或 Idea Pool |
| 图片风格 | Text | 视觉表达要求 |
| 代表栏目 | Text | 常用栏目 |

### 7.2 示例

in77：

- CBD
- 公园
- 艺术
- 松弛
- 城市生活

in88：

- 科技
- 年轻
- 动漫
- 王府井
- 室内漫游

### 7.3 使用方式

AI 生成选题和文案前，先读取 Brand Library，避免生成通用内容。

---

## 8. Database 07：📖 Weekly Reports

Weekly Reports 保存所有周报。

### 8.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 标题 | Title | 周报标题 |
| 日期 | Date | 周报生成日期 |
| 热点 | Relation | 关联 Trend Center |
| 案例 | Relation | 关联 Content Library |
| 选题 | Relation | 关联 Idea Pool |
| PDF | Files | PDF 文件 |
| 状态 | Status | 草稿、已完成、已归档 |

### 8.2 推荐视图

| View | 说明 |
| --- | --- |
| 2026 | 2026 年周报 |
| 2027 | 2027 年周报 |
| 已完成 | 状态 = 已完成 |
| 草稿 | 状态 = 草稿 |

---

## 9. Database 08：⚙ Settings

Settings 不给普通用户看，用于管理系统配置。

### 9.1 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 配置项 | Title | 配置名称 |
| 类型 | Select | Prompt、Brand、AI模型、评分规则、数据源 |
| 当前版本 | Text | 版本号 |
| 内容 | Text | 配置内容 |
| 是否启用 | Checkbox | 是否启用 |
| 更新日期 | Date | 最近更新时间 |

### 9.2 示例配置项

- Prompt版本
- Brand版本
- AI模型
- 评分规则
- 数据源列表
- 关键词列表

### 9.3 使用方式

后续可以直接修改 Settings，不需要改代码。

---

## 10. 数据关联关系

Notion 结构最重要的是 Relation。

核心关系链：

```text
Content Library
        ↓
Trend Center
        ↓
Idea Pool
        ↓
Content Calendar
        ↓
Weekly Reports
```

### 10.1 关系说明

| 起点 | 终点 | 关系 |
| --- | --- | --- |
| Content Library | Competitor Library | 内容来自哪个竞品或媒体 |
| Content Library | Trend Center | 哪些内容支撑某个热点 |
| Trend Center | Idea Pool | 哪些热点生成了某个选题 |
| Content Library | Idea Pool | 哪些案例启发了某个选题 |
| Idea Pool | Content Calendar | 哪些选题进入排期 |
| Idea Pool | Weekly Reports | 哪些选题进入周报 |
| Trend Center | Weekly Reports | 哪些热点进入周报 |
| Content Library | Weekly Reports | 哪些案例进入周报 |

### 10.2 为什么重要

每一个选题都能追溯：

- 来自哪篇案例
- 来自哪个热点
- 来自哪个竞品
- 为什么值得做
- 后续是否采用

领导问“为什么推荐这个”，可以直接点进去看到来源和依据。

---

## 11. V2：🧬 Brand Brain Database

V2 建议增加一个核心数据库：Brand Brain Database。

它不是普通品牌资料库，而是品牌知识图谱。

### 11.1 目标

记录每个品牌或项目的长期内容记忆，让 AI 每次生成内容前先读取品牌知识，而不是只依赖固定 Prompt。

### 11.2 字段设计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| 品牌 / 项目 | Title | in77、in88、山每等 |
| 品牌定位 | Text | 项目定位 |
| 内容调性 | Text | 文案与表达方式 |
| 禁用表达 | Text | 禁用词和不建议使用的表达 |
| 常用栏目 | Multi-select | 固定栏目 |
| 高阅读历史内容 | Relation | 关联 Content Library |
| 高收藏历史内容 | Relation | 关联 Content Library |
| 图片风格 | Text | 视觉风格 |
| 标题风格 | Text | 标题结构与常用句式 |
| 合作品牌偏好 | Multi-select | 适合合作的品牌类型 |
| 用户画像 | Text | 目标客群 |
| KPI偏好 | Multi-select | 阅读、收藏、到店、会员转化等 |
| 内容比例 | Text | 80% 品牌 DNA / 20% 创新 |
| 最近更新 | Date | 最近更新时间 |

### 11.3 使用方式

AI 每次生成内容前，先读取 Brand Brain Database：

```text
用户请求
  ↓
读取 Brand Brain
  ↓
读取 Prompt
  ↓
生成内容
```

这样，同一个 Prompt 会因为品牌不同而输出完全不同的结果。

### 11.4 长期价值

Notion 不只是临时数据库，而会成为 INSight OS 的长期知识库和品牌记忆中心。

未来迁移到网页版时，这套结构可以一比一迁移到 PostgreSQL 或其他数据库，不需要重新设计。

---

## 12. MVP 搭建顺序

建议按以下顺序搭建 Notion：

1. 建立 Dashboard 首页。
2. 建立 Content Library。
3. 建立 Competitor Library。
4. 建立 Trend Center。
5. 建立 Idea Pool。
6. 建立 Content Calendar。
7. 建立 Weekly Reports。
8. 建立 Brand Library。
9. 建立 Settings。
10. 配置 Relation。
11. 创建 Views。
12. 导入第一批测试内容。

---

## 13. 第一批测试数据建议

为了让系统尽快跑起来，建议先导入：

- 20 条竞品内容
- 10 条商业资讯
- 10 条小红书内容
- 5 个竞品项目
- 2 个品牌项目：in77、in88
- 10 条 AI 生成选题

这样可以立即测试：

- 内容入库
- 标签分类
- 趋势归纳
- 选题生成
- 周报关联

---

## 14. 一句话总结

Notion Workspace 是 INSight OS 的第一版操作系统。

它先承接内容、竞品、热点、选题和周报，再逐步沉淀为品牌记忆中心。等未来迁移到网页产品时，这套数据库结构可以直接成为后端数据模型的原型。
