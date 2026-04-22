<p align="center">
  <img src="assets/sloth-avatar-round.png" width="120" />
</p>

<h1 align="center">Sloth-MGO-Eido</h1>

<p align="center">
  <strong>Marketing Growth Operations AI Agent</strong><br/>
  An AI-powered full-loop marketing operations system for B2B SaaS companies, covering market intelligence, content creation, channel distribution, lead nurturing, customer lifecycle growth, and growth analytics.
</p>

<p align="center">
  <img src="assets/qrcode.jpg" width="140" /><br/>
  <sub>Follow <strong>树懒老K</strong> · Get more AI Skills</sub><br/>
  <em>Slow down, go deeper</em>
</p>

---

## Feature Overview

Sloth-MGO-Eido uses a **1+7 parent-child architecture**, with one parent Skill (commander) orchestrating seven sub-modules:

| Module | Name | Core Capabilities |
|--------|------|-------------------|
| **A** | Content & Creative Engine | Product articles, whitepapers, case studies, comparison articles, EDM templates with built-in value validation and competitive positioning |
| **B** | Campaign & Project Command | Campaign planning, execution rundowns, budget management, vendor comparison, cross-module project tracking |
| **C** | Market Intelligence Center | Competitor monitoring, industry trend tracking, customer demand analysis, category opportunity discovery, Battle Card generation |
| **D** | Lead Nurturing & Conversion Engine | Lead scoring, nurture sequence orchestration, sales enablement, two-way market-sales feedback, win/loss analysis |
| **E** | Channel Distribution & Acquisition | Multi-channel content adaptation (WeChat/Zhihu/Toutiao/Xiaohongshu/LinkedIn/EDM), SEO optimization, ABM support |
| **F** | Customer Lifecycle Growth | Onboarding support, health monitoring, renewal/expansion marketing, case study collection, NPS analysis |
| **G** | Growth Metrics & Experimentation | North Star metrics dashboard, attribution analysis, A/B testing framework, ROI review, budget recommendations |

Key Features:

- **Growth Flywheel Model** -- Customer advocacy and case studies fuel new acquisition, building momentum with each cycle
- **Three-tier Risk Control** -- L1 lightweight / L2 standard / L3 full, tiered validation to avoid blocking daily operations
- **Built-in Compliance Engine** -- Multi-layer compliance checks for advertising law, PIPL, brand guidelines, and industry-specific rules
- **Hybrid Knowledge Adapter** -- Three-tier retrieval: local folders + knowledge base API + vector database
- **Cross-module Context Passing** -- Automatic data flow between modules: intelligence drives content, content drives distribution

## Quick Start

### Installation

1. Install the Sloth-MGO-Eido skill in QoderWork
2. The system will automatically guide you through configuration on first use (company info, competitor list, module preferences, etc.)
3. You can also pre-fill the `EXTEND.md` file with your personalized configuration

### Minimal Working Example

```
User: Write a product comparison article against Competitor A

MGO execution chain:
  1. Module C (Market Intel) -> Fetch latest intel on Competitor A
  2. Module A (Content Engine) -> Write comparison article master copy
  3. Prompt user whether Module E (Channel Distribution) should adapt for platforms
```

```
User: Clean up the lead list from last week's event

MGO execution chain:
  1. Module D (Lead Engine) -> Clean, deduplicate, score, and tier
  2. Hot leads flagged for priority follow-up with lead intel cards
  3. B/C tier leads automatically assigned nurture sequences
```

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
|              Sloth-MGO-Eido (Parent Skill -- Commander)    |
|                                                          |
|   Intent -> Risk Control -> Knowledge -> Routing -> Merge |
└────┬─────┬─────┬──────┬──────┬──────┬──────┬─────────────┘
     |     |     |      |      |      |      |
     v     v     v      v      v      v      v
   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
   | A | | B | | C | | D | | E | | F | | G |
   |Con-| |Cam-| |Int-| |Lea-| |Cha-| |Cus-| |Met-|
   |tent| |paig| |el  | |ds  | |nnel| |tmer| |rics|
   └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘
```

- **Parent Skill**: Single interaction entry point, responsible for intent recognition, risk control, knowledge injection, module routing, and cross-module context passing
- **Sub-modules A-G**: Stateless executors, each with independent role definitions, workflows, and output specifications

## Version

Current version: **1.1.0** (General Availability)

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

## License

[MIT License](LICENSE)

## Related Skills

| Skill | Integration |
|-------|------------|
| [Sloth-Sales-Eido](https://github.com/wangguobao0215/Sloth-Sales-Eido) | Two-way bridge: leads pushed to CRM, sales feedback flows back to content/intel modules |
| [Sloth-PSC-Eido](https://github.com/wangguobao0215/Sloth-PSC-Eido) | Competitive intel feeds into pre-sales analysis; solution frameworks generate marketing content |
| [Sloth-SMM-Eido](https://github.com/wangguobao0215/Sloth-SMM-Eido) | Master articles flow into social media publishing; trending data feeds back to intel |
| [Agent-Reach](https://github.com/wangguobao0215/agent-reach) | 17-platform deep search enhances intel gathering, lead enrichment, and customer monitoring |
