# INSight OS｜Core Engine Design V1.0

**AI Content Operating System for Commercial Real Estate**  
for 北京 in77 & 北京 in88

| 项目 | 内容 |
| --- | --- |
| 产品代号 | INSight OS |
| 文档类型 | Core Engine Design |
| Version | 1.0 |
| Owner | Michelle Ni |
| Created | 2026 |
| 核心模块 | Brand Brain / Scoring Engine / Workflow Engine / Memory Layer |

---

## 0. 更大的产品定位

INSight OS 不应被定义为一个 AI 工具。

更准确的定位是：

**AI Content Operating System for Commercial Real Estate**

即：

**面向商业地产的 AI 内容操作系统。**

它不是只服务 in77 和 in88。未来任何商业地产项目，只要替换 Brand Brain，就可以使用同一套系统。

```text
同一套系统
    +
不同 Brand Brain
    ↓
不同项目内容策略
```

这意味着 INSight OS 的核心资产不是 Prompt，也不是某一次 GPT 输出，而是：

- Brand Brain
- Scoring Engine
- Workflow Engine
- Memory Layer
- Performance Feedback

---

## 1. 第五份：Brand Brain Design

### 1.1 Brand Brain 是什么

Brand Brain 是整个系统真正的核心。

它回答一个问题：

**AI 为什么知道 in77 应该怎么写？**

答案不是因为 Prompt 写得长，而是因为 AI 在生成前先读取 Brand Brain。

普通 AI：

```text
Prompt
  ↓
GPT
  ↓
输出
```

INSight OS：

```text
用户需求
  ↓
Brand Brain
  ↓
Prompt Composer
  ↓
GPT
  ↓
结构化输出
```

### 1.2 Brand Brain 的设计原则

1. 品牌信息不写死在 Prompt 里。
2. 品牌信息存入数据库，可持续更新。
3. AI 每次生成前，自动读取品牌定位、历史表现和风格规则。
4. 同一个 Prompt，面对不同 Brand Brain，会生成不同内容。

### 1.3 in77 Brand Brain 示例

```text
项目：in77

定位：
CBD 城市公园商业

关键词：
城市
自然
艺术
开放
松弛
CBD
公园

禁用词：
最低价
爆款
疯抢
秒杀
全城最低

喜欢标题：
城市观察
今天适合
夏天是一种
CBD今天
北京今天最舒服的

图片风格：
Monocle
Popeye
城市杂志感
自然光
低饱和

历史高阅读：
从 Content Library 和 Performance Database 自动读取
```

### 1.4 in88 Brand Brain 示例

```text
项目：in88

定位：
王府井年轻生活方式与科技潮流商业项目

关键词：
王府井
科技
动漫
年轻
室内漫游
潮流
生活方式

禁用词：
传统百货
甩卖
清仓
疯抢
老派商场话术

喜欢标题：
今天别急着回家
室内漫游计划
漫画里的夏天
年轻人的电玩城
王府井新鲜事

图片风格：
明亮
潮流
动线感
IP感
年轻场景

历史高阅读：
从 Content Library 和 Performance Database 自动读取
```

### 1.5 Brand Brain 字段结构

| 字段 | 说明 |
| --- | --- |
| brand_id | 品牌或项目 ID |
| brand_name | 品牌名称 |
| positioning | 品牌定位 |
| keywords | 核心关键词 |
| avoid_words | 禁用词 |
| preferred_titles | 喜欢的标题结构 |
| copy_tone | 文案语气 |
| visual_style | 图片风格 |
| content_columns | 常用栏目 |
| audience_profile | 用户画像 |
| brand_partners | 合作品牌偏好 |
| high_performance_content | 历史高表现内容 |
| low_performance_content | 历史低表现内容 |
| kpi_preference | KPI 偏好 |
| content_ratio | 80% 品牌 DNA / 20% 创新 |

### 1.6 Brand Brain 在系统中的作用

AI 生成内容前，必须先读取：

- 品牌定位
- 禁用词
- 标题风格
- 图片风格
- 历史高阅读
- 历史高收藏
- 栏目表现
- 合作品牌偏好

然后再进入 Prompt。

这使 AI 不是“直接生成”，而是“基于品牌记忆生成”。

---

## 2. 第六份：Scoring Engine

### 2.1 Scoring Engine 是什么

Scoring Engine 是 INSight OS 的内容判断系统。

它解决的问题是：

过去：

```text
我觉得这个不错。
```

未来：

```text
综合分 92。
建议：立即执行。
理由：创新高、品牌契合高、执行成本可控、收藏潜力强。
```

### 2.2 评分维度

AI 看到一篇内容或一个选题后，自动评分。

| 维度 | 说明 | 分值 |
| --- | --- | --- |
| 创新 | 是否有新鲜角度 | 1-5 |
| 品牌契合 | 是否符合 in77 / in88 Brand Brain | 1-5 |
| 执行成本 | 是否容易拍摄、写作和落地 | 1-5 |
| 传播潜力 | 是否适合平台传播 | 1-5 |
| 收藏潜力 | 是否具有攻略、清单、路线价值 | 1-5 |
| 热点相关 | 是否贴合当前热点 | 1-5 |
| 时效性 | 是否适合现在发布 | 1-5 |

### 2.3 综合评分逻辑

建议采用加权评分。

```text
综合分 =
创新 × 15%
+ 品牌契合 × 25%
+ 执行成本 × 10%
+ 传播潜力 × 20%
+ 收藏潜力 × 15%
+ 热点相关 × 10%
+ 时效性 × 5%
```

换算为 0-100 分。

### 2.4 输出示例

```json
{
  "title": "CBD今天最好坐的一张椅子",
  "scores": {
    "innovation": 5,
    "brand_fit": 5,
    "execution_cost": 4,
    "spread_potential": 4,
    "save_potential": 5,
    "trend_relevance": 5,
    "timeliness": 5
  },
  "overall_score": 92,
  "recommendation": "立即执行",
  "reason": "该选题符合 in77 城市、公园、松弛的品牌方向，同时具备小红书收藏价值和低成本拍摄条件。"
}
```

### 2.5 推荐动作

| 综合分 | 动作 |
| --- | --- |
| 90-100 | 立即执行 |
| 80-89 | 本周优先讨论 |
| 70-79 | 可作为备选 |
| 60-69 | 暂缓 |
| 60 以下 | 不建议执行 |

### 2.6 Scoring Engine 的价值

它让内容判断从主观经验变成有依据的系统判断。

每一个推荐都能解释：

- 为什么推荐
- 为什么适合这个项目
- 为什么现在做
- 为什么比另一个选题优先

---

## 3. 第七份：Workflow Engine

### 3.1 Workflow Engine 是什么

Workflow Engine 是整个系统的自动化大脑。

它负责任务何时发生、如何流转、输出到哪里。

### 3.2 每日自动流程

```text
08:00
开始采集
  ↓
AI 分析
  ↓
热点生成
  ↓
选题生成
  ↓
推送到 Notion
  ↓
推送到 Slack / 企业微信
  ↓
结束
```

### 3.3 每周自动流程

```text
每周五 10:00
读取过去 7 天内容
  ↓
生成热点排行
  ↓
生成竞品分析
  ↓
生成 in77 选题 ×5
  ↓
生成 in88 选题 ×5
  ↓
生成周报 Markdown / PDF
  ↓
写入 Weekly Reports
  ↓
推送给团队
```

### 3.4 Workflow 节点设计

| 节点 | 作用 |
| --- | --- |
| Trigger | 定时触发或手动触发 |
| Collector | 采集或导入内容 |
| Dedup | 去重 |
| AI Analyzer | 摘要、标签、评分 |
| Trend Engine | 热点识别 |
| Idea Engine | 选题生成 |
| Scoring Engine | 选题评分 |
| Report Generator | 周报生成 |
| Notion Writer | 写入 Notion |
| Notification | 推送 Slack / 企业微信 |

### 3.5 MVP 实现方式

第一阶段可以用 n8n 实现：

- Cron Trigger
- HTTP Request
- OpenAI Node
- Notion Node
- Slack / 企业微信 Webhook

后续如果做独立后台，可以迁移到：

- Celery
- Temporal
- Cloud Tasks
- GitHub Actions

### 3.6 Workflow Engine 的价值

它让 INSight OS 不需要每天手动点击。

系统每天自己完成：

- 看市场
- 看竞品
- 看热点
- 做判断
- 给选题
- 生成周报

---

## 4. Memory Layer 内容记忆层

### 4.1 Memory Layer 是什么

Memory Layer 是 INSight OS 最有价值的长期能力之一。

普通 AI：

```text
今天分析
今天结束
```

INSight OS：

```text
去年
今年
去年七夕
去年夏天
去年世界杯
全部知道
```

### 4.2 示例

当 AI 生成“今年七夕”选题时，系统会自动搜索：

- 去年七夕 in77 发过什么
- 去年七夕 in88 发过什么
- 阅读多少
- 收藏多少
- 评论关键词是什么
- 哪些内容有效
- 哪些内容不应重复

然后输出：

```text
今年不要重复去年的情侣路线合集。

建议升级为：
“一个人也可以过七夕的城市计划”

理由：
去年情侣向内容阅读中等，但评论区出现大量“一个人也想出去”的反馈。
```

这就是真正的 Content Memory。

### 4.3 Memory Layer 记录内容

Memory Layer 不只是存原始内容，而是存内容经验：

- 栏目
- 表现
- 成功原因
- 失败原因
- 用户反馈
- 评论关键词
- 节点复盘
- 不要重复的旧选题
- 可以升级的旧选题

---

## 5. V2 新增数据库

除了 Brand Brain Database，V2 建议新增两个核心数据库：

- 🧠 Memory Database
- 📊 Performance Database

---

## 6. 🧠 Memory Database

Memory Database 不是存内容原文，而是存内容经验。

### 6.1 字段设计

| 字段 | 说明 |
| --- | --- |
| memory_id | 记忆 ID |
| project | in77 / in88 |
| memory_type | 栏目、节点、失败原因、成功原因、评论洞察 |
| related_topic | 相关话题 |
| related_date | 相关日期或节点 |
| related_content | 关联内容 |
| insight | 记忆内容 |
| recommendation | 未来建议 |
| avoid_repeat | 是否避免重复 |
| reusable | 是否可复用 |
| confidence | 置信度 |
| updated_at | 更新时间 |

### 6.2 示例

```json
{
  "project": "in77",
  "memory_type": "节点复盘",
  "related_topic": "七夕",
  "related_date": "2025-08",
  "insight": "情侣路线合集阅读中等，但评论区出现单人友好需求。",
  "recommendation": "2026 年七夕可尝试一个人也可以过七夕的城市计划。",
  "avoid_repeat": true,
  "reusable": true,
  "confidence": 0.82
}
```

### 6.3 作用

Memory Database 让 AI 越用越懂：

- 什么内容适合某个项目
- 哪些栏目值得保留
- 哪些节点不要重复
- 哪些失败可以避免
- 哪些评论反馈值得放大

---

## 7. 📊 Performance Database

Performance Database 用来记录内容发布后的真实表现。

### 7.1 字段设计

| 字段 | 说明 |
| --- | --- |
| performance_id | 表现数据 ID |
| project | in77 / in88 |
| platform | 公众号、小红书、视频、朋友圈 |
| content_id | 关联内容 |
| idea_id | 关联选题 |
| publish_date | 发布时间 |
| reads | 阅读 |
| likes | 点赞 |
| saves | 收藏 |
| comments | 评论 |
| shares | 分享 |
| engagement_rate | 互动率 |
| comment_keywords | 评论关键词 |
| kpi_result | KPI 结果 |
| updated_at | 更新时间 |

### 7.2 示例

```json
{
  "project": "in88",
  "platform": "小红书",
  "idea_id": "idea_001",
  "publish_date": "2026-07-07",
  "reads": 18500,
  "likes": 920,
  "saves": 430,
  "comments": 86,
  "shares": 120,
  "engagement_rate": 0.084,
  "comment_keywords": ["高达", "王府井", "周末", "想去"],
  "kpi_result": "高收藏，高到店意图"
}
```

### 7.3 反向更新 Brand Brain

Performance Database 不只是复盘，它会反向更新 Brand Brain。

```text
内容发布
  ↓
表现数据回收
  ↓
Performance Database
  ↓
Memory Database
  ↓
Brand Brain 更新
  ↓
下一次 AI 更准
```

### 7.4 作用

Performance Database 让系统从“会生成”变成“会学习”。

---

## 8. Core Engine 总架构

```text
Data Collector
      ↓
Content Library
      ↓
AI Analyzer
      ↓
Trend Engine
      ↓
Brand Brain
      ↓
Idea Engine
      ↓
Scoring Engine
      ↓
Content Generator
      ↓
Workflow Engine
      ↓
Weekly Report / Notion / Slack
      ↓
Performance Database
      ↓
Memory Layer
      ↓
Brand Brain 更新
```

---

## 9. V1 / V2 / V3 路线

### V1：跑通闭环

- 内容导入
- AI 分析
- 趋势识别
- 选题生成
- 周报输出
- 基础 Brand Library
- 基础评分

### V2：建立品牌大脑和内容记忆

- Brand Brain Database
- Memory Database
- Performance Database
- Prompt Composer
- 自动读取品牌 DNA
- 避免重复选题

### V3：成为可复用商业地产内容 OS

- 多项目 Brand Brain
- 多城市商业项目适配
- 自动表现回流
- 自动内容策略升级
- 可部署给不同商业地产客户

---

## 10. 一句话总结

Brand Brain 决定 AI 是否懂品牌。

Scoring Engine 决定 AI 是否会判断。

Workflow Engine 决定 AI 是否能自动运行。

Memory Layer 决定 AI 是否会越来越聪明。

这四层加起来，才让 INSight OS 从一个 AI 工具变成真正的商业地产内容操作系统。
