# UTM 追踪标准与治理规范

> 来源参考：SpillwaveSolutions/running-marketing-campaigns-agent-skill

---

## 第1节：5 个 UTM 参数定义及格式规则

### 1.1 UTM 参数概述

UTM（Urchin Tracking Module）参数是附加在 URL 后的查询字符串，用于追踪营销活动的流量来源和效果。Google Analytics（GA4）通过读取这些参数来对流量进行分类和归因。

### 1.2 五个标准 UTM 参数

| 参数 | 英文名 | 必填性 | 定义 | 回答的问题 |
|------|--------|--------|------|-----------|
| utm_source | Source | **必填** | 流量来源平台/网站 | "流量从哪里来？" |
| utm_medium | Medium | **必填** | 营销媒介/渠道类型 | "通过什么方式来的？" |
| utm_campaign | Campaign | **必填** | 营销活动名称 | "哪个活动带来的？" |
| utm_term | Term | 选填 | 付费搜索关键词 | "用户搜了什么词？" |
| utm_content | Content | 选填 | 区分同一活动中的不同素材 | "用户点的是哪个素材？" |

### 1.3 各参数详解

**utm_source（来源）**
- 定义：产生流量的具体平台或网站
- 示例值：`google`、`baidu`、`linkedin`、`wechat`、`zhihu`、`newsletter`、`partner-abc`
- 易混淆点：source 是"谁发的"，不是"怎么发的"

**utm_medium（媒介）**
- 定义：营销渠道的类型/方式
- 示例值：`cpc`、`email`、`social`、`display`、`referral`、`affiliate`、`organic`
- 易混淆点：medium 是"什么方式"，是渠道的类型而非名称

**utm_campaign（活动）**
- 定义：具体的营销活动或促销名称
- 示例值：`spring-launch-2026`、`webinar-apr-growth`、`ebook-crm-guide`
- 命名应包含：活动类型-主题-时间

**utm_term（关键词）**
- 定义：付费搜索中用户点击的关键词
- 主要用于 SEM/搜索广告
- 在 Google Ads 中可用 ValueTrack 动态插入
- 示例值：`crm-software`、`best-saas-tools`

**utm_content（内容）**
- 定义：区分同一活动中不同的广告素材、链接位置或变体
- 示例值：`banner-top`、`cta-bottom`、`variant-a`、`red-button`
- 常用于 A/B 测试追踪

### 1.4 严格格式规则

| 规则 | 正确示例 | 错误示例 | 说明 |
|------|---------|---------|------|
| 全小写 | `utm_source=google` | `utm_source=Google` | GA4 区分大小写，大小写不一致会产生多个来源 |
| 用连字符分隔 | `utm_campaign=spring-launch-2026` | `utm_campaign=spring_launch_2026` | 连字符（-）是标准分隔符 |
| 无空格 | `utm_campaign=spring-launch` | `utm_campaign=spring launch` | 空格会被编码为 %20，破坏可读性 |
| 无特殊字符 | `utm_source=wechat` | `utm_source=微信` | 避免中文和特殊字符，使用英文等价词 |
| 无尾部斜杠 | `utm_content=banner-top` | `utm_content=banner-top/` | 尾部斜杠会导致归因错误 |
| 以 ? 开始 | `url.com?utm_source=google` | `url.com&utm_source=google` | 第一个参数前用 ?，后续用 & |
| URL 编码 | 仅在必要时编码 | 不编码特殊字符 | 确保浏览器正确解析 |

### 1.5 完整 UTM URL 示例

```
https://www.example.com/landing-page?utm_source=linkedin&utm_medium=social&utm_campaign=ebook-crm-guide-2026q2&utm_content=carousel-ad-variant-a
```

分解：
- 来源：linkedin（LinkedIn 平台）
- 媒介：social（社交媒体渠道类型）
- 活动：ebook-crm-guide-2026q2（CRM 指南电子书，2026年Q2活动）
- 内容：carousel-ad-variant-a（轮播广告 A 变体）

---

## 第2节：GA4 渠道对齐表

### 2.1 GA4 默认渠道分组（Default Channel Grouping）

GA4 根据 source 和 medium 的组合自动将流量归类到默认渠道分组。正确设置 UTM 参数可确保流量被 GA4 正确分类。

| GA4 默认渠道 | source 条件 | medium 条件 | 说明 |
|-------------|------------|-------------|------|
| Direct | (direct) | (none) | 直接访问，无 UTM 参数 |
| Organic Search | google, baidu, bing, etc. | organic | 自然搜索 |
| Paid Search | google, baidu, bing, etc. | cpc, ppc, paid-search | 付费搜索广告 |
| Display | 任意 | display, banner, cpm | 展示广告 |
| Social (Organic) | facebook, linkedin, twitter, weibo, etc. | social, social-media, social-network | 社交媒体自然流量 |
| Paid Social | facebook, linkedin, twitter, etc. | paid-social, paidsocial | 社交媒体付费广告 |
| Email | 任意 | email | 邮件营销 |
| Referral | 任意 | referral | 外部网站引荐 |
| Affiliate | 任意 | affiliate | 联盟营销 |
| Video | youtube, bilibili, etc. | video | 视频平台 |
| Audio | 任意 | audio | 音频/播客平台 |
| SMS | 任意 | sms | 短信营销 |

### 2.2 推荐的 source/medium 标准组合

**搜索引擎**：

| 平台 | utm_source | utm_medium（自然） | utm_medium（付费） |
|------|-----------|-------------------|-------------------|
| Google | google | organic | cpc |
| 百度 | baidu | organic | cpc |
| Bing | bing | organic | cpc |
| 360搜索 | so | organic | cpc |
| 搜狗 | sogou | organic | cpc |
| 神马搜索 | sm | organic | cpc |

**社交媒体**：

| 平台 | utm_source | utm_medium（自然） | utm_medium（付费） |
|------|-----------|-------------------|-------------------|
| LinkedIn | linkedin | social | paid-social |
| 微信公众号 | wechat-mp | social | paid-social |
| 微信朋友圈 | wechat-moments | social | paid-social |
| 企业微信 | wecom | social | N/A |
| 微博 | weibo | social | paid-social |
| 知乎 | zhihu | social | paid-social |
| 小红书 | xiaohongshu | social | paid-social |
| 抖音 | douyin | social | paid-social |
| B站 | bilibili | social | paid-social |
| Twitter/X | twitter | social | paid-social |
| Facebook | facebook | social | paid-social |

**邮件与直效渠道**：

| 渠道 | utm_source | utm_medium |
|------|-----------|-----------|
| 营销邮件 | newsletter 或 marketing-email | email |
| 事务性邮件 | transactional | email |
| 短信 | sms-provider 或 brand-name | sms |
| 企微消息 | wecom | im |
| 钉钉消息 | dingtalk | im |
| 飞书消息 | feishu | im |

**其他渠道**：

| 渠道 | utm_source | utm_medium |
|------|-----------|-----------|
| 合作伙伴 | partner-[name] | referral |
| 联盟营销 | affiliate-[name] | affiliate |
| PR/媒体 | [media-name] | referral |
| QR 码 | qr | offline |
| 线下活动 | event-[name] | offline |
| 播客 | [podcast-name] | audio |

### 2.3 避免 GA4 归因错误的关键规则

1. **不要混用 medium 值**：`cpc` 和 `CPC` 和 `ppc` 会被分到不同渠道
2. **使用 GA4 认可的 medium 值**：自定义 medium 会被归入"Unassigned"
3. **source 用平台名，medium 用渠道类型**：不要反过来
4. **社交平台的自然和付费必须区分**：`social` vs `paid-social`

---

## 第3节：平台动态参数宏

### 3.1 什么是动态参数宏

动态参数宏（Dynamic Parameter Macros）是广告平台提供的占位符变量，在用户点击广告时自动替换为实际值。这样可以自动化 UTM 标记，避免手动设置每个广告的 UTM 参数。

### 3.2 Meta（Facebook/Instagram）动态宏

| 宏 | 替换值 | 常用于 |
|----|--------|--------|
| `{{site_source_name}}` | facebook 或 instagram | utm_source |
| `{{campaign.name}}` | 广告系列名称 | utm_campaign |
| `{{adset.name}}` | 广告组名称 | utm_content |
| `{{ad.name}}` | 广告名称 | utm_content |
| `{{campaign.id}}` | 广告系列 ID | utm_campaign（备用） |
| `{{placement}}` | 展示位置（feed/stories 等） | utm_content |

**Meta UTM 模板**：
```
?utm_source={{site_source_name}}&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{adset.name}}-{{ad.name}}
```

### 3.3 Google Ads ValueTrack 参数

| 宏 | 替换值 | 常用于 |
|----|--------|--------|
| `{campaignid}` | 广告系列 ID | utm_campaign |
| `{campaign}` | 广告系列名称 | utm_campaign |
| `{adgroupid}` | 广告组 ID | utm_content |
| `{keyword}` | 触发关键词 | utm_term |
| `{matchtype}` | 匹配类型（e/p/b） | utm_term（附加） |
| `{network}` | 投放网络（g/s/d） | utm_content |
| `{device}` | 设备类型（m/t/c） | utm_content |
| `{creative}` | 广告创意 ID | utm_content |

**Google Ads UTM 模板**：
```
?utm_source=google&utm_medium=cpc&utm_campaign={campaign}&utm_term={keyword}&utm_content={adgroupid}-{creative}-{matchtype}-{device}
```

### 3.4 LinkedIn 广告参数

LinkedIn 不支持动态宏替换，需要在广告管理界面手动设置 UTM 参数，或使用 LinkedIn 的自定义参数功能。

**推荐方式**：
```
?utm_source=linkedin&utm_medium=paid-social&utm_campaign=[campaign-name]&utm_content=[ad-name]-[format]
```

LinkedIn Campaign Manager 支持在广告层级设置 URL 参数，建议：
- 在广告系列层级设置 source 和 medium
- 在广告层级设置 campaign 和 content
- 命名规则与内部一致

### 3.5 抖音/巨量引擎动态宏

| 宏 | 替换值 | 常用于 |
|----|--------|--------|
| `__CAMPAIGN_ID__` | 广告计划 ID | utm_campaign |
| `__CAMPAIGN_NAME__` | 广告计划名称 | utm_campaign |
| `__AID__` | 广告创意 ID | utm_content |
| `__CID__` | 广告组 ID | utm_content |
| `__CREATIVE_ID__` | 创意 ID | utm_content |
| `__OS__` | 操作系统 | utm_content（附加） |
| `__PTYPE__` | 出价类型 | 内部分析 |

**巨量引擎 UTM 模板**：
```
?utm_source=douyin&utm_medium=paid-social&utm_campaign=__CAMPAIGN_NAME__&utm_content=__AID__-__CREATIVE_ID__
```

**注意**：巨量引擎的宏使用双下划线包裹（`__XXX__`），与 Meta 的双花括号（`{{xxx}}`）和 Google 的单花括号（`{xxx}`）不同。

### 3.6 微信生态追踪方案

微信生态因其封闭性，UTM 追踪有特殊挑战：

**公众号菜单链接**：
```
?utm_source=wechat-mp&utm_medium=social&utm_campaign=menu-[menu-item-name]&utm_content=menu-bottom
```

**公众号文内链接**：
```
?utm_source=wechat-mp&utm_medium=social&utm_campaign=[article-title-slug]&utm_content=inline-link-[position]
```

**朋友圈广告**：
```
?utm_source=wechat-moments&utm_medium=paid-social&utm_campaign=[campaign-name]&utm_content=[creative-variant]
```

**企业微信消息**：
```
?utm_source=wecom&utm_medium=im&utm_campaign=[campaign-name]&utm_content=[message-type]
```

**微信小程序页面参数**：
- 小程序不支持标准 UTM，使用 `scene` 和自定义参数：
```
pages/landing?source=wechat-mp&campaign=spring-2026&channel=menu
```
- 需要在小程序端自行解析参数并上报到分析平台

---

## 第4节：QR 码追踪

### 4.1 QR 码 UTM 标准

QR 码用于连接线下场景与线上追踪，标准 UTM 配置：

```
utm_source=qr
utm_medium=offline
utm_campaign=[campaign-name]
utm_content=[placement-description]
```

### 4.2 按投放位置区分

| 投放场景 | utm_content 值 | 完整 URL 示例 |
|----------|---------------|-------------|
| 名片 | `business-card` | `?utm_source=qr&utm_medium=offline&utm_campaign=brand-2026&utm_content=business-card` |
| 展会展台 | `booth-[event-name]` | `?utm_source=qr&utm_medium=offline&utm_campaign=expo-2026&utm_content=booth-saas-summit` |
| 产品包装 | `packaging-[product]` | `?utm_source=qr&utm_medium=offline&utm_campaign=product-launch&utm_content=packaging-pro-plan` |
| 宣传册 | `brochure-[page]` | `?utm_source=qr&utm_medium=offline&utm_campaign=sales-kit&utm_content=brochure-page3` |
| 户外广告 | `billboard-[location]` | `?utm_source=qr&utm_medium=offline&utm_campaign=brand-awareness&utm_content=billboard-zhongguancun` |
| 线下活动 | `event-[name]` | `?utm_source=qr&utm_medium=offline&utm_campaign=meetup-apr&utm_content=event-registration` |
| 杂志/报纸 | `print-[publication]` | `?utm_source=qr&utm_medium=offline&utm_campaign=pr-2026q2&utm_content=print-36kr` |

### 4.3 QR 码追踪最佳实践

1. **每个投放位置使用独立 QR 码**：不要复用同一个 QR 码
2. **使用短链接服务**：QR 码内容越短，码越简洁易扫
   - 推荐工具：Bitly、短链宝、站长工具短链
3. **可更新的短链**：使用支持目标 URL 修改的短链服务，无需重新印刷 QR 码
4. **落地页适配移动端**：QR 码 99% 来自手机扫描
5. **测试 QR 码**：发印前在 3 种以上手机上测试扫描成功率

### 4.4 QR 码与短链的配合

```
原始 URL（太长，QR码密度高）：
https://www.example.com/landing?utm_source=qr&utm_medium=offline&utm_campaign=expo-2026&utm_content=booth-main

短链化：
https://link.example.com/expo2026

QR码指向短链，短链重定向到带完整UTM的原始URL
```

---

## 第5节：UTM 治理框架

### 5.1 治理的必要性

没有治理的 UTM 使用会导致：
- GA4 中出现数百个重复/无意义的来源和媒介
- 数据无法聚合分析（如 `Google`、`google`、`GOOGLE` 被识别为三个来源）
- 归因模型失效
- 跨团队数据不可比

### 5.2 团队文档模板

创建一份集中的 UTM 命名规范文档（UTM Naming Convention Document），包含：

```
# [公司名] UTM 追踪规范 v1.0

## 1. 通用规则
- 全小写
- 仅使用连字符（-）分隔
- 无空格、无下划线、无特殊字符
- 中文用英文等价词替代

## 2. 已批准的 source 列表
[见下方]

## 3. 已批准的 medium 列表
[见下方]

## 4. campaign 命名规则
[type]-[name]-[date]

## 5. content 命名规则
[format]-[variant]-[position]

## 6. 审批流程
新增 source/medium 需经 [负责人] 批准

## 7. 更新日志
[日期] [变更内容] [负责人]
```

### 5.3 已批准的 source 清单

维护一份公司级的已批准 source 值清单，禁止使用清单外的 source：

| 类别 | 已批准的 source 值 | 说明 |
|------|-------------------|------|
| 搜索引擎 | google, baidu, bing, so, sogou, sm | 各搜索引擎平台 |
| 社交平台（国际） | linkedin, twitter, facebook, instagram, youtube | 国际社交平台 |
| 社交平台（国内） | wechat-mp, wechat-moments, weibo, zhihu, xiaohongshu, douyin, bilibili | 国内社交平台 |
| IM 工具 | wecom, dingtalk, feishu | 企业 IM |
| 邮件 | newsletter, marketing-email, transactional | 邮件渠道 |
| 线下 | qr, event-[name], print-[name] | 线下渠道 |
| 合作伙伴 | partner-[name] | 合作方渠道 |
| 联盟 | affiliate-[name] | 联盟营销 |
| 其他 | podcast-[name], webinar, direct-mail | 其他渠道 |

### 5.4 已批准的 medium 清单

| medium 值 | 对应 GA4 渠道 | 适用场景 |
|-----------|-------------|---------|
| organic | Organic Search | 自然搜索（通常不手动标记） |
| cpc | Paid Search | 搜索广告 |
| social | Organic Social | 社交平台自然帖子 |
| paid-social | Paid Social | 社交平台付费广告 |
| email | Email | 邮件营销 |
| display | Display | 展示广告/横幅广告 |
| referral | Referral | 外部网站引荐 |
| affiliate | Affiliate | 联盟营销 |
| video | Video | 视频平台 |
| audio | Audio | 音频/播客 |
| sms | SMS | 短信营销 |
| im | 自定义 | 即时通讯（企微/钉钉等） |
| offline | 自定义 | 线下渠道（QR码/活动等） |

### 5.5 Campaign 命名规范

**格式**：`[type]-[name]-[date]`

| 组件 | 说明 | 示例值 |
|------|------|--------|
| type | 活动类型 | `ebook`、`webinar`、`launch`、`promo`、`nurture`、`retarget` |
| name | 活动主题（2-4 个词） | `crm-guide`、`spring-sale`、`product-update` |
| date | 时间标识 | `2026q2`、`202604`、`2026` |

**完整示例**：
- `ebook-crm-guide-2026q2`
- `webinar-growth-strategy-202604`
- `launch-v3-spring-2026`
- `promo-annual-plan-2026q2`
- `nurture-trial-users-202604`

### 5.6 月度审计清单

每月执行一次 UTM 数据质量审计：

**审计步骤**：

1. **导出 GA4 来源/媒介报告**
   - GA4 → 报告 → 流量获取 → 流量获取概览
   - 导出所有 source/medium 组合

2. **检查项**：
   - [ ] 是否有大小写不一致的 source（如 `Google` vs `google`）
   - [ ] 是否有未批准的 source 值
   - [ ] 是否有大小写不一致的 medium
   - [ ] 是否有 source/medium 互换的情况
   - [ ] 是否有包含空格的参数值
   - [ ] 是否有 "(not set)" 占比异常高的渠道
   - [ ] 是否有 "Unassigned" 渠道占比异常高
   - [ ] campaign 命名是否符合规范

3. **修正行动**：
   - 在 GA4 中使用"数据过滤器"修正历史数据（有限支持）
   - 通知相关团队成员修正 UTM 配置
   - 更新并重新分发 UTM 规范文档

---

## 第6节：常见错误矩阵

### 6.1 高频 UTM 错误及修正

| # | 错误类型 | 错误示例 | 影响 | 正确做法 |
|---|---------|---------|------|---------|
| 1 | 大小写不一致 | `utm_source=Google` vs `utm_source=google` | GA4 识别为两个不同来源，数据分裂 | 全部使用小写 |
| 2 | 使用空格 | `utm_campaign=spring launch` | URL 中空格被编码为 %20，可读性差且可能导致截断 | 使用连字符：`spring-launch` |
| 3 | source/medium 互换 | `utm_source=cpc&utm_medium=google` | GA4 渠道分组错误，Paid Search 无法正确识别 | source=平台名，medium=渠道类型 |
| 4 | 内部链接打 UTM | 站内链接添加 UTM 参数 | **严重**：覆盖原始归因，所有后续转化归因到内部链接 | 站内链接永远不加 UTM |
| 5 | 缺少 ? 号 | `url.com&utm_source=google` | URL 参数无法被正确解析 | 第一个参数前用 ? |
| 6 | 重复 ? 号 | `url.com?page=1?utm_source=google` | 第二个 ? 后的参数可能不被识别 | 只用一个 ?，后续参数用 & |
| 7 | 使用下划线分隔 | `utm_campaign=spring_launch_2026` | 与连字符分隔的同名活动不一致 | 统一使用连字符 |
| 8 | 使用中文值 | `utm_source=微信` | URL 编码问题、跨系统兼容性差 | 使用英文等价词：`wechat` |
| 9 | 缺少必填参数 | 只设置了 utm_source 没有 utm_medium | GA4 可能归入 "Unassigned" | source+medium+campaign 全部设置 |
| 10 | 尾部斜杠 | `utm_content=banner/` | 与不带斜杠的值被识别为不同内容 | 去掉尾部斜杠 |

### 6.2 错误影响评估

| 严重度 | 错误类型 | 影响范围 | 是否可修复 |
|--------|---------|---------|-----------|
| 致命 | 内部链接打 UTM | 破坏所有归因数据 | 历史数据不可修复 |
| 高 | source/medium 互换 | 渠道分组完全错误 | 需在 GA4 手动处理 |
| 中 | 大小写不一致 | 数据分裂，无法聚合 | 可在报表层合并 |
| 中 | 缺少必填参数 | 流量归入 Unassigned | 修正后新数据正确 |
| 低 | 命名不规范 | 可读性差，分析效率低 | 可在报表层映射 |

### 6.3 防错机制

1. **UTM 构建工具**：使用统一的 UTM 生成器（Excel 模板或 Web 工具），预设 source/medium 下拉选项
2. **URL 验证脚本**：在发布前自动检查 UTM 格式
3. **GA4 数据过滤器**：设置小写过滤器自动将 source/medium 转为小写
4. **团队培训**：新成员入职时进行 UTM 规范培训
5. **审批流程**：新的广告活动 UTM 需经审批后使用

---

## 第7节：中国特色追踪补充

### 7.1 微信生态无法直接传 UTM 的替代方案

**挑战**：微信内浏览器对外部链接有诸多限制，且微信公众号文章内无法直接嵌入带 UTM 的外部链接（会被微信屏蔽或限流）。

**替代方案**：

| 场景 | 追踪方法 | 实现方式 |
|------|---------|---------|
| 公众号菜单链接 | 短链+UTM | 使用短链服务包装带 UTM 的链接 |
| 公众号文内链接 | 阅读原文+UTM | "阅读原文"链接可带完整 UTM |
| 公众号文内链接 | 小程序码 | 跳转小程序，小程序内传参数 |
| 企微消息链接 | 短链+UTM | 企微支持外部链接，可带 UTM |
| 朋友圈分享 | 短链+UTM | 分享链接中嵌入 UTM |
| 微信群消息 | 短链+UTM | 短链服务包装 |
| 企微侧边栏 | 短链+UTM | 侧边栏内容嵌入追踪链接 |

**公众号阅读原文追踪示例**：
```
阅读原文 URL：
https://link.example.com/apr-article
→ 重定向到：
https://www.example.com/landing?utm_source=wechat-mp&utm_medium=social&utm_campaign=article-crm-guide-202604&utm_content=read-more
```

### 7.2 小程序码追踪

**小程序 scene 参数方案**：

微信小程序通过 `scene` 参数（扫码场景值）和自定义参数实现追踪。

```
小程序码参数：
pages/landing?scene=wechat-mp-menu-202604

参数解析规则：
scene 格式：[source]-[medium]-[campaign]
wechat-mp  →  source: wechat-mp
menu       →  content: menu
202604     →  campaign: 202604
```

**小程序端解析代码**：
```javascript
// app.js 或 landing page
onLoad(options) {
  if (options.scene) {
    const scene = decodeURIComponent(options.scene);
    const parts = scene.split('-');
    // 解析为追踪参数
    const trackingData = {
      source: parts.slice(0, 2).join('-'), // wechat-mp
      content: parts[2],                    // menu
      campaign: parts[3]                    // 202604
    };
    // 上报到分析平台
    this.reportTracking(trackingData);
  }
}
```

**小程序码类型与追踪**：

| 小程序码类型 | 参数限制 | 追踪建议 |
|-------------|---------|---------|
| 普通二维码 | 无限制 | 直接在 URL 中传参 |
| 小程序码（有限） | scene 最多 32 字符 | 使用编码压缩方案 |
| 小程序码（无限） | scene 最多 32 字符 | 使用服务端映射表 |

### 7.3 企微渠道活码追踪

**什么是企微渠道活码**：
企业微信的"渠道活码"功能允许为每个渠道生成独立二维码，扫码后自动添加企微好友并标记渠道来源。

**追踪方案**：

| 步骤 | 操作 | 追踪信息 |
|------|------|---------|
| 1. 创建渠道活码 | 企微后台 → 客户联系 → 渠道活码 | 渠道名称 = utm_source+utm_medium |
| 2. 命名规范 | `[source]-[medium]-[campaign]-[content]` | 与 UTM 命名一致 |
| 3. 设置标签 | 自动打标签 = 渠道来源 | 后续分析用 |
| 4. 部署 | 投放到各渠道 | 每个位置一个活码 |
| 5. 数据回流 | 企微数据导出 → CRM/分析平台 | 打通线上线下归因 |

**企微活码命名示例**：

| 投放场景 | 活码名称 | 自动标签 |
|----------|---------|---------|
| 公众号底部 | `wechat-mp-social-article-footer` | 公众号-文章 |
| 知乎回答 | `zhihu-social-answer-crm-guide` | 知乎-CRM |
| 线下展会 | `qr-offline-expo-saas-summit-2026` | 展会-SaaS |
| 百度 SEM | `baidu-cpc-crm-landing` | 百度搜索-CRM |
| 朋友圈广告 | `wechat-moments-paid-social-spring` | 朋友圈-春季 |

### 7.4 微信生态全链路追踪架构

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│  公众号文章   │   │  朋友圈广告    │   │  企微消息     │
│  (阅读原文    │   │  (落地页链接   │   │  (短链+UTM   │
│   +UTM)      │   │   +UTM)       │   │   追踪)       │
└──────┬───────┘   └──────┬────────┘   └──────┬───────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌──────────────────────────────────────────────────────┐
│                  短链服务 / 落地页                      │
│           (解析 UTM → 传递到分析平台)                   │
└──────────────────────────┬───────────────────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌──────────┐       ┌──────────┐       ┌──────────────┐
│  GA4     │       │  百度统计  │       │  企微 CRM     │
│  (网站   │       │  (网站    │       │  (客户归因    │
│   归因)  │       │   归因)   │       │   +跟进)      │
└──────────┘       └──────────┘       └──────────────┘
                           │
                           ▼
                   ┌──────────────┐
                   │  数据中台/BI   │
                   │  (全渠道归因   │
                   │   分析报表)    │
                   └──────────────┘
```

### 7.5 中国市场追踪工具推荐

| 工具 | 类型 | 主要用途 | 是否支持 UTM |
|------|------|---------|-------------|
| 百度统计 | 网站分析 | 百度搜索归因 | 支持 |
| 友盟+ | 全平台分析 | 多端数据打通 | 支持 |
| 神策数据 | 用户行为分析 | 事件追踪+归因 | 支持 |
| GrowingIO | 增长分析 | 无埋点+UTM | 支持 |
| 易观方舟 | 用户分析 | 全渠道追踪 | 支持 |
| GA4 | 网站分析 | 全球标准 | 原生支持 |

---

## 附录：UTM 构建器模板

### Excel/Google Sheets UTM 构建器

创建一个标准化的 UTM 构建器表格：

| 列 | 内容 | 数据验证 |
|----|------|---------|
| A: 目标 URL | 落地页地址 | URL 格式验证 |
| B: utm_source | 来源 | 下拉选择（已批准清单） |
| C: utm_medium | 媒介 | 下拉选择（已批准清单） |
| D: utm_campaign | 活动名 | 格式验证：[type]-[name]-[date] |
| E: utm_term | 关键词 | 自由输入（可选） |
| F: utm_content | 内容 | 自由输入（可选） |
| G: 完整 URL | 自动生成 | 公式拼接 |
| H: 短链 | 短链地址 | 手动填入 |

**G 列公式（Google Sheets）**：
```
=A2&"?utm_source="&LOWER(B2)&"&utm_medium="&LOWER(C2)&"&utm_campaign="&LOWER(D2)&IF(E2<>"","&utm_term="&LOWER(E2),"")&IF(F2<>"","&utm_content="&LOWER(F2),"")
```

---

## 附录：UTM 术语表

| 术语 | 英文全称 | 定义 |
|------|----------|------|
| UTM | Urchin Tracking Module | 用于追踪营销活动流量来源的 URL 参数标准 |
| GA4 | Google Analytics 4 | Google 的网站分析平台（第 4 代） |
| Source | Traffic Source | 流量来源平台 |
| Medium | Marketing Medium | 营销渠道类型 |
| Campaign | Marketing Campaign | 营销活动名称 |
| ValueTrack | Google Ads ValueTrack | Google Ads 的动态参数替换机制 |
| Dunning | N/A | 本文件不涉及，见 churn-prevention-playbook.md |
| Short URL | Short URL / URL Shortener | 短链接服务，用于压缩长 URL |
| QR Code | Quick Response Code | 二维码，用于连接线下与线上 |
| Channel Grouping | Default Channel Grouping | GA4 对流量的自动分类 |
| Attribution | Marketing Attribution | 营销归因，追踪转化的来源渠道 |

---

> 文件版本：v1.1.0 | 最后更新：2026-04
