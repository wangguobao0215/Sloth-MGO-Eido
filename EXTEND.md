# Sloth-MGO-Eido 用户个性化配置

> 首次使用时由系统引导填写。你可以随时修改此文件来调整配置，也可以在对话中说"修改配置"触发引导流程。
>
> 所有配置项均为可选，留空或保持默认值即可正常使用。

---

## 一、企业信息

```yaml
company:
  name: ""                          # 公司名称，如"云深科技"
  industry: ""                      # 所属行业，如"企业级 SaaS"、"智能制造"、"金融科技"
  main_products: []                 # 主要产品/服务列表
    # - "智能营销平台"
    # - "客户数据平台（CDP）"
  target_customer_profile:          # 目标客户画像
    company_size: ""                # 目标客户规模，如"200-2000人中大型企业"
    industries: []                  # 目标客户行业，如 ["制造业", "零售", "金融"]
    decision_makers: []             # 典型决策角色，如 ["CMO", "市场VP", "数字化负责人"]
    pain_points: []                 # 目标客户核心痛点
      # - "营销ROI难以量化"
      # - "市场与销售协同低效"
      # - "内容产出跟不上渠道需求"
```

## 二、竞品列表

```yaml
competitors:                        # 3-5 家核心竞品，用于情报监控和内容对标
  - name: ""                        # 竞品名称，如"HubSpot"
    website: ""                     # 竞品官网，如"https://www.hubspot.com"
    notes: ""                       # 备注（可选），如"北美市场领导者，近期发力中国市场"
  - name: ""
    website: ""
    notes: ""
  - name: ""
    website: ""
    notes: ""
  # 可继续添加，建议不超过 5 家
```

## 三、模块偏好

```yaml
modules:
  # 设为 true 启用，false 禁用。默认全部启用。
  # 建议首批至少启用 A + C + D（内容 + 情报 + 线索），构成最小可用闭环。
  content_engine: true              # Module A：内容与创意引擎
  campaign_command: true            # Module B：活动与项目指挥
  market_intel: true                # Module C：市场情报中心
  lead_engine: true                 # Module D：线索培育与转化引擎
  channel_distribution: true        # Module E：渠道分发与获客
  customer_growth: true             # Module F：客户生命周期增长
  growth_metrics: true              # Module G：增长度量与实验
```

## 四、渠道配置

```yaml
channels:
  # 设为 true 开启该渠道的内容适配和分发支持
  wechat_mp: false                  # 微信公众号
  zhihu: false                      # 知乎
  toutiao: false                    # 今日头条 / 百家号
  xiaohongshu: false                # 小红书
  linkedin: false                   # LinkedIn
  edm: false                        # EDM 邮件营销
  wechat_work: false                # 企业微信
  douyin: false                     # 抖音 / 视频号
  # 可自行添加其他渠道：
  # custom_channel_1: false         # 自定义渠道名称
```

## 五、合规级别

```yaml
compliance:
  level: "standard"                 # standard | strict
  # standard：适用于大多数行业，启用广告法 + PIPL 基础校验
  # strict：适用于金融、医疗、教育等强监管行业，启用全量合规规则
  industry_rules: ""                # 行业特定规则集（可选）：finance | healthcare | education | ""
  advertising_law: true             # 广告法校验（绝对化用语检测）
  pipl: true                        # 个人信息保护法校验（数据脱敏提醒）
```

## 六、预算与风控配置

```yaml
budget:
  annual_marketing_budget: ""       # 年度市场预算（元），用于 L3 风控阈值判断和 ROI 参考
  quarterly_budget: ""              # 季度市场预算（元），可选
  single_campaign_limit: ""         # 单次活动预算上限（元），可选
  # 预算信息来源：由用户在初始化时手动填写，或从 CRM/财务系统自动同步
  # L3 风控触发条件"预算>10万"中的预算指单次活动预算或季度预算，优先读取 single_campaign_limit，
  # 如未配置则读取 quarterly_budget / 4，如均未配置则使用默认值 10 万元作为阈值
```

## 七、线索评分权重

```yaml
lead_scoring:
  # 四维度权重之和应为 1.0，可自定义或使用默认值
  weights:
    profile_match: 0.30             # 企业画像匹配度（公司规模、行业、技术栈）
    behavior_signal: 0.30           # 行为信号强度（内容下载、活动参与、网站访问）
    need_clarity: 0.25              # 需求明确度（表单信息、沟通记录）
    recency: 0.15                   # 时效性（线索产生时间、最近互动时间）
  thresholds:
    hot: 80                         # H 级（Hot）：80-100 分，48h 内交付销售
    a_level: 70                     # A 级：70-79 分，7 天内培育后交付
    b_level: 50                     # B 级：50-69 分，进入培育序列
    # C 级：<50 分，存档观察
  handoff_sla_hours: 48             # H 级线索交付销售的 SLA（小时）
```

## 八、集成配置

```yaml
integrations:
  # 以下配置均为可选。未配置的集成项将被跳过，不影响系统正常运行。

  crm:
    enabled: false
    api_url: ""                     # CRM API 地址，如"https://crm.example.com/api/v1"
    api_key: ""                     # CRM API Key（建议通过环境变量注入）
    notes: ""                       # 如与 Sloth-Sales-Eido 共用同一 CRM，在此备注

  wechat_work:
    enabled: false
    corp_id: ""                     # 企业微信 CorpID
    agent_id: ""                    # 应用 AgentID
    secret: ""                      # 应用 Secret（建议通过环境变量注入）

  feishu:
    enabled: false
    app_id: ""                      # 飞书应用 App ID
    app_secret: ""                  # 飞书应用 App Secret（建议通过环境变量注入）
    webhook_url: ""                 # 飞书群机器人 Webhook（可选，用于通知推送）

  wechat_mp:
    enabled: false
    app_id: ""                      # 公众号 AppID
    app_secret: ""                  # 公众号 AppSecret（建议通过环境变量注入）

  analytics:
    enabled: false
    platform: ""                    # 数据分析平台，如"google_analytics"、"baidu_tongji"、"sensors"
    api_url: ""
    api_key: ""
```

---

> **安全提醒**：API Key、Secret 等敏感信息建议通过环境变量注入，不要直接写入此文件。如果此文件需要提交到版本控制，请确保已在 `.gitignore` 中排除，或移除敏感信息后再提交。

---

### 扩展知识库（v1.1.0 新增）

以下参考知识库在 v1.1.0 版本中新增，用于增强特定场景的能力深度：

| 参考文件 | 用途 | 触发场景示例 |
|---------|------|------------|
| `references/geo-optimization.md` | AI搜索引擎优化（GEO/LLMO） | "优化内容的AI搜索可见性""让ChatGPT引用我们" |
| `references/messaging-frameworks.md` | 品牌定位与消息框架 | "帮我做品牌定位""写一个定位声明" |
| `references/churn-prevention-playbook.md` | 客户流失防控 | "分析流失风险""设计挽留方案" |
| `references/competitive-content-strategy.md` | 竞品内容SEO策略 | "做一个竞品Alternative页面" |
| `references/lead-magnet-strategy.md` | 线索磁铁设计 | "设计一个Lead Magnet""白皮书获客方案" |
| `references/utm-tracking-standards.md` | UTM追踪标准 | "给这次活动的链接打UTM" |
| `references/email-sequence-templates.md` | 邮件序列模板 | "设计一套培育邮件""写Welcome序列" |

这些文件会在对应场景触发时自动加载，无需手动配置。如需自定义，可直接编辑对应文件。

---

## 八、2 小时快速上手路径

> 核心理念：先看到价值，再投入时间。不需要万事俱备才能开始。

### 8.1 最小启动：只需 3 个字段

你只需要在首次使用引导中填写 3 个信息就能开始：

1. **公司名称**
2. **主要产品名称**
3. **3 家主要竞品名称**

所有知识库分区为空也没关系，系统照常运行，输出中会标注 `[待补充，建议上传XX]` 提示你逐步完善。不需要提前准备任何文档，知识库可以在使用过程中自然积累。

### 8.2 推荐首次体验场景

建议你第一次使用时说：

> "帮我写一篇我们产品和 [竞品名] 的对比分析文章"

- 这个场景同时触发 Module C（竞品情报采集）和 Module A（内容生成），让你 5 分钟内看到飞轮的雏形
- 即使知识库为空，系统也会通过 Agent-Reach 搜索公开信息完成初稿

### 8.3 三步体验流程

1. **填表**（2 分钟）：回答首次使用引导的 5 个问题（可以只填前 3 个）
2. **说一句话**（10 秒）：用自然语言描述你要做的事
3. **拿到产出**（3-5 分钟）：收到初稿，按需修改

### 8.4 从体验到深度使用

| 使用阶段 | 时间投入 | 动作 | 效果 |
|---------|---------|------|------|
| 快速体验 | 30 分钟 | 跑 2-3 个场景（竞品分析、内容生成、线索清洗） | 验证价值 |
| 基础配置 | 1-2 小时 | 上传产品白皮书、设置渠道偏好、配置合规级别 | 产出质量提升 50% |
| 知识库填充 | 1-2 周（持续） | 按冷启动 SOP 逐步补充各分区数据 | 产出质量提升 80%+，飞轮开始自转 |

---

## 九、知识库冷启动清单

> 知识库的冷启动是系统落地的最大隐形成本。上线前必须完成最低可用数据的填充，否则模块输出质量将大幅下降。

### 9.1 各分区最低可用数据量与责任人

| 知识库分区 | 最低可用数据量 | 建议填充责任人 |
|---|---|---|
| `01_Product_Data` | 1 份产品白皮书 + 核心功能列表 | 产品营销经理 / 解决方案顾问 |
| `02_Brand_Assets` | 禁用词表 + VI 基础规范（Logo、色值、字体） | 品牌经理 |
| `03_Competitor_Intel` | 3-5 家核心竞品的基础 Battle Card | 市场总监 + Module C 自动生成初版后人工校准 |
| `04_Voice_of_Customer` | 10 条以上客户真实反馈（销售记录/客服工单/NPS） | 销售运营 + 客户成功 |
| `05_Best_Practices` | 3 个历史成功案例（含量化成果） | 内容经理 |
| `06_Industry_Intel` | 近 3 个月行业报告摘要 | Module C 自动采集 + 人工筛选确认 |
| `07_Growth_Metrics` | 近 6 个月核心指标基准数据（CAC/LTV/MQL 量等） | 市场分析师 |

### 9.2 冷启动四步 SOP

```
Step 1  上线前 2 周 — 数据填充
        由市场总监组织各数据责任人，按上表清单填充最低可用数据至
        00_Shared/ 对应分区。重点确保 01_Product_Data 和 02_Brand_Assets
        就位（这两项是 Module A 内容引擎的硬依赖）。

Step 2  上线第 1 周 — 竞品初始化扫描
        运行 Module C 的"竞品初始化扫描"功能，自动生成 3-5 家核心竞品的
        基础画像和初版 Battle Card，由市场总监人工校准后入库
        03_Competitor_Intel/。

Step 3  上线第 2 周 — 历史线索导入
        运行 Module D 导入历史线索数据（Excel/CSV），训练初始打分模型。
        同步将历史活动数据、渠道数据导入 07_Growth_Metrics/，
        为 Module G 建立基准线。

Step 4  上线第 1 月末 — 知识库质量审计
        完成首次知识库质量审计，逐分区检查数据完整性和准确性，
        标注需补充的数据缺口，生成《知识库健康度报告》，
        明确第 2 个月的数据补充优先级。
```

---

## 十、团队采纳指南

> 核心理念：不是"全员培训"，而是"种子用户先跑起来"。

### 10.1 四阶段采纳策略

| 阶段 | 时间节点 | 具体动作 | 成功标准 |
|---|---|---|---|
| 种子期 | 上线前 1 周 | 选择 2-3 名愿意尝新的团队成员作为种子用户，进行 1 对 1 辅导上手，优先跑通 A+C+D 最小闭环 | 种子用户能独立完成至少 3 个典型场景（如写一篇竞品对比文章、清洗一批线索、生成一张 Battle Card） |
| 扩散期 | 上线第 2-4 周 | 种子用户在团队内分享使用经验和成果，组织 30 分钟 Demo Session 展示实际产出 | 50% 团队成员尝试使用至少 1 个模块 |
| 常态期 | 上线第 5-8 周 | 将系统嵌入日常工作流（如周报模板中增加"本周 MGO 使用情况"、内容审批流程中加入合规校验环节） | 80% 团队成员每周至少使用 2 次 |
| 优化期 | 持续进行 | 月度反馈收集 + 功能优化迭代，根据使用数据和用户反馈调整模块优先级和工作流 | 用户满意度 > 4/5 分 |

### 10.2 五维成功指标 KPI

| 维度 | 指标 | 目标值 |
|---|---|---|
| 效率提升 | 单篇内容产出时间 | 降低 40% |
| 质量提升 | 内容合规通过率（首次提交即通过） | > 90% |
| 协同改善 | 市场-销售线索反馈周期 | 从 1 周缩短至 1 天 |
| 增长贡献 | 月度 MQL 量 | 环比提升 20% |
| 洞察深度 | 竞品情报更新频率 | 从月度变为周度 |

### 10.3 常见阻力与应对策略

| 阻力类型 | 典型表现 | 应对策略 |
|---|---|---|
| "AI 写的内容没灵魂" | 团队对 AI 生成内容质量的不信任 | 强调 MGO 的定位是"骨架生成器 + 合规校验器"而非"替代创作者"，人工注入灵魂是流程的一部分 |
| "又多了一个工具" | 工具疲劳，不愿学习新系统 | 不要求学习新界面，MGO 通过自然语言交互，上手门槛极低；直接用自然语言描述需求即可 |
| "我的经验比 AI 准" | 资深员工的防御心理 | 让资深员工成为"知识库共建者"，他们的经验是 MGO 的燃料而非竞争者；主动邀请他们审核和校准知识库内容 |
| "数据不准" | 系统初期数据不足导致的输出质量问题 | 严格执行冷启动计划（见第九章），明确告知团队"系统需要 1-2 个月的数据积累期"，设定合理预期 |

---

## 十一、部署模式说明

### 11.1 两种部署模式对比

| 对比维度 | 本地单机模式（Local） | 团队协同模式（Team） |
|---|---|---|
| 适用场景 | 个人电脑，无内网环境，数据高度隐私 | 市场部全员使用，需共享数据，对接公司知识库和 CRM |
| 数据存储 | 所有路径指向本地文件夹 | `shared_path` 指向 NAS 共享文件夹 |
| 外部依赖 | 零依赖，安装即用 | 需配置 NAS 路径，可选对接 API 和向量数据库 |
| 典型用户 | 个人市场经理、小型团队 | 中大型市场部（5 人以上） |
| 特点 | 速度最快，隐私性最高 | 数据实时同步，多角色协作，符合企业合规 |

### 11.2 模式切换方式

在项目根目录的 `config.yaml` 中修改 `system.mode` 字段即可切换：

```yaml
# 本地单机模式
system:
  mode: "Local"

# 团队协同模式
system:
  mode: "Team"

# Team 模式下需额外配置以下字段：
team_mode:
  shared_path: "//NAS/Marketing"      # NAS 共享路径（必填）
  api_gateway: ""                      # 公司知识库 API（可选）
  vector_db_endpoint: ""               # 向量数据库 API（可选）
```

> **建议**：首次使用建议从 `Local` 模式开始，跑通核心闭环后，再根据团队规模决定是否切换至 `Team` 模式。
