# Changelog

All notable changes to Sloth-MGO-Eido will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-04-23

> First batch delivery: core closed-loop (intelligence -> content -> conversion).

### Added

**Core Architecture**
- 1+7 parent-child skill architecture: one parent Skill (commander) orchestrating seven sub-modules
- Intent recognition and routing engine with keyword and semantic-based module dispatch
- Three-tier risk control mechanism (L1 lightweight / L2 standard / L3 full)
- Hybrid knowledge adapter with three-tier retrieval (local files / knowledge base API / vector DB)
- Cross-module context passing for automatic data flow between modules
- First-use guided configuration flow via EXTEND.md

**Module A: Content & Creative Engine**
- Value validation with Voice of Customer (VoC) data integration
- Competitive positioning with competitor intel injection
- Eight content types: product articles, case studies, whitepapers, thought leadership, comparison guides, EDM templates, social posts, sales enablement content
- Writing frameworks: AIDA, STAR, problem-solution-path, trend-insight-action
- Optional creative acceleration: storyboards, asset recommendations, short video scripts
- Three density modes: lightning / standard / deep dive

**Module C: Market Intelligence Center**
- Four intelligence dimensions: competitor monitoring, industry trends, customer demand shifts, category opportunities
- Competitor dynamic tracking: website changes, content updates, product releases, hiring signals, funding
- Impact-rated intelligence with recommended response strategies
- Trend signal classification: confirmed / emerging / weak signals
- VoC analysis report generation with automatic knowledge base updates
- Battle Card generation with professional, objective tone guidelines

**Module D: Lead Nurturing & Conversion Engine**
- Four-dimension lead scoring: profile match (30%), behavior signals (30%), need clarity (25%), recency (15%)
- Four-tier lead classification: H (Hot) / A / B / C with SLA-based handoff
- Automated 5-7 step nurture sequence orchestration with stage-matched content
- Lead intel cards for sales handoff with customer profile, interaction history, and recommended talking points
- Two-way market-sales feedback mechanism with three auto-triggered chains
- Win/loss analysis with monthly pattern identification

**Compliance Engine**
- Advertising law compliance: absolute claims detection, false advertising check
- Brand compliance: forbidden word list, brand tone validation
- Data privacy (PIPL): personal data de-identification reminders
- Data security: sensitive data classification, cross-border transfer detection
- Industry-specific rules: finance, healthcare, education (configurable)
- Competitor mention rules: anti-unfair competition law compliance
- Three-level compliance results: red (block) / yellow (warn) / green (pass)

**Knowledge Base Architecture**
- Seven shared knowledge partitions: Product Data, Brand Assets, Competitor Intel, Voice of Customer, Best Practices, Industry Intel, Growth Metrics
- Publish-subscribe model for cross-module knowledge sharing
- Human + AI dual confirmation for knowledge base updates
- Version control with rollback support for critical files

**Cross-skill Integration Design**
- Sloth-Sales-Eido: two-way lead and feedback bridge
- Sloth-PSC-Eido: competitive intel and solution framework exchange
- Sloth-SMM-Eido: content distribution and trending data feedback
- Agent-Reach: 17-platform deep search enhancement
- Document delivery: DeckBuilder-Eido / PPTX / DOCX / PDF integration
- Data analysis: data-analysis / xlsx skill integration
- Strategy alignment: Sloth-StratAlign-Eido BSC integration

---

## [1.1.0] - 2026-04-23 — 知识库增强与全球最佳实践融合

### Added — 新增7个参考知识库

基于全网16个开源营销技能仓库的系统性调研（包括 kostja94/marketing-skills、coreyhaines31/marketingskills、manojbajaj95/claude-gtm-plugin、SpillwaveSolutions/running-marketing-campaigns-agent-skill、aaron-he-zhu/seo-geo-claude-skills 等），提取并融合了全球顶级营销框架和方法论。

- `references/geo-optimization.md`：GEO/LLMO 生成式引擎优化指南，覆盖5大优化策略、中外AI搜索平台差异化适配、IndexNow快速索引
- `references/messaging-frameworks.md`：7大品牌定位与消息框架（Peep Laja四层模型、消息屋、Geoffrey Moore、April Dunford、StoryBrand SB7、Andy Raskin、MECLABS）
- `references/churn-prevention-playbook.md`：客户流失防控手册，含健康度评分模型、动态挽留方案映射、Dunning催收栈
- `references/competitive-content-strategy.md`：竞品内容SEO策略，4种页面格式（Alternative/Alternatives/You vs X/X vs Y）及集中化竞品数据架构
- `references/lead-magnet-strategy.md`：线索磁铁策略，11种类型×3阶段映射、门控策略矩阵、落地页与交付优化
- `references/utm-tracking-standards.md`：UTM追踪标准与治理规范，含GA4渠道对齐、平台动态参数宏、中国特色追踪方案
- `references/email-sequence-templates.md`：7类邮件序列模板及自动化框架，含Subject Line公式、生命周期阶段自动化规则

### Enhanced — 模块能力增强

- **SKILL.md**：知识库调度新增6个分区，意图路由表扩展6个模块的触发词，跨模块上下文新增4条GEO/竞品/线索磁铁/流失相关数据流
- **content-engine.md**：新增"品牌定位与消息框架""竞品对比落地页"2种内容类型，新增 Step 6 GEO/LLMO优化增强
- **lead-engine.md**：新增线索磁铁（Lead Magnet）设计与优化工作流，含买家阶段映射和门控策略
- **customer-growth.md**：新增 Step 5 客户流失防控与健康度管理（健康度评分/风险预警/挽留方案/Dunning）
- **channel-distribution.md**：新增 GEO/LLMO 渠道优化和 UTM 追踪标准化两个执行板块
- **EXTEND.md**：新增"扩展知识库"说明段落，列出7个新增参考文件及触发场景

---

## [Planned] [2.0.0] - Execution Expansion

> Second batch delivery: content distribution channels and campaign execution capabilities.
> Estimated timeline: 3-4 weeks after 1.0.0 stabilization.

### Planned

**Module B: Campaign & Project Command**
- Smart campaign planning with agenda, budget, venue, and material list generation
- Execution control with minute-level run-down tables and T-minus checklists
- Vendor management with OCR-based quote comparison
- Cross-module project progress monitoring and weekly/monthly report generation
- Campaign ROI estimation and post-event review

**Module E: Channel Distribution & Acquisition**
- Multi-channel content adaptation for 8 channels: WeChat MP, Zhihu, Toutiao, Xiaohongshu, LinkedIn, EDM, WeCom, Douyin
- Three candidate titles generated per channel version
- SEO content optimization: keyword research, content audit, gap analysis
- Paid advertising assets: search ads, display ads, landing page content
- ABM support with multi-touchpoint outreach sequences
- Lead collection and channel-tagged handoff to Module D

**Supporting Assets**
- Channel adaptation template library
- Campaign planning template library

---

## [Planned] [3.0.0] - Growth Closed-Loop

> Third batch delivery: customer lifecycle growth and metrics-driven experimentation.
> Estimated timeline: 4-6 weeks after 2.0.0 stabilization.
> Prerequisite: accumulated operational data from Module A/C/D/B/E to power growth models and attribution analysis.

### Planned

**Module F: Customer Lifecycle Growth**
- Personalized onboarding email sequences (5-7 emails covering first month)
- Customer health score model with three-tier risk response (light / moderate / high)
- Key person departure detection via LinkedIn monitoring
- Renewal/expansion marketing with 90/60/30-day automated triggers
- Upsell/cross-sell opportunity identification based on usage data
- Customer case study collection: candidate screening, interview guides, outreach templates
- NPS/CSAT analysis with layered satisfaction driver identification

**Module G: Growth Metrics & Experimentation**
- North Star metrics dashboard: 7 metric tiers covering acquisition, conversion, revenue, retention, channel, content, and pipeline
- Attribution analysis: first-touch, last-touch, and multi-touch weighted models
- A/B experiment framework: hypothesis definition, experiment design, result analysis, knowledge archival
- ROI review engine: campaign ROI, content ROI, channel ROI, and comprehensive monthly/quarterly reports
- Budget allocation recommendations based on historical ROI data

---

## Roadmap

Continuous iteration directions beyond 3.0.0:

- **Sloth-Sales-Eido bidirectional bridge deepening**: richer lead-to-opportunity data exchange, joint pipeline analytics, and tighter feedback loops between marketing and sales workflows
- **Agent-Reach full-channel enhancement**: expanding search and monitoring coverage across all 17 platforms, automated competitor alert triggers, and deeper content extraction capabilities
- **Automation uplift**: scheduled competitor monitoring, periodic report generation and push, automated knowledge base refresh, and event-triggered nurture sequences
- **Industry vertical expansion**: pre-built templates and compliance rules for finance, manufacturing, and healthcare verticals
