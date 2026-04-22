#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sloth-MGO-Eido 线索评分计算脚本

功能：读取 CSV 格式的线索数据，按照四维评分模型计算线索综合分数并进行分级。

评分维度（默认权重）：
  - 企业画像匹配度 (profile_match):  30%
  - 行为信号强度 (behavior_signal):  30%
  - 需求明确度 (need_clarity):       25%
  - 时效性 (recency):                15%

分级规则：
  - H (Hot):   80-100 分 → 48h 内交付销售
  - A:         70-79 分  → 7 天内培育后交付
  - B:         50-69 分  → 进入培育序列
  - C:         < 50 分   → 存档观察

用法：
  python lead_scoring.py -i leads.csv -o scored_leads.csv
  python lead_scoring.py -i leads.csv -o scored.csv --w-profile 0.35 --w-behavior 0.25
  python lead_scoring.py -i leads.csv --summary

作者：Sloth-MGO-Eido
版本：1.0.0
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# 常量定义
# ============================================================

# 默认评分权重
DEFAULT_WEIGHTS = {
    "profile_match": 0.30,
    "behavior_signal": 0.30,
    "need_clarity": 0.25,
    "recency": 0.15,
}

# 分级阈值
GRADE_THRESHOLDS = {
    "H": 80,  # Hot: >= 80
    "A": 70,  # A级: >= 70
    "B": 50,  # B级: >= 50
    # C级: < 50
}

# 分级说明
GRADE_DESCRIPTIONS = {
    "H": "Hot — 48h内交付销售",
    "A": "A级 — 7天内培育后交付",
    "B": "B级 — 进入培育序列",
    "C": "C级 — 存档观察",
}

# CSV 输入文件必需的列（四维原始分数列名）
REQUIRED_SCORE_COLUMNS = [
    "profile_match_score",
    "behavior_signal_score",
    "need_clarity_score",
    "recency_score",
]

# 企业画像匹配度的评分映射规则
INDUSTRY_MATCH_MAP = {
    "exact": 100,       # 完全匹配目标行业
    "related": 70,      # 相关行业
    "partial": 40,      # 部分相关
    "none": 10,         # 不匹配
}

COMPANY_SIZE_MATCH_MAP = {
    "ideal": 100,       # 理想规模范围
    "acceptable": 70,   # 可接受范围
    "small": 40,        # 偏小
    "large": 40,        # 偏大
    "mismatch": 10,     # 不匹配
}

# 行为信号强度的评分规则
BEHAVIOR_WEIGHTS = {
    "content_download": 25,     # 内容下载（每次加分，上限25）
    "event_participation": 30,  # 活动参与（每次加分，上限30）
    "website_visit": 20,        # 网站高价值页面访问（每次加分，上限20）
    "email_interaction": 15,    # 邮件互动（每次加分，上限15）
    "form_submission": 10,      # 表单提交（有则得分）
}

# 需求明确度的评分规则
NEED_CLARITY_LEVELS = {
    "explicit_budget_timeline": 100,   # 明确预算和时间线
    "explicit_need": 80,               # 明确需求但无预算
    "implied_need": 60,                # 暗示需求
    "exploring": 40,                   # 探索阶段
    "unknown": 20,                     # 需求不明
}

# 时效性评分规则（基于最近互动天数）
RECENCY_DECAY = [
    (3, 100),       # 3天内互动: 100分
    (7, 90),        # 7天内互动: 90分
    (14, 75),       # 14天内互动: 75分
    (30, 55),       # 30天内互动: 55分
    (60, 35),       # 60天内互动: 35分
    (90, 20),       # 90天内互动: 20分
    (float("inf"), 5),  # 超过90天: 5分
]


# ============================================================
# 评分函数
# ============================================================

def calculate_recency_score(days_since_last_interaction: int) -> float:
    """
    根据最近互动天数计算时效性得分。

    参数:
        days_since_last_interaction: 距离最近一次互动的天数

    返回:
        时效性得分（0-100）
    """
    for threshold_days, score in RECENCY_DECAY:
        if days_since_last_interaction <= threshold_days:
            return score
    return 5  # 兜底分数


def calculate_weighted_score(scores: dict, weights: dict) -> float:
    """
    计算加权总分。

    参数:
        scores: 四维原始分数字典，键为维度名，值为 0-100 的原始分
        weights: 权重字典，键为维度名，值为权重（0-1之间，合计为1）

    返回:
        加权总分（0-100）
    """
    total = 0.0
    for dimension, weight in weights.items():
        raw_score = scores.get(dimension, 0)
        # 确保原始分在 0-100 范围内
        raw_score = max(0, min(100, float(raw_score)))
        total += raw_score * weight
    return round(total, 2)


def determine_grade(total_score: float) -> str:
    """
    根据总分确定线索等级。

    参数:
        total_score: 加权总分（0-100）

    返回:
        等级字符串："H"、"A"、"B" 或 "C"
    """
    if total_score >= GRADE_THRESHOLDS["H"]:
        return "H"
    elif total_score >= GRADE_THRESHOLDS["A"]:
        return "A"
    elif total_score >= GRADE_THRESHOLDS["B"]:
        return "B"
    else:
        return "C"


def validate_weights(weights: dict) -> bool:
    """
    校验权重合法性：所有权重为正数且合计为 1.0（允许浮点误差）。

    参数:
        weights: 权重字典

    返回:
        是否合法
    """
    for key, value in weights.items():
        if value < 0 or value > 1:
            print(f"[错误] 权重 '{key}' 的值 {value} 不在 [0, 1] 范围内。")
            return False
    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        print(f"[错误] 权重合计为 {total:.4f}，应接近 1.0。")
        return False
    return True


# ============================================================
# CSV 处理函数
# ============================================================

def read_leads_csv(input_path: str) -> list:
    """
    读取线索 CSV 文件。

    参数:
        input_path: 输入 CSV 文件路径

    返回:
        字典列表，每个字典代表一条线索记录

    异常:
        FileNotFoundError: 文件不存在
        ValueError: 文件格式错误或缺少必需列
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"输入文件不存在：{input_path}")

    if not input_file.suffix.lower() == ".csv":
        raise ValueError(f"输入文件必须是 CSV 格式，当前文件后缀为：{input_file.suffix}")

    leads = []
    try:
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            if headers is None:
                raise ValueError("CSV 文件为空或格式不正确。")

            # 检查必需列是否存在
            missing_columns = [col for col in REQUIRED_SCORE_COLUMNS if col not in headers]
            if missing_columns:
                raise ValueError(
                    f"CSV 文件缺少必需列：{', '.join(missing_columns)}\n"
                    f"文件现有列：{', '.join(headers)}\n"
                    f"必需列：{', '.join(REQUIRED_SCORE_COLUMNS)}"
                )

            for row_num, row in enumerate(reader, start=2):  # 第2行开始（第1行是表头）
                leads.append(row)

    except UnicodeDecodeError:
        # 尝试 GBK 编码（常见于中文 Excel 导出）
        try:
            with open(input_file, "r", encoding="gbk") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
        except Exception as e:
            raise ValueError(f"无法读取文件编码，请确保文件为 UTF-8 或 GBK 编码：{e}")

    if not leads:
        raise ValueError("CSV 文件中没有数据行。")

    return leads


def score_leads(leads: list, weights: dict) -> list:
    """
    对线索列表进行评分和分级。

    参数:
        leads: 线索字典列表
        weights: 四维评分权重

    返回:
        添加了评分和分级结果的线索列表
    """
    scored_leads = []

    for i, lead in enumerate(leads):
        try:
            # 提取四维原始分数
            scores = {
                "profile_match": float(lead.get("profile_match_score", 0)),
                "behavior_signal": float(lead.get("behavior_signal_score", 0)),
                "need_clarity": float(lead.get("need_clarity_score", 0)),
                "recency": float(lead.get("recency_score", 0)),
            }

            # 如果提供了 last_interaction_date 列，则自动计算时效性分数
            last_interaction = lead.get("last_interaction_date", "").strip()
            if last_interaction:
                try:
                    # 支持多种日期格式
                    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
                        try:
                            last_date = datetime.strptime(last_interaction, fmt)
                            days_since = (datetime.now() - last_date).days
                            scores["recency"] = calculate_recency_score(days_since)
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass  # 无法解析日期时，使用 CSV 中的原始分数

            # 计算加权总分
            total_score = calculate_weighted_score(scores, weights)

            # 确定等级
            grade = determine_grade(total_score)

            # 计算各维度加权得分（用于详情展示）
            weighted_profile = round(scores["profile_match"] * weights["profile_match"], 2)
            weighted_behavior = round(scores["behavior_signal"] * weights["behavior_signal"], 2)
            weighted_need = round(scores["need_clarity"] * weights["need_clarity"], 2)
            weighted_recency = round(scores["recency"] * weights["recency"], 2)

            # 构建结果记录
            scored_lead = dict(lead)
            scored_lead["weighted_profile_match"] = weighted_profile
            scored_lead["weighted_behavior_signal"] = weighted_behavior
            scored_lead["weighted_need_clarity"] = weighted_need
            scored_lead["weighted_recency"] = weighted_recency
            scored_lead["total_score"] = total_score
            scored_lead["grade"] = grade
            scored_lead["grade_description"] = GRADE_DESCRIPTIONS[grade]
            scored_lead["scoring_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            scored_leads.append(scored_lead)

        except (ValueError, TypeError) as e:
            print(f"[警告] 第 {i + 2} 行数据处理异常，已跳过：{e}")
            # 将异常行标记为评分失败
            scored_lead = dict(lead)
            scored_lead["total_score"] = "ERROR"
            scored_lead["grade"] = "ERROR"
            scored_lead["grade_description"] = f"评分失败：{e}"
            scored_lead["scoring_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            scored_leads.append(scored_lead)

    return scored_leads


def write_scored_csv(scored_leads: list, output_path: str) -> None:
    """
    将评分结果写入 CSV 文件。

    参数:
        scored_leads: 评分后的线索列表
        output_path: 输出 CSV 文件路径
    """
    if not scored_leads:
        print("[警告] 没有可输出的评分结果。")
        return

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 确定输出列顺序：原始列 + 评分新增列
    score_columns = [
        "weighted_profile_match",
        "weighted_behavior_signal",
        "weighted_need_clarity",
        "weighted_recency",
        "total_score",
        "grade",
        "grade_description",
        "scoring_timestamp",
    ]
    all_columns = [col for col in scored_leads[0].keys() if col not in score_columns]
    all_columns.extend(score_columns)

    with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(scored_leads)


def print_summary(scored_leads: list, weights: dict) -> None:
    """
    打印评分结果摘要。

    参数:
        scored_leads: 评分后的线索列表
        weights: 使用的权重配置
    """
    # 过滤掉评分失败的记录
    valid_leads = [l for l in scored_leads if l.get("grade") != "ERROR"]
    error_leads = [l for l in scored_leads if l.get("grade") == "ERROR"]

    if not valid_leads:
        print("[警告] 没有有效的评分结果。")
        return

    # 统计各等级数量
    grade_counts = {"H": 0, "A": 0, "B": 0, "C": 0}
    total_scores = []
    for lead in valid_leads:
        grade = lead.get("grade", "C")
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
        try:
            total_scores.append(float(lead["total_score"]))
        except (ValueError, TypeError):
            pass

    total_count = len(valid_leads)
    avg_score = sum(total_scores) / len(total_scores) if total_scores else 0

    print("\n" + "=" * 60)
    print("  线索评分结果摘要")
    print("=" * 60)

    print(f"\n评分权重配置：")
    print(f"  企业画像匹配度 (profile_match):  {weights['profile_match']:.0%}")
    print(f"  行为信号强度 (behavior_signal):   {weights['behavior_signal']:.0%}")
    print(f"  需求明确度 (need_clarity):        {weights['need_clarity']:.0%}")
    print(f"  时效性 (recency):                 {weights['recency']:.0%}")

    print(f"\n线索总数：{len(scored_leads)} 条")
    if error_leads:
        print(f"  其中评分失败：{len(error_leads)} 条")
    print(f"有效评分：{total_count} 条")
    print(f"平均得分：{avg_score:.1f} 分")

    print(f"\n分级分布：")
    print(f"  {'等级':<6} {'数量':>6} {'占比':>8} {'说明'}")
    print(f"  {'─' * 50}")
    for grade in ["H", "A", "B", "C"]:
        count = grade_counts[grade]
        pct = (count / total_count * 100) if total_count > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  {grade:<6} {count:>6} {pct:>7.1f}% {bar} {GRADE_DESCRIPTIONS[grade]}")

    # 销售交付统计
    handoff_count = grade_counts["H"] + grade_counts["A"]
    nurture_count = grade_counts["B"]
    archive_count = grade_counts["C"]
    print(f"\n行动建议：")
    print(f"  立即/近期交付销售 (H+A): {handoff_count} 条")
    print(f"  进入培育序列 (B):        {nurture_count} 条")
    print(f"  存档观察 (C):            {archive_count} 条")

    # 显示 Top 5 高分线索
    if total_scores:
        sorted_leads = sorted(
            valid_leads,
            key=lambda x: float(x.get("total_score", 0)),
            reverse=True,
        )
        print(f"\nTop 5 高分线索：")
        # 尝试找到用于标识线索的列
        id_col = None
        for candidate in ["lead_id", "company_name", "contact_name", "email", "id", "name"]:
            if candidate in sorted_leads[0]:
                id_col = candidate
                break

        for i, lead in enumerate(sorted_leads[:5], start=1):
            score = lead["total_score"]
            grade = lead["grade"]
            identifier = lead.get(id_col, f"第{i}条") if id_col else f"第{i}条"
            print(f"  {i}. [{grade}] {score}分 — {identifier}")

    print(f"\n{'=' * 60}")


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：解析参数并执行线索评分。"""

    parser = argparse.ArgumentParser(
        description="Sloth-MGO-Eido 线索评分计算脚本",
        epilog=(
            "CSV 文件格式要求：\n"
            "  必需列：profile_match_score, behavior_signal_score, need_clarity_score, recency_score\n"
            "  可选列：last_interaction_date (YYYY-MM-DD 格式，自动计算时效性分数)\n"
            "  其他列：lead_id, company_name, contact_name 等（原样保留并输出）\n"
            "\n"
            "示例 CSV：\n"
            "  lead_id,company_name,profile_match_score,behavior_signal_score,need_clarity_score,recency_score\n"
            "  L001,某科技公司,85,70,60,90\n"
            "  L002,某制造企业,60,45,30,70\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="输入 CSV 文件路径（包含线索原始数据和四维分数）",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="输出 CSV 文件路径（默认：在输入文件同目录生成 *_scored.csv）",
    )
    parser.add_argument(
        "--w-profile",
        type=float,
        default=DEFAULT_WEIGHTS["profile_match"],
        help=f"企业画像匹配度权重（默认: {DEFAULT_WEIGHTS['profile_match']}）",
    )
    parser.add_argument(
        "--w-behavior",
        type=float,
        default=DEFAULT_WEIGHTS["behavior_signal"],
        help=f"行为信号强度权重（默认: {DEFAULT_WEIGHTS['behavior_signal']}）",
    )
    parser.add_argument(
        "--w-need",
        type=float,
        default=DEFAULT_WEIGHTS["need_clarity"],
        help=f"需求明确度权重（默认: {DEFAULT_WEIGHTS['need_clarity']}）",
    )
    parser.add_argument(
        "--w-recency",
        type=float,
        default=DEFAULT_WEIGHTS["recency"],
        help=f"时效性权重（默认: {DEFAULT_WEIGHTS['recency']}）",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        default=False,
        help="输出评分结果摘要到终端",
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        choices=["score", "grade", "none"],
        default="score",
        help="输出结果排序方式：score（按分数降序）、grade（按等级）、none（保持原序）",
    )

    args = parser.parse_args()

    # 构建权重字典
    weights = {
        "profile_match": args.w_profile,
        "behavior_signal": args.w_behavior,
        "need_clarity": args.w_need,
        "recency": args.w_recency,
    }

    # 校验权重
    if not validate_weights(weights):
        print("\n请调整权重参数，确保所有权重在 [0, 1] 范围内且合计为 1.0。")
        sys.exit(1)

    # 确定输出文件路径
    if args.output:
        output_path = args.output
    else:
        input_file = Path(args.input)
        output_path = str(input_file.parent / f"{input_file.stem}_scored.csv")

    # 执行评分流程
    try:
        print(f"[1/3] 正在读取线索数据：{args.input}")
        leads = read_leads_csv(args.input)
        print(f"      成功读取 {len(leads)} 条线索记录。")

        print(f"[2/3] 正在计算评分...")
        scored_leads = score_leads(leads, weights)
        valid_count = sum(1 for l in scored_leads if l.get("grade") != "ERROR")
        error_count = len(scored_leads) - valid_count
        print(f"      评分完成。成功 {valid_count} 条，失败 {error_count} 条。")

        # 排序
        if args.sort_by == "score":
            scored_leads.sort(
                key=lambda x: float(x.get("total_score", 0)) if x.get("grade") != "ERROR" else -1,
                reverse=True,
            )
        elif args.sort_by == "grade":
            grade_order = {"H": 0, "A": 1, "B": 2, "C": 3, "ERROR": 4}
            scored_leads.sort(key=lambda x: grade_order.get(x.get("grade", "C"), 4))

        print(f"[3/3] 正在写入评分结果：{output_path}")
        write_scored_csv(scored_leads, output_path)
        print(f"      写入完成。")

        # 输出摘要（默认启用或用户指定）
        if args.summary or not args.output:
            print_summary(scored_leads, weights)

        print(f"\n评分结果已保存至：{output_path}")

    except FileNotFoundError as e:
        print(f"\n[错误] {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[错误] 数据格式问题：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[错误] 未预期的异常：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
