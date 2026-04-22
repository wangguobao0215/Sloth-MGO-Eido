#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sloth-MGO-Eido 知识库目录初始化脚本

功能：自动创建设计方案中定义的完整工作区目录结构，包括：
  - 00_Shared 共享知识库及其 7 个子分区
  - Module_A 到 Module_G 的各模块工作区及子目录
  - config.yaml 配置文件占位

用法：
  python init_workspace.py /path/to/marketing_os_root
  python init_workspace.py .  # 在当前目录初始化

作者：Sloth-MGO-Eido
版本：1.0.0
"""

import argparse
import os
import sys
from pathlib import Path


# ============================================================
# 目录结构定义
# ============================================================

# 完整的工作区目录结构，按照设计方案第七章定义
WORKSPACE_STRUCTURE = {
    # 共享知识库
    "00_Shared": {
        "01_Product_Data": {},                          # 产品白皮书、功能文档、参数表
        "02_Brand_Assets": {},                          # 品牌VI、Logo、禁用词表、广告法合规规则
        "03_Competitor_Intel": {},                      # 竞品攻防卡、竞品画像
        "04_Voice_of_Customer": {
            "raw_feedback": {},                         # 原始反馈记录
        },
        "05_Best_Practices": {},                        # 历史高转化案例、SOP、实验结论
        "06_Industry_Intel": {},                        # 行业情报、政策法规
        "07_Growth_Metrics": {
            "monthly_reports": {},                      # 历史月度报告
        },
    },
    # Module A：内容引擎工作区
    "Module_A_Content": {
        "drafts": {},                                   # 内容草稿
        "published": {},                                # 已发布内容归档
        "templates": {},                                # 内容模板
    },
    # Module B：活动指挥工作区
    "Module_B_Campaign": {
        "plans": {},                                    # 策划案
        "rundowns": {},                                 # 执行总控表
        "reviews": {},                                  # 复盘报告
    },
    # Module C：情报中心工作区
    "Module_C_Intel": {
        "monitor": {},                                  # 监听原始数据
        "reports": {},                                  # 分析报告
        "battle_cards_draft": {},                       # 作战卡草稿（入库前暂存）
    },
    # Module D：线索引擎工作区
    "Module_D_Leads": {
        "input": {},                                    # 原始线索表（Excel/CSV）
        "scored": {},                                   # 清洗打分后的分级表
        "nurture_sequences": {},                        # 培育序列
        "feedback": {},                                 # 销售反馈记录
    },
    # Module E：渠道分发工作区
    "Module_E_Channel": {
        "adapted": {},                                  # 各渠道适配版本
        "seo": {},                                      # SEO 内容和关键词
        "ads": {},                                      # 投放素材
    },
    # Module F：客户增长工作区
    "Module_F_Customer": {
        "onboarding": {},                               # 欢迎序列
        "health_reports": {},                           # 健康度报告
        "case_studies": {},                             # 案例素材
        "nps": {},                                      # NPS 分析
    },
    # Module G：增长度量工作区
    "Module_G_Metrics": {
        "dashboards": {},                               # 看板数据
        "experiments": {},                              # A/B 实验记录
        "attribution": {},                              # 归因分析
    },
}

# config.yaml 的默认内容
CONFIG_YAML_CONTENT = """\
# config.yaml - Sloth-MGO-Eido 配置文件
# 由 init_workspace.py 自动生成，请根据实际情况修改

system:
  mode: "Local"                    # Local | Team
  language: "zh-CN"                # 系统默认语言

paths:
  knowledge_base: "./00_Shared"    # 共享知识库路径
  workspace_root: "./"             # 工作区根目录

team_mode:                         # 仅 Team 模式下生效
  shared_path: ""                  # NAS 共享路径
  api_gateway: ""                  # 公司知识库 API（可选）
  vector_db_endpoint: ""           # 向量数据库 API（可选）

modules:
  enabled:
    - content_engine                # Module A
    - campaign_command              # Module B
    - market_intel                  # Module C
    - lead_engine                   # Module D
    - channel_distribution          # Module E
    - customer_growth               # Module F
    - growth_metrics                # Module G

  content_engine:
    compliance_level: "standard"   # standard | strict
    default_content_types:
      - article
      - case_study
      - whitepaper

  lead_engine:
    scoring_weights:
      profile_match: 0.30
      behavior_signal: 0.30
      need_clarity: 0.25
      recency: 0.15
    hot_threshold: 80
    handoff_sla_hours: 48

  customer_growth:
    health_score_enabled: true
    nps_survey_enabled: true
    renewal_alert_days: [90, 60, 30]

  growth_metrics:
    attribution_model: "multi_touch"
    report_frequency: "monthly"

integrations:
  wechat_work: false
  wechat_mp: false
  feishu: false
  crm_api: ""

compliance:
  advertising_law: true
  pipl: true
  industry_rules: ""
"""

# 共享知识库中的占位文件及其内容
PLACEHOLDER_FILES = {
    "00_Shared/03_Competitor_Intel/competitor_landscape.md": (
        "# 竞品全景图\n\n"
        "> 本文件记录所有已识别竞品的全景概览，由 Module C 维护更新。\n\n"
        "## 竞品列表\n\n"
        "| 竞品名称 | 市场定位 | 威胁等级 | 最近更新 |\n"
        "|---|---|---|---|\n"
        "| （待填充） | | | |\n"
    ),
    "00_Shared/04_Voice_of_Customer/voc_summary.md": (
        "# 客户之声（VoC）分析摘要\n\n"
        "> 本文件汇总客户反馈的核心洞察，由 Module C 和 Module F 共同维护。\n\n"
        "## 核心发现\n\n"
        "（待填充：客户最关注的痛点、需求偏移趋势等）\n"
    ),
    "00_Shared/05_Best_Practices/content_playbook.md": (
        "# 内容最佳实践手册\n\n"
        "> 记录历史高转化内容的经验总结，供 Module A 参考。\n\n"
        "## 最佳实践清单\n\n"
        "（待填充：高转化内容的共同特征、推荐写作框架等）\n"
    ),
    "00_Shared/05_Best_Practices/channel_playbook.md": (
        "# 渠道最佳实践手册\n\n"
        "> 记录各渠道的运营经验，供 Module E 参考。\n\n"
        "## 渠道实践清单\n\n"
        "（待填充：各渠道的最佳发布时间、内容格式建议等）\n"
    ),
    "00_Shared/05_Best_Practices/experiment_log.md": (
        "# 实验结论库\n\n"
        "> 记录所有 A/B 实验的结论，由 Module G 自动写入。\n\n"
        "## 实验记录\n\n"
        "| 实验ID | 实验名称 | 结论 | 日期 |\n"
        "|---|---|---|---|\n"
        "| （待填充） | | | |\n"
    ),
    "00_Shared/07_Growth_Metrics/benchmarks.md": (
        "# 增长指标基准数据\n\n"
        "> 记录 CAC/LTV/转化率等核心指标的基准值，供 Module G 和风控使用。\n\n"
        "## 基准指标\n\n"
        "| 指标 | 基准值 | 数据来源 | 更新日期 |\n"
        "|---|---|---|---|\n"
        "| （待填充） | | | |\n"
    ),
}


# ============================================================
# 核心函数
# ============================================================

def create_directory_tree(root_path: Path, structure: dict, created_dirs: list) -> None:
    """
    递归创建目录结构。

    参数:
        root_path: 当前递归的根目录路径
        structure: 目录结构字典，键为目录名，值为子目录结构字典
        created_dirs: 已创建的目录列表（用于统计和输出）
    """
    for dir_name, sub_structure in structure.items():
        dir_path = root_path / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(dir_path))
        # 递归创建子目录
        if sub_structure:
            create_directory_tree(dir_path, sub_structure, created_dirs)


def create_placeholder_files(root_path: Path, created_files: list) -> None:
    """
    在共享知识库中创建占位文件。

    参数:
        root_path: 工作区根目录路径
        created_files: 已创建的文件列表（用于统计和输出）
    """
    for relative_path, content in PLACEHOLDER_FILES.items():
        file_path = root_path / relative_path
        if not file_path.exists():
            # 确保父目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            created_files.append(str(file_path))


def create_config_file(root_path: Path, created_files: list) -> None:
    """
    创建 config.yaml 配置文件。

    参数:
        root_path: 工作区根目录路径
        created_files: 已创建的文件列表（用于统计和输出）
    """
    config_path = root_path / "config.yaml"
    if not config_path.exists():
        config_path.write_text(CONFIG_YAML_CONTENT, encoding="utf-8")
        created_files.append(str(config_path))


def print_directory_tree(root_path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> None:
    """
    打印目录树结构（类似 tree 命令的输出）。

    参数:
        root_path: 要打印的根目录路径
        prefix: 当前行的前缀字符（用于缩进）
        max_depth: 最大显示深度
        current_depth: 当前递归深度
    """
    if current_depth >= max_depth:
        return

    # 获取目录内容并排序（目录优先，然后按名称排序）
    try:
        entries = sorted(root_path.iterdir(), key=lambda e: (not e.is_dir(), e.name))
    except PermissionError:
        return

    # 过滤隐藏文件
    entries = [e for e in entries if not e.name.startswith(".")]

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        # 目录名后面加 /
        display_name = f"{entry.name}/" if entry.is_dir() else entry.name
        print(f"{prefix}{connector}{display_name}")

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_directory_tree(entry, prefix + extension, max_depth, current_depth + 1)


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：解析参数并执行工作区初始化。"""

    parser = argparse.ArgumentParser(
        description="Sloth-MGO-Eido 知识库目录初始化脚本",
        epilog="示例：python init_workspace.py /path/to/marketing_os_root",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "root_dir",
        type=str,
        help="工作区根目录路径（将在此目录下创建完整的 MGO 目录结构）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="即使目录已存在也继续执行（仅补建缺失的目录和文件，不覆盖已有内容）",
    )
    parser.add_argument(
        "--no-placeholders",
        action="store_true",
        default=False,
        help="不创建占位文件（仅创建目录结构）",
    )
    parser.add_argument(
        "--no-config",
        action="store_true",
        default=False,
        help="不创建 config.yaml 配置文件",
    )
    parser.add_argument(
        "--tree-depth",
        type=int,
        default=4,
        help="目录树显示深度（默认: 4）",
    )

    args = parser.parse_args()

    # 解析根目录路径
    root_path = Path(args.root_dir).resolve()

    # 检查根目录是否已存在且包含内容
    if root_path.exists() and any(root_path.iterdir()) and not args.force:
        print(f"[警告] 目录 '{root_path}' 已存在且非空。")
        print(f"       如果要在已有目录中补建缺失结构，请使用 --force 参数。")
        print(f"       用法：python init_workspace.py {args.root_dir} --force")
        sys.exit(1)

    # 创建根目录（如果不存在）
    root_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  Sloth-MGO-Eido 知识库目录初始化")
    print("=" * 60)
    print(f"\n工作区根目录：{root_path}\n")

    # 统计列表
    created_dirs = []
    created_files = []

    # Step 1：创建目录结构
    print("[1/3] 正在创建目录结构...")
    create_directory_tree(root_path, WORKSPACE_STRUCTURE, created_dirs)
    print(f"      完成。新建 {len(created_dirs)} 个目录。")

    # Step 2：创建占位文件
    if not args.no_placeholders:
        print("[2/3] 正在创建知识库占位文件...")
        create_placeholder_files(root_path, created_files)
        print(f"      完成。新建 {len(created_files)} 个占位文件。")
    else:
        print("[2/3] 跳过占位文件创建（--no-placeholders）。")

    # Step 3：创建配置文件
    if not args.no_config:
        print("[3/3] 正在创建 config.yaml 配置文件...")
        create_config_file(root_path, created_files)
        print(f"      完成。")
    else:
        print("[3/3] 跳过配置文件创建（--no-config）。")

    # 输出统计
    print(f"\n{'=' * 60}")
    print(f"  初始化完成！")
    print(f"  新建目录：{len(created_dirs)} 个")
    print(f"  新建文件：{len(created_files)} 个")
    print(f"{'=' * 60}")

    # 打印目录树
    print(f"\n目录结构预览（深度 {args.tree_depth}）：\n")
    print(f"{root_path.name}/")
    print_directory_tree(root_path, max_depth=args.tree_depth)

    # 给出下一步指引
    print(f"\n{'─' * 60}")
    print("下一步操作建议：")
    print(f"  1. 编辑 config.yaml 配置企业信息和模块偏好")
    print(f"  2. 在 00_Shared/01_Product_Data/ 中放入产品文档")
    print(f"  3. 在 00_Shared/02_Brand_Assets/ 中放入品牌规范和禁用词表")
    print(f"  4. 在 00_Shared/04_Voice_of_Customer/raw_feedback/ 中放入客户反馈数据")
    print(f"  5. 运行 lead_scoring.py 进行线索评分")
    print(f"{'─' * 60}")


if __name__ == "__main__":
    main()
