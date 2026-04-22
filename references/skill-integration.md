# 跨技能协同规则与数据映射 Skill Integration

> Sloth-MGO-Eido 参考知识库 | 版本 1.0
> 适用范围：Sloth-Role-Eido 技能家族内 MGO 与其他技能的协同接口定义

---

## 1. 技能家族协同总览

### 1.1 MGO 协同技能矩阵

```
                    ┌─────────────┐
                    │  StratAlign  │ ← 战略对齐
                    │    Eido      │
                    └──────┬──────┘
                           │ 战略目标下发
                    ┌──────▼──────┐
         ┌──────────┤   MGO-Eido   ├──────────┐
         │          │  (市场增长)   │          │
         │          └──┬───┬───┬──┘          │
         │             │   │   │              │
    线索移交      内容注入 │ 渠道搜索    文档交付
         │             │   │              │
    ┌────▼────┐  ┌─────▼──┐│  ┌──────▼──────┐
    │  Sales   │  │  PSC    ││  │ Agent-Reach  │
    │  Eido    │  │  Eido   ││  │  (搜索引擎)   │
    │ (销售)    │  │(售前顾问)││  └─────────────┘
    └─────────┘  └────────┘│
                           │
                    ┌──────▼──────┐
                    │  SMM-Eido    │
                    │ (社交媒体)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  DeckBuilder │ ← 文档交付
                    │  / PPTX/PDF  │
                    └─────────────┘
```

### 1.2 数据流方向定义

| 方向 | 说明 | 频率 |
|------|------|------|
| MGO → Sales-Eido | 合格线索（MQL/SQL）移交 | 实时（触发式） |
| Sales-Eido → MGO | 线索反馈（赢单/丢单/不合格）、评分校准 | 每周汇总 |
| MGO → PSC-Eido | 客户背景资料注入（用于售前准备） | 按需（商机触发） |
| MGO → SMM-Eido | 内容发布计划、品牌调性指引 | 每周同步 |
| SMM-Eido → MGO | 社交互动数据、舆情信号 | 每日汇总 |
| MGO ↔ Agent-Reach | 搜索请求 / 搜索结果 | 按需（实时） |
| StratAlign-Eido → MGO | OKR/战略目标、预算分配 | 每季度 |
| MGO → StratAlign-Eido | 营销绩效数据、目标达成进度 | 每月汇报 |

---

## 2. MGO ↔ Sales-Eido 字段映射表

### 2.1 线索移交（MGO → Sales）字段映射

MGO 评分达到 H/A 级的线索，自动生成移交数据包：

| MGO 字段 | Sales-Eido 字段 | 数据类型 | 必填 | 映射规则 |
|----------|-----------------|---------|------|---------|
| `lead_id` | `lead_id` | String | 是 | 直传，全局唯一标识 |
| `contact_name` | `contact_name` | String | 是 | 直传 |
| `contact_email` | `email` | String | 是 | 直传 |
| `contact_phone` | `phone` | String | 否 | 直传，脱敏存储 |
| `contact_title` | `job_title` | String | 否 | 直传 |
| `company_name` | `account_name` | String | 是 | 直传 |
| `company_industry` | `industry` | Enum | 是 | MGO行业分类 → Sales行业枚举映射表 |
| `company_size` | `employee_range` | Enum | 否 | "1-50" / "51-200" / "201-1000" / "1001-5000" / "5000+" |
| `company_revenue` | `annual_revenue_range` | Enum | 否 | "<500万" / "500万-5000万" / "5000万-5亿" / "5亿+" |
| `lead_score_total` | `mgo_score` | Integer | 是 | 0-100分值直传 |
| `lead_grade` | `mgo_grade` | Enum | 是 | "H" / "A" / "B" / "C" |
| `score_d1_firmographic` | `fit_score` | Integer | 否 | 企业画像维度分值 |
| `score_d2_behavioral` | `engagement_score` | Integer | 否 | 行为信号维度分值 |
| `score_d3_intent` | `intent_score` | Integer | 否 | 需求明确度维度分值 |
| `score_d4_recency` | `recency_score` | Integer | 否 | 时效性维度分值 |
| `lead_source` | `lead_source` | String | 是 | UTM Source 值 |
| `lead_source_detail` | `lead_source_detail` | String | 否 | UTM Campaign + Medium |
| `first_touch_channel` | `first_touch` | String | 否 | 首次触达渠道 |
| `last_touch_channel` | `last_touch` | String | 否 | 末次触达渠道 |
| `content_consumed[]` | `content_history` | Array | 否 | 消费内容列表（标题+类型+日期） |
| `key_behaviors[]` | `activity_log` | Array | 否 | 关键行为事件列表 |
| `expressed_needs` | `pain_points` | Text | 否 | 表单/对话中表达的需求 |
| `estimated_budget` | `budget_range` | String | 否 | 如有 |
| `estimated_timeline` | `decision_timeline` | String | 否 | 如有 |
| `handoff_timestamp` | `created_at` | DateTime | 是 | 移交时间 ISO-8601 |
| `handoff_sla` | `follow_up_deadline` | DateTime | 是 | H级=+4h, A级=+24h |
| `attribution_summary` | `marketing_attribution` | JSON | 否 | 归因摘要（首触/末触/加权） |

### 2.2 销售反馈（Sales → MGO）字段映射

| Sales-Eido 字段 | MGO 字段 | 用途 |
|-----------------|----------|------|
| `lead_id` | `lead_id` | 关联标识 |
| `sales_disposition` | `feedback_disposition` | 跟进结果枚举 |
| `disposition_reason` | `feedback_reason` | 详细原因文本 |
| `actual_deal_stage` | `pipeline_stage` | 当前商机阶段 |
| `deal_amount` | `deal_value` | 商机金额（用于归因ROI计算） |
| `close_date` | `close_date` | 预计/实际成交日期 |
| `feedback_timestamp` | `feedback_at` | 反馈时间 |
| `score_accuracy` | `score_feedback` | 评分准确性反馈（"偏高"/"准确"/"偏低"） |

### 2.3 Sales Disposition 枚举映射

| Sales Disposition | MGO 处理逻辑 |
|-------------------|-------------|
| `qualified` | 确认合格，线索进入Pipeline，记录为正样本 |
| `working` | 正在跟进中，不做评分调整 |
| `nurture_back` | 退回培育池，降为B级，进入Nurturing序列 |
| `disqualified_fit` | 企业画像不匹配 → 触发D1维度校准反馈 |
| `disqualified_timing` | 时机不对 → 降为C级，标记"延迟跟进" |
| `disqualified_budget` | 无预算 → 降为C级，标记"预算周期后重访" |
| `disqualified_duplicate` | 重复线索 → 合并处理 |
| `closed_won` | 成交 → 触发归因结算，更新渠道ROI |
| `closed_lost` | 丢单 → 记录丢单原因，触发丢单归因分析 |

---

## 3. MGO → PSC-Eido 注入规则

当线索升级为商机（Opportunity Created）或 Sales 申请售前支持时，MGO 向 PSC-Eido 注入客户背景包。

### 3.1 注入触发条件

| 触发事件 | 注入内容级别 |
|----------|-------------|
| Sales手动申请售前支持 | 完整背景包 |
| 商机阶段进入"方案演示" | 完整背景包 |
| 商机阶段进入"POC评估" | 完整背景包 + 竞品情报 |
| Sales标记"需要Battle Card" | 竞品情报包 |

### 3.2 背景包数据结构

```json
{
  "psc_briefing_pack": {
    "account_overview": {
      "company_name": "客户企业名",
      "industry": "行业",
      "company_size": "规模",
      "annual_revenue": "营收范围",
      "headquarters": "总部位置",
      "tech_stack": ["已知技术栈"],
      "public_info_summary": "公开信息摘要（官网/新闻/年报要点）"
    },
    "contact_overview": {
      "primary_contact": {
        "name": "姓名",
        "title": "职位",
        "role_in_decision": "决策角色（决策者/影响者/使用者/把关者）"
      },
      "known_stakeholders": [
        {"name": "姓名", "title": "职位", "role": "角色"}
      ]
    },
    "engagement_history": {
      "first_touch_date": "首次触达日期",
      "first_touch_channel": "首触渠道",
      "total_touchpoints": "总触点数",
      "key_content_consumed": [
        {"title": "内容标题", "type": "内容类型", "date": "消费日期"}
      ],
      "key_behaviors": [
        {"event": "行为事件", "date": "日期", "detail": "详情"}
      ],
      "engagement_timeline_summary": "互动时间线摘要（自然语言）"
    },
    "needs_intelligence": {
      "expressed_pain_points": ["已明确表达的痛点"],
      "inferred_needs": ["基于行为推断的需求"],
      "budget_signal": "预算信号（如有）",
      "timeline_signal": "时间线信号（如有）",
      "evaluation_criteria": ["已知的评估标准"]
    },
    "competitive_intelligence": {
      "current_vendor": "当前使用产品（如已知）",
      "competitors_evaluated": ["正在评估的竞品"],
      "contract_expiry": "当前合同到期时间（如已知）",
      "switch_motivation": "切换动机",
      "battle_card_ref": "相关Battle Card编号"
    },
    "mgo_scoring_snapshot": {
      "total_score": 75,
      "grade": "A",
      "d1_firmographic": 80,
      "d2_behavioral": 70,
      "d3_intent": 75,
      "d4_recency": 85
    }
  }
}
```

### 3.3 PSC-Eido 使用指引

| PSC场景 | 使用MGO数据 | 目的 |
|---------|------------|------|
| 会议准备 | account_overview + contact_overview | 了解客户背景，准备开场 |
| 方案定制 | needs_intelligence | 针对性定制演示内容 |
| 竞品应对 | competitive_intelligence | 准备竞品对比话术 |
| 后续跟进 | engagement_history | 引用客户已消费的内容建立连续性 |
| SPIN提问 | expressed_pain_points + inferred_needs | 设计高质量提问清单 |

---

## 4. MGO ↔ SMM-Eido 接口

### 4.1 MGO → SMM 内容发布计划

MGO 生成内容后，向 SMM-Eido 发布分发指令：

```json
{
  "content_distribution_request": {
    "content_id": "MGO内容唯一ID",
    "content_title": "内容标题",
    "content_type": "article | case_study | whitepaper | social_post | video_script",
    "content_body": "内容正文（或正文链接）",
    "target_channels": [
      {
        "channel": "wechat_mp | zhihu | linkedin | xiaohongshu | toutiao | video_channel | douyin",
        "priority": "P0 | P1 | P2",
        "scheduled_time": "ISO-8601 发布时间",
        "adaptation_notes": "渠道适配备注（如'小红书版需改为清单体'）"
      }
    ],
    "campaign_id": "关联Campaign ID",
    "utm_params": {
      "source": "渠道值",
      "medium": "媒介值",
      "campaign": "活动值"
    },
    "compliance_status": "GREEN-PASS | YELLOW-WARN",
    "brand_tone": "professional | friendly | authoritative | conversational",
    "visual_assets": ["配图/视频素材链接列表"],
    "hashtags_suggested": ["建议话题标签"]
  }
}
```

### 4.2 SMM → MGO 社交数据回流

| SMM 数据字段 | MGO 用途 | 回流频率 |
|-------------|---------|---------|
| `post_id` + `engagement_metrics` (views, likes, comments, shares) | 内容效果评估，渠道归因 | 每日汇总 |
| `follower_growth` (per channel) | 渠道健康度监控 | 每周 |
| `comment_sentiment` (positive/neutral/negative) | 品牌舆情信号 | 实时（负面立即） |
| `mention_alerts` (品牌/竞品提及) | 竞品监控、PR风险预警 | 实时 |
| `top_performing_content[]` | 内容策略复盘输入 | 每周 |
| `audience_demographics` | 受众画像更新 | 每月 |
| `social_leads[]` (私信/评论中表达需求的用户) | 社交线索采集→进入评分 | 实时 |

### 4.3 品牌调性同步

```
MGO → SMM 品牌调性指引结构：

{
  "brand_voice_guide": {
    "tone": "专业但不刻板，亲和但不随意",
    "vocabulary_positive": ["赋能", "协同", "高效", "智能化", "增长"],
    "vocabulary_avoid": ["颠覆", "吊打", "最强", "碾压"],
    "emoji_policy": "LinkedIn不用/小红书适度/微信公众号不用",
    "response_style": "评论回复在2小时内，用第一人称，保持友好专业",
    "crisis_escalation": "负面评论5条以上或KOL负面提及 → 立即通知MGO"
  }
}
```

---

## 5. Agent-Reach 搜索路由策略

当 MGO 需要外部信息时，通过 Agent-Reach 发起搜索请求。以下是场景→渠道路由规则：

### 5.1 搜索场景路由表

| MGO 搜索场景 | Agent-Reach 首选渠道 | 备选渠道 | 搜索参数建议 |
|-------------|---------------------|---------|-------------|
| 目标企业背景调研 | 企查查/天眼查（web） | 官网（web）→ LinkedIn | 企业名+行业+规模+融资 |
| 目标联系人信息 | LinkedIn（career） | 企业官网团队页 | 姓名+企业+职位 |
| 行业趋势/报告 | Search（搜索引擎） | 知乎（social） | 行业关键词+年份+趋势/报告 |
| 竞品信息收集 | 竞品官网（web） | Search + 知乎 | 竞品名+产品+功能+定价 |
| 竞品社交声量 | 微博/小红书/知乎（social） | V2EX/Reddit | 竞品名+用户评价 |
| 行业新闻/事件 | Search + 微博（social） | 头条/公众号（web） | 行业+事件关键词 |
| 技术文档/API | GitHub（dev） | 官方文档（web） | 产品名+技术栈+API |
| 行业KOL识别 | LinkedIn + 知乎 + 公众号 | 小红书/B站 | 行业关键词+KOL/专家/大V |
| 客户公开信息 | 企业官网 + 年报 + 新闻 | Search | 企业名+年报/财报/新闻 |
| 政策法规查询 | Search（gov站点） | 公众号（政策类） | 法规名称+行业+最新 |
| 活动/展会信息 | Search + 活动平台 | 公众号/LinkedIn | 行业+展会/峰会/活动+年份 |
| 视频内容参考 | B站/YouTube（video） | 抖音 | 行业关键词+教程/解读 |

### 5.2 搜索请求格式

```json
{
  "search_request": {
    "purpose": "MGO搜索目的枚举",
    "query": "搜索关键词",
    "preferred_channel": "首选Agent-Reach渠道",
    "fallback_channels": ["备选渠道列表"],
    "language": "zh-CN | en-US",
    "time_range": "最近1月 | 最近3月 | 最近1年 | 不限",
    "max_results": 10,
    "output_format": "summary | full_text | structured_data"
  }
}
```

### 5.3 搜索结果处理规则

| 结果质量 | 判定标准 | 处理方式 |
|----------|---------|---------|
| 高质量 | 来自官方/权威来源、数据有日期和出处 | 直接引用，标注来源 |
| 中等质量 | 来自行业媒体/专业社区，信息较新 | 交叉验证后引用 |
| 低质量 | 来源不明、数据陈旧、个人观点为主 | 仅作参考，不直接引用 |
| 无结果 | 搜索无有效返回 | 切换备选渠道重试 → 仍无则标记"信息待补充" |

---

## 6. 文档交付技能调用规则

MGO 在产出内容/报告时，需调用文档生成技能进行最终交付。

### 6.1 交付格式 → 技能映射

| 交付物类型 | 调用技能 | 触发条件 |
|-----------|---------|---------|
| 演示文稿（PPT） | sloth-deckbuilder-eido 或 pptx | 季度报告/方案演示/行业分享 |
| 白皮书/报告（PDF） | pdf | 白皮书/研究报告/正式文档 |
| 数据分析报告 | data-analysis + xlsx | 渠道分析/ROI报告/评分报告 |
| Excel数据表 | xlsx | 线索列表导出/评分明细/归因数据 |
| Word文档 | docx | 内容草稿/合同条款/合规审核报告 |

### 6.2 调用参数规范

```
文档交付请求结构：

{
  "delivery_request": {
    "doc_type": "pptx | pdf | xlsx | docx",
    "doc_title": "文档标题",
    "doc_purpose": "用途说明",
    "content_source": "MGO生成的内容数据（结构化JSON或Markdown）",
    "brand_template": "使用品牌模板（如有）",
    "language": "zh-CN",
    "target_audience": "高管 | 执行层 | 外部客户",
    "page_count_target": "目标页数（PPT）",
    "delivery_deadline": "交付截止时间",
    "quality_check": true
  }
}
```

### 6.3 DeckBuilder 专项调用

当 MGO 需要生成 PPT 时，传递给 DeckBuilder-Eido 的 slide_spec 格式：

```python
# MGO → DeckBuilder 数据映射示例
slide_spec = {
    "metadata": {
        "title": "2024 Q4 营销绩效报告",
        "subtitle": "渠道归因与增长分析",
        "author": "市场增长团队",
        "date": "2024-12-31"
    },
    "slides": [
        {
            "layout": "title_slide",
            "title": "2024 Q4 营销绩效报告",
            "subtitle": "数据驱动增长"
        },
        {
            "layout": "kpi_dashboard",
            "title": "核心指标总览",
            "kpis": [
                {"label": "新线索", "value": "1,234", "change": "+15%"},
                {"label": "MQL", "value": "456", "change": "+22%"},
                {"label": "SQL", "value": "123", "change": "+18%"},
                {"label": "成交额", "value": "¥5.6M", "change": "+25%"}
            ]
        },
        # ... 更多幻灯片
    ]
}
```

---

## 7. StratAlign-Eido 战略对齐接口

### 7.1 战略目标下发（StratAlign → MGO）

每季度初，StratAlign-Eido 向 MGO 下发战略对齐指令：

```json
{
  "strategic_alignment": {
    "period": "2024-Q4",
    "company_okr": {
      "objective": "公司级目标描述",
      "key_results": [
        "KR1：全年ARR达到XX万",
        "KR2：新客户数达到XX家",
        "KR3：NRR保持XX%以上"
      ]
    },
    "marketing_okr": {
      "objective": "市场增长目标",
      "key_results": [
        {"kr": "MQL数量达到XX", "current": 0, "target": 500},
        {"kr": "SQL数量达到XX", "current": 0, "target": 150},
        {"kr": "营销归因Pipeline达到¥XX万", "current": 0, "target": 2000},
        {"kr": "CAC降至¥XX以下", "current": 5000, "target": 4000}
      ]
    },
    "budget_allocation": {
      "total_budget": 1000000,
      "channel_allocation": {
        "sem_paid": 300000,
        "content_seo": 200000,
        "events": 200000,
        "social": 150000,
        "email": 50000,
        "tools_tech": 100000
      }
    },
    "strategic_priorities": [
      "优先拓展制造业垂直市场",
      "加强内容营销降低CAC",
      "建立合作伙伴推荐体系"
    ],
    "icp_definition": {
      "primary_industries": ["制造业", "科技", "金融"],
      "company_size": "200-5000人",
      "decision_makers": ["CMO", "VP Marketing", "数字化负责人"],
      "geo": "华东、华南、华北"
    }
  }
}
```

### 7.2 MGO 绩效回报（MGO → StratAlign）

MGO 每月向 StratAlign-Eido 回报营销绩效：

```json
{
  "marketing_performance_report": {
    "period": "2024-11",
    "okr_progress": [
      {
        "kr": "MQL数量达到500",
        "target": 500,
        "current": 380,
        "progress_pct": 76,
        "on_track": true,
        "forecast": "预计12月底可达520"
      }
    ],
    "budget_utilization": {
      "total_spent": 820000,
      "total_budget": 1000000,
      "utilization_pct": 82,
      "channel_breakdown": {
        "sem_paid": {"spent": 260000, "budget": 300000},
        "content_seo": {"spent": 180000, "budget": 200000}
      }
    },
    "funnel_metrics": {
      "new_leads": 1500,
      "mqls": 420,
      "sqls": 130,
      "opportunities": 65,
      "closed_won": 18,
      "pipeline_value": 18000000,
      "closed_won_value": 5600000
    },
    "channel_attribution_summary": {
      "top_channel_by_leads": "Organic Search",
      "top_channel_by_pipeline": "Events",
      "top_channel_by_roi": "Content/SEO",
      "underperforming": "Social Paid（ROI低于目标50%）"
    },
    "key_insights": [
      "内容营销CAC较SEM低40%，建议Q1增加内容投入",
      "制造业线索转化率显著高于其他行业（+35%）",
      "邮件序列优化后打开率提升18%"
    ],
    "risks_and_blockers": [
      "SEM成本持续上涨，CPC同比+22%",
      "内容团队人力不足，白皮书产出延迟"
    ],
    "next_period_plan": [
      "发布制造业白皮书",
      "启动合作伙伴推荐计划",
      "优化官网转化率（3组A/B测试）"
    ]
  }
}
```

### 7.3 战略对齐检查点

```
季度对齐会议议程（MGO参与StratAlign Review）：

1. OKR进度回顾（15min）
   - MGO各KR达成情况
   - 偏差分析与调整方案

2. 漏斗健康度（10min）
   - 各阶段转化率趋势
   - 瓶颈识别

3. 渠道ROI与预算优化（10min）
   - 渠道归因ROI排名
   - 预算再分配建议

4. ICP与市场策略更新（10min）
   - ICP定义是否需要调整
   - 新市场/行业拓展计划

5. 跨部门协同议题（15min）
   - Sales反馈线索质量
   - 产品路线图对营销的影响
   - 下季度重点Campaign规划
```

---

## 8. 接口版本管理与变更规则

### 8.1 接口版本规范

```
版本命名：v{主版本}.{次版本}
  主版本变更：字段删除/类型变更（Breaking Change）→ 需所有对接方同步升级
  次版本变更：新增字段/新增可选参数（Non-Breaking）→ 向后兼容

当前版本：v1.0
```

### 8.2 变更通知规则

| 变更类型 | 通知提前期 | 通知方式 |
|----------|-----------|---------|
| Breaking Change | 至少2周 | 在SKILL.md changelog中声明 + 通知相关技能维护者 |
| Non-Breaking Change | 即时生效 | 在references/skill-integration.md中更新 |
| 废弃字段（Deprecated） | 标记废弃→保留2个版本→移除 | 字段标注 `[DEPRECATED v1.x]` |

---

*最后更新：2024-Q4 | 维护者：MGO集成引擎*
*关联技能：Sales-Eido v1.1、PSC-Eido v1.0、SMM-Eido v1.0、Agent-Reach v1.0、StratAlign-Eido v1.0、DeckBuilder-Eido v1.0*
