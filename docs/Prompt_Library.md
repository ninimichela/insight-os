# INSight OS｜Prompt Library V1.0

**AI Content Intelligence System**  
for 北京 in77 & 北京 in88

| 项目 | 内容 |
| --- | --- |
| 产品代号 | INSight OS |
| 文档类型 | Prompt Library |
| Version | 1.0 |
| Owner | Michelle Ni |
| Created | 2026 |
| Prompt 数量 | 36 个核心 Prompt + 2 个共享规范文件 |

---

## 0. 设计原则

Prompt Library 不是越多越好，而是每一个 Prompt 都必须职责唯一。

INSight OS 的 Prompt 设计原则：

1. 一个 Prompt 只做一件事。
2. 所有 Prompt 统一输入和输出规范。
3. 所有 Prompt 输出结构化 JSON，方便前端渲染和数据库保存。
4. 所有 Prompt 必须引用输入依据，不能杜撰。
5. 品牌调性不写死在 Prompt 里，由 Brand Brain 动态加载。
6. 写作类 Prompt 不能直接生成通用内容，必须先读取品牌 DNA。

---

## 1. Prompt 总目录

```text
packages/prompts/
├── analysis/
│   ├── summarize_content.md
│   ├── tag_content.md
│   ├── extract_keywords.md
│   ├── detect_city.md
│   ├── detect_category.md
│   ├── extract_brands.md
│   ├── analyze_visual_style.md
│   └── analyze_copy_style.md
│
├── competitor/
│   ├── competitor_analysis.md
│   ├── competitor_score.md
│   ├── competitor_compare.md
│   └── weekly_competitor_summary.md
│
├── trend/
│   ├── trend_analysis.md
│   ├── trend_cluster.md
│   ├── trend_prediction.md
│   └── topic_growth.md
│
├── idea/
│   ├── generate_ideas.md
│   ├── expand_outline.md
│   ├── generate_series.md
│   ├── recommend_brands.md
│   └── recommend_visuals.md
│
├── writing/
│   ├── wechat_article.md
│   ├── xiaohongshu.md
│   ├── moments.md
│   ├── video_script.md
│   └── poster_copy.md
│
├── reports/
│   ├── weekly_report.md
│   ├── monthly_report.md
│   └── ppt_outline.md
│
├── style/
│   ├── style_in77.md
│   ├── style_in88.md
│   ├── style_same.md
│   ├── style_monocle.md
│   ├── style_popeye.md
│   └── style_andpremium.md
│
└── shared/
    ├── system_prompt.md
    ├── json_schema.md
    └── rules.md
```

说明：

- 36 个核心 Prompt：除 `json_schema.md` 和 `rules.md` 外，其余均为可调用 Prompt。
- 2 个共享规范文件：`json_schema.md` 和 `rules.md` 用于约束所有 Prompt 的输出格式和行为规则。

---

## 2. 统一 Prompt 规范

所有 Prompt 统一采用以下结构：

```md
# Role

你是一名商业地产内容策略总监。

---

# Goal

说明这个 Prompt 唯一要完成的任务。

---

# Input

输入字段：
- title
- body
- platform
- source
- publish_time
- brand_profile
- reference_cases

---

# Output

必须输出 JSON。

---

# Rules

- 不能杜撰。
- 不能夸张。
- 必须引用依据。
- 不要生成与输入无关的信息。
- 不要使用空泛商业话术。
- 如果信息不足，返回 `insufficient_information: true`。
```

---

## 3. 第一层：Analysis

负责理解内容。

输入一篇公众号、小红书、新闻或竞品内容后，输出摘要、标签、品牌、栏目、关键词、城市、品类、文案风格和视觉风格。

### 3.1 summarize_content.md

**职责：** 提炼内容摘要。

输入：

- 标题
- 正文
- 来源
- 发布时间

输出：

```json
{
  "summary_30": "30字摘要",
  "summary_100": "100字摘要",
  "key_points": ["要点1", "要点2", "要点3"],
  "source_evidence": ["依据1", "依据2"]
}
```

### 3.2 tag_content.md

**职责：** 为内容自动打标签。

输出：

```json
{
  "tags": ["Citywalk", "艺术展", "夏天"],
  "primary_tag": "Citywalk",
  "confidence": 0.86,
  "source_evidence": ["依据"]
}
```

### 3.3 extract_keywords.md

**职责：** 提取关键词。

输出：

```json
{
  "keywords": ["王府井", "室内漫游", "艺术展"],
  "people_keywords": ["年轻人", "亲子"],
  "place_keywords": ["王府井", "CBD"],
  "event_keywords": ["快闪", "展览"]
}
```

### 3.4 detect_city.md

**职责：** 判断内容关联城市与商圈。

输出：

```json
{
  "city": "北京",
  "district": "东城",
  "business_area": "王府井",
  "confidence": 0.9
}
```

### 3.5 detect_category.md

**职责：** 判断内容类别。

候选类别：

- 商业地产
- 生活方式
- 艺术
- 品牌
- 科技
- 餐饮
- 运动
- 城市更新
- 快闪
- IP
- 音乐
- 展览

输出：

```json
{
  "category": "生活方式",
  "sub_category": "Citywalk",
  "is_commercial_relevant": true,
  "reason": "内容提到商场、路线和到店消费。"
}
```

### 3.6 extract_brands.md

**职责：** 提取内容中出现的品牌、项目和机构。

输出：

```json
{
  "brands": ["LEGO", "高达"],
  "commercial_projects": ["北京SKP", "三里屯太古里"],
  "media_accounts": ["北京LOOK"],
  "institutions": ["东城区文旅局"]
}
```

### 3.7 analyze_visual_style.md

**职责：** 分析内容视觉风格。

输出：

```json
{
  "visual_style": "街拍感、自然光、低饱和",
  "cover_type": "人物场景图",
  "image_suggestion": "适合借鉴为小红书封面",
  "reference_value": 85
}
```

### 3.8 analyze_copy_style.md

**职责：** 分析文案表达方式。

输出：

```json
{
  "copy_style": "口语化、清单式、生活方式表达",
  "title_pattern": "场景 + 情绪 + 地点",
  "tone": "轻松、克制、有城市感",
  "reference_value": 88
}
```

---

## 4. 第二层：Competitor

负责竞品内容分析。

### 4.1 competitor_analysis.md

**职责：** 分析单个竞品最近内容表现。

输入：

- 竞品名称
- 最近 7 天内容

输出：

```json
{
  "competitor": "北京LOOK",
  "content_directions": ["Citywalk", "餐饮", "展览"],
  "columns": ["周末去哪", "新店"],
  "hot_topics": ["夏天", "夜生活"],
  "tone": "城市生活方式",
  "visual_style": "真实街拍、轻杂志感",
  "learnable_points": ["标题场景化", "路线清单化"]
}
```

### 4.2 competitor_score.md

**职责：** 为竞品评分。

输出：

```json
{
  "competitor": "北京SKP",
  "publish_frequency": 5,
  "engagement": 4,
  "innovation": 4,
  "visual_quality": 5,
  "reference_value": 5,
  "overall_score": 92,
  "recommendation": "值得重点参考"
}
```

### 4.3 competitor_compare.md

**职责：** 对比多个竞品的内容策略。

输出：

```json
{
  "summary": "三里屯太古里偏潮流，SKP偏高端审美，THE BOX偏年轻社群。",
  "differences": [
    {
      "competitor": "THE BOX",
      "strength": "年轻社群表达",
      "weakness": "内容延展依赖活动"
    }
  ],
  "opportunities_for_in88": ["科技动漫内容可做差异化"],
  "opportunities_for_in77": ["CBD松弛生活方式可持续化"]
}
```

### 4.4 weekly_competitor_summary.md

**职责：** 生成每周竞品总结。

输出：

```json
{
  "week_summary": "本周竞品集中在夏日活动、Citywalk、艺术展。",
  "top_cases": [],
  "worth_learning": [],
  "avoid": [],
  "recommendations": []
}
```

---

## 5. 第三层：Trend

负责识别热点与趋势。

### 5.1 trend_analysis.md

**职责：** 分析过去 7 天热点。

输出：

```json
{
  "top_10": [
    {
      "topic": "Citywalk",
      "score": 95,
      "reason": "跨公众号和小红书高频出现。"
    }
  ]
}
```

### 5.2 trend_cluster.md

**职责：** 将相似热点聚类。

输出：

```json
{
  "clusters": [
    {
      "cluster_name": "夏日城市漫游",
      "topics": ["Citywalk", "夜经济", "草坪", "咖啡"],
      "content_count": 24
    }
  ]
}
```

### 5.3 trend_prediction.md

**职责：** 预测下周可跟进热点。

输出：

```json
{
  "predictions": [
    {
      "topic": "夜经济",
      "probability": 0.82,
      "why": "天气升温、暑期开始、夜间消费增加。",
      "recommended_for": ["in77", "in88"]
    }
  ]
}
```

### 5.4 topic_growth.md

**职责：** 判断话题增长速度和生命周期。

输出：

```json
{
  "topic": "漫画",
  "growth_rate": 0.42,
  "lifecycle": "上升期",
  "should_follow": true,
  "reason": "近期展览和动漫 IP 活动增多。"
}
```

---

## 6. 第四层：Idea

负责生成选题，是 INSight OS 最重要的一层。

### 6.1 generate_ideas.md

**职责：** 生成项目选题。

输入：

- 热点
- 品牌 DNA
- 竞品案例
- 天气 / 节气 / 城市节点

输出：

```json
{
  "project": "in88",
  "ideas": [
    {
      "title": "室内漫游计划",
      "angle": "用避暑场景包装商场动线",
      "platforms": ["小红书", "公众号"],
      "priority": 5,
      "reason": "高温天气下室内场景有真实需求。"
    }
  ]
}
```

### 6.2 expand_outline.md

**职责：** 将选题扩展为内容大纲。

输出：

```json
{
  "title": "室内漫游计划",
  "outline": ["开头场景", "路线一", "品牌点位", "互动结尾"],
  "key_message": "今天不想晒太阳，就去王府井室内漫游。"
}
```

### 6.3 generate_series.md

**职责：** 将单个选题扩展为栏目系列。

输出：

```json
{
  "series_name": "CBD 今天适合坐哪里",
  "episodes": [
    "CBD今天最好坐的一张椅子",
    "今天中午去哪放空",
    "北京今天最舒服的一公里"
  ]
}
```

### 6.4 recommend_brands.md

**职责：** 为选题推荐可结合品牌。

输出：

```json
{
  "recommended_brands": [
    {
      "brand": "咖啡品牌",
      "role": "作为路线中的放空点",
      "reason": "与松弛生活方式匹配"
    }
  ]
}
```

### 6.5 recommend_visuals.md

**职责：** 为选题推荐视觉表达。

输出：

```json
{
  "cover_idea": "一张空椅子 + CBD背景",
  "shot_list": ["远景", "手部细节", "路线图", "品牌门头"],
  "visual_style": "自然光、低饱和、城市感"
}
```

---

## 7. 第五层：Writing

负责把选题变成具体内容。

### 7.1 wechat_article.md

输出公众号文章：

```json
{
  "title_options": [],
  "lead": "",
  "body": "",
  "brand_integration": "",
  "image_suggestions": [],
  "ending": ""
}
```

### 7.2 xiaohongshu.md

输出小红书笔记：

```json
{
  "title_options": [],
  "cover_text": "",
  "body": "",
  "hashtags": [],
  "comment_prompt": "",
  "shooting_suggestions": []
}
```

### 7.3 moments.md

输出朋友圈文案：

```json
{
  "short_copy": "",
  "long_copy": "",
  "image_order": [],
  "call_to_action": ""
}
```

### 7.4 video_script.md

输出视频脚本：

```json
{
  "hook_3s": "",
  "scenes": [],
  "voice_over": "",
  "subtitles": [],
  "ending": ""
}
```

### 7.5 poster_copy.md

输出 KV / 海报文案：

```json
{
  "main_slogan": "",
  "sub_copy": "",
  "cta": "",
  "variants": []
}
```

---

## 8. 第六层：Reports

负责生成周报、月报和 PPT 结构。

### 8.1 weekly_report.md

输出《北京商业内容观察｜Week XX》：

```json
{
  "title": "北京商业内容观察｜Week 28",
  "hot_topics": [],
  "platform_observations": [],
  "competitor_analysis": [],
  "ideas_in77": [],
  "ideas_in88": [],
  "next_week_calendar": []
}
```

### 8.2 monthly_report.md

输出月度复盘：

```json
{
  "month": "2026-07",
  "trend_summary": "",
  "best_cases": [],
  "content_lessons": [],
  "next_month_recommendations": []
}
```

### 8.3 ppt_outline.md

输出 PPT 结构：

```json
{
  "deck_title": "",
  "slides": [
    {
      "slide_title": "",
      "slide_type": "chart / case / summary / calendar",
      "key_points": [],
      "visual_suggestion": ""
    }
  ]
}
```

---

## 9. 第七层：Style

这一层是 INSight OS 与普通 AI 工具最大的区别之一。

AI 不是直接写，而是先学习品牌和参考媒体风格，再生成内容。

### 9.1 style_in77.md

用于加载 in77 风格。

核心方向：

- 城市
- 公园
- CBD
- 艺术
- 品牌体验
- 松弛
- 开放

避免：

- 过度促销
- 强卖点堆叠
- 硬广感

### 9.2 style_in88.md

用于加载 in88 风格。

核心方向：

- 王府井
- 科技
- 动漫
- 年轻
- 潮流
- 室内漫游
- 生活方式

避免：

- 传统百货口吻
- 老派商场话术
- 过度端着

### 9.3 style_same.md

用于参考“山每”式内容风格。

方向：

- 轻盈
- 生活方式
- 情绪表达
- 城市观察

### 9.4 style_monocle.md

用于参考 Monocle 式城市商业观察。

方向：

- 国际化
- 城市治理
- 商业观察
- 克制高级

### 9.5 style_popeye.md

用于参考 Popeye 式青年生活方式。

方向：

- 青年
- 街区
- 穿搭
- 咖啡
- 日常生活

### 9.6 style_andpremium.md

用于参考 &Premium 式温和生活美学。

方向：

- 温柔
- 精致
- 慢生活
- 物件感
- 日常美学

---

## 10. 第八层：Shared

### 10.1 system_prompt.md

所有 Prompt 的系统层角色：

```md
你是 INSight OS，一名商业地产内容策略总监。

你服务于北京 in77 与北京 in88。

你需要基于真实输入、品牌 DNA、竞品内容和城市趋势，输出可执行的内容策略建议。

你不能杜撰事实，不能编造数据，不能夸大项目能力。

所有输出必须结构化，必须保留判断依据。
```

### 10.2 json_schema.md

共享 JSON 输出规范，不计入 36 个核心 Prompt。

要求：

- 所有输出必须是合法 JSON。
- 所有数组必须可为空，但不能省略关键字段。
- 所有评分统一使用 1-5 或 0-100，不混用。
- 所有来源依据必须放入 `source_evidence`。

### 10.3 rules.md

共享规则，不计入 36 个核心 Prompt。

规则：

- 不能杜撰。
- 不能夸张。
- 不能虚构品牌、数据、活动。
- 不能把竞品内容直接改写成自己的内容。
- 必须区分事实、判断和建议。
- 事实必须来自输入内容。
- 建议可以推理，但必须说明推理依据。

---

## 11. Brand Brain 品牌大脑

Brand Brain 是 INSight OS 和普通 AI 工具最大的区别。

普通 AI 工具：

```text
输入
  ↓
输出
```

INSight OS：

```text
输入
  ↓
Brand Brain
  ↓
Prompt
  ↓
输出
```

也就是说，AI 在生成之前，必须先读取品牌 DNA。

### 11.1 Brand Brain 自动加载内容

以 in77 为例，系统自动加载：

- 品牌定位
- 栏目结构
- 历史文章
- 高阅读内容
- 高收藏内容
- 禁用词
- 喜欢的语气
- 图片风格
- 品牌合作

以 in88 为例，系统自动加载：

- 王府井
- 科技
- 动漫
- 年轻
- 生活方式
- 室内漫游
- 历史内容表现
- 适合合作品牌

### 11.2 Brand Brain 输出结构

```json
{
  "project": "in88",
  "positioning": "王府井年轻生活方式与科技潮流商业项目",
  "tone": ["年轻", "科技", "动漫", "生活方式"],
  "preferred_columns": ["室内漫游", "王府井新鲜事", "年轻人的周末"],
  "high_performance_topics": ["动漫IP", "科技首店", "室内Citywalk"],
  "avoid_words": ["传统百货", "促销甩卖"],
  "visual_style": ["明亮", "潮流", "动线感"],
  "brand_partners": ["科技品牌", "动漫IP", "潮流零售"],
  "content_ratio": {
    "brand_dna": 0.8,
    "innovation": 0.2
  }
}
```

---

## 12. Prompt Composer

Prompt Composer 是 V2 的关键模块。

它负责在调用 GPT 前，自动拼装 Prompt。

### 12.1 拼装逻辑

```text
用户输入
  +
系统角色 system_prompt.md
  +
任务 Prompt
  +
Brand Brain
  +
Style Prompt
  +
JSON Schema
  +
Rules
  ↓
最终 Prompt
```

### 12.2 示例

用户请求：

```text
为 in88 生成 5 条本周小红书选题。
```

系统自动加载：

- `system_prompt.md`
- `generate_ideas.md`
- `style_in88.md`
- `brand_brain/in88.json`
- `json_schema.md`
- `rules.md`

最终输出：

```json
{
  "project": "in88",
  "ideas": [
    {
      "title": "今天别急着回家",
      "angle": "用王府井夜间室内漫游承接下班后情绪",
      "platforms": ["小红书"],
      "priority": 5,
      "reason": "符合 in88 年轻、室内、生活方式方向。"
    }
  ]
}
```

---

## 13. V2 架构

```text
                User
                  │
                  ▼
           Brand Brain
                  │
        (自动加载品牌DNA)
                  ▼
          Prompt Composer
      （动态拼装Prompt）
                  ▼
             GPT-5.5
                  ▼
          Structured JSON
                  ▼
          Frontend Render
```

### V2 价值

同一个 Prompt，因为 Brand Brain 不同，输出会完全不同。

`generate_ideas.md` 对 in77 输出的是：

- CBD
- 公园
- 松弛
- 艺术
- 城市开放空间

对 in88 输出的是：

- 王府井
- 科技
- 动漫
- 室内漫游
- 年轻生活方式

这就是品牌内容 AI，而不是通用 AI 文案工具。

---

## 14. 开发落地建议

### V1

- 先建立 36 个 Prompt 文件。
- Prompt 内容先用 Markdown 管理。
- API 调用时手动选择 Prompt。
- 品牌配置从 `brand_profiles.json` 读取。

### V2

- 建立 Brand Brain 数据表。
- 建立 Prompt Composer。
- 支持动态拼装 Prompt。
- 支持根据项目自动加载风格。
- 支持根据历史表现调整选题。

### V3

- 根据内容发布后的真实表现回流训练。
- 自动识别品牌内容疲劳点。
- 自动判断哪些栏目应该延续、停止或创新。

---

## 15. 最小可运行 Prompt 闭环

第一版只要跑通以下 6 个 Prompt，就可以支撑 MVP：

1. `summarize_content.md`
2. `tag_content.md`
3. `score_content.md`
4. `trend_analysis.md`
5. `generate_ideas.md`
6. `weekly_report.md`

完整 36 个 Prompt 用于后续精细化扩展。

---

## 16. 一句话总结

Prompt Library 是 INSight OS 的策划方法论内核。

Brand Brain 是 INSight OS 的品牌记忆。

Prompt Composer 是 INSight OS 真正从“AI 工具”升级为“品牌内容 AI”的关键。
