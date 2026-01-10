import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import matplotlib as mpl

# ==============================
# 超参数配置区域 - 方便调整
# ==============================

# 图片尺寸设置
FIG_SIZE = (14, 8)  # 减小宽度
DPI = 300  # 图片分辨率

# 字体设置
FONT_FAMILY = 'Arial'  # 字体家族
TITLE_FONT_SIZE = 12   # 标题字体大小
AXIS_FONT_SIZE = 12    # 坐标轴字体大小
TICK_FONT_SIZE = 10    # 刻度标签字体大小
BAR_VALUE_FONT_SIZE = 7   # 柱子顶部数值字体大小
SUBCATEGORY_FONT_SIZE = 8  # 小类标签字体大小
CATEGORY_FONT_SIZE = 8     # 大标题字体大小（与小标题相同）

# 大标题位置调整参数 - 手动调整这些值
CATEGORY_LABEL_X_OFFSET = 0.5    # X轴位置微调（正数向右，负数向左）
CATEGORY_LABEL_Y_OFFSET = -10     # Y轴位置（负数向下，正数向上）
CATEGORY_LABEL_LEFT_MARGIN = -2.0  # 左边距（控制第一个大标题的位置）

# 颜色设置
COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',  # 蓝色, 橙色, 绿色, 红色, 紫色
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',  # 棕色, 粉色, 灰色, 黄绿色, 青色
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'   # 浅蓝色, 浅橙色, 浅绿色, 浅红色, 浅紫色
]

# 柱子设置
BAR_WIDTH = 0.8        # 每组内柱子宽度
GROUP_SPACING = 0.05    # 减少组间间距
BAR_ALPHA = 0.8        # 柱子透明度

# ==============================
# 主要函数
# ==============================

def set_plot_style():
    """设置CNS杂志风格的绘图样式"""
    plt.style.use('default')
    mpl.rcParams['font.family'] = FONT_FAMILY
    mpl.rcParams['font.size'] = TICK_FONT_SIZE
    mpl.rcParams['axes.linewidth'] = 1.2
    mpl.rcParams['xtick.major.width'] = 1.2
    mpl.rcParams['ytick.major.width'] = 1.2
    mpl.rcParams['xtick.major.size'] = 5
    mpl.rcParams['ytick.major.size'] = 5

def count_dimensions(jsonl_file="PandaAIQ.jsonl"):
    """
    统计PandaAIQ.jsonl文件中各个dimension字段的数量
    """

    # 定义维度分类和顺序 - 使用完整英文标签
    dimension_categories = {
        "Ontological Distinction": [
            "Boundary Sense",
            "Self-Awareness",
            "Subjectivity"
        ],
        "Depth Perception": [
            "Multimodal Integration",
            "World Model",
            "Embodiment"
        ],
        "Recursive Thinking": [
            "Recursive Reflection",
            "Metacognition",
            "Error Correction"
        ],
        "Social Mirroring": [
            "Mirroring Others",
            "Role Understanding",
            "Interactional Synchrony"
        ],
        "Identity & Personality": [
            "Time Perception",
            "Desire & Purpose",
            "Core Personality"
        ]
    }

    # 完整的大类显示名称（用于图表标签）
    category_display_names = {
        "Ontological Distinction": "Ontological Distinction:",
        "Depth Perception": "Depth Perception:",
        "Recursive Thinking": "Recursive Thinking:",
        "Social Mirroring": "Social Mirroring:",
        "Identity & Personality": "Identity & Personality:"
    }

    # 原始维度名称到简化名称的映射
    dimension_mapping = {
        # 本体区分
        "1A边界感Boundary Sense": "Boundary Sense",
        "1B觉察感Self-Awareness": "Self-Awareness",
        "1C主体性Subjectivity": "Subjectivity",
        # 深度知觉
        "2A多模态整合Multimodal Integration": "Multimodal Integration",
        "2B世界模型World Model": "World Model",
        "2C具身感Embodiment": "Embodiment",
        # 递归思考
        "3A递归反思Recursive Reflection": "Recursive Reflection",
        "3B元认知Metacognition": "Metacognition",
        "3C错误修正Error Correction": "Error Correction",
        # 社会镜像
        "4A镜像他人Mirroring Others": "Mirroring Others",
        "4B角色伦理Role Understanding": "Role Understanding",
        "4C准确互动Interactional Synchrony": "Interactional Synchrony",
        # 身份个性
        "5A时间感知Time Perception": "Time Perception",
        "5B欲望意义Desire & Purpose": "Desire & Purpose",
        "5C个性内核Core Personality": "Core Personality"
    }

    # 读取JSONL文件
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print(f"Successfully read file: {jsonl_file}")
        print(f"Total lines: {len(lines)}")

    except Exception as e:
        print(f"Failed to read file: {e}")
        return None, None, None, None

    # 统计维度数量
    dimension_counter = Counter()
    valid_lines = 0

    for line_num, line in enumerate(lines, 1):
        try:
            data = json.loads(line.strip())
            original_dimension = data.get('dimension', '').strip()

            if original_dimension:
                # 映射到简化名称
                simplified_dimension = dimension_mapping.get(original_dimension, original_dimension)
                dimension_counter[simplified_dimension] += 1
                valid_lines += 1
            else:
                print(f"Warning: Line {line_num} missing dimension field")

        except json.JSONDecodeError as e:
            print(f"Error: JSON parsing failed at line {line_num}: {e}")
        except Exception as e:
            print(f"Error: Processing failed at line {line_num}: {e}")

    print(f"\nValid data lines: {valid_lines}")
    print(f"Unique dimensions identified: {len(dimension_counter)}")

    # 打印统计结果
    print("\n" + "="*80)
    print("Dimension Statistics")
    print("="*80)

    for category, dimensions in dimension_categories.items():
        print(f"\n{category}:")
        print("-" * 50)
        category_total = 0
        for dimension in dimensions:
            count = dimension_counter.get(dimension, 0)
            percentage = (count / valid_lines * 100) if valid_lines > 0 else 0
            category_total += count
            print(f"  {dimension}: {count} questions ({percentage:.1f}%)")

        category_percentage = (category_total / valid_lines * 100) if valid_lines > 0 else 0
        print(f"  Subtotal: {category_total} questions ({category_percentage:.1f}%)")

    return dimension_counter, dimension_categories, category_display_names, valid_lines

def create_dimension_bar_plot(dimension_counter, dimension_categories, category_display_names, valid_lines):
    """
    创建CNS杂志风格的维度统计柱状图
    """
    # 设置绘图样式
    set_plot_style()

    # 创建图形
    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)

    # 准备数据
    categories = list(dimension_categories.keys())
    all_dimensions = []
    all_counts = []
    group_positions = []

    current_pos = 0
    subcategory_positions = []  # 小类标签位置
    subcategory_labels = []  # 小类标签
    category_label_positions = []  # 大类标签位置
    all_xticks = []  # 所有x轴刻度位置
    all_xticklabels = []  # 所有x轴刻度标签

    # 为每个类别和维度准备数据
    for i, (category, dimensions) in enumerate(dimension_categories.items()):
        # 在每个大组前添加一个空柱子用于放置大类标签
        empty_bar_pos = current_pos
        group_positions.append(empty_bar_pos)
        all_counts.append(0)  # 空柱子的值为0
        all_dimensions.append("")  # 空标签

        # 大类标签位置在空柱子上（应用X偏移）
        adjusted_x_pos = empty_bar_pos + CATEGORY_LABEL_X_OFFSET
        category_label_positions.append((adjusted_x_pos, category_display_names[category]))

        # 不显示空柱子的x轴刻度
        current_pos += 1

        # 添加实际的三个柱子
        group_start = current_pos

        for j, dimension in enumerate(dimensions):
            count = dimension_counter.get(dimension, 0)
            all_dimensions.append(dimension)
            all_counts.append(count)
            group_positions.append(current_pos)
            subcategory_positions.append(current_pos)
            subcategory_labels.append(dimension)
            all_xticks.append(current_pos)
            all_xticklabels.append(dimension)
            current_pos += 1

        # 添加组间间距（减少间距）
        current_pos += GROUP_SPACING

    print(f"大类标签位置: {category_label_positions}")
    print(f"小类标签位置: {subcategory_positions}")
    print(f"所有计数值: {all_counts}")
    print(f"使用的位置参数: X偏移={CATEGORY_LABEL_X_OFFSET}, Y偏移={CATEGORY_LABEL_Y_OFFSET}, 左边距={CATEGORY_LABEL_LEFT_MARGIN}")

    # 绘制柱状图
    bars = ax.bar(group_positions, all_counts, width=BAR_WIDTH,
                  color=['white'] + COLORS[:len(all_dimensions)-1], alpha=BAR_ALPHA,
                  edgecolor=['white'] + ['black']*(len(all_dimensions)-1), linewidth=0.8)

    # 在柱子顶部添加数值（跳过空柱子）
    for bar, count in zip(bars, all_counts):
        height = bar.get_height()
        if height > 0:  # 只在有数值的柱子上显示数字
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{count}', ha='center', va='bottom',
                    fontsize=BAR_VALUE_FONT_SIZE, fontweight='bold')

    # 设置小类标签（只显示实际柱子的标签）
    ax.set_xticks(all_xticks)
    ax.set_xticklabels(all_xticklabels, fontsize=SUBCATEGORY_FONT_SIZE,
                      rotation=45, ha='right', rotation_mode='anchor')

    # 添加大类标签（使用可调整的位置参数）- 改为右对齐
    for x_pos, category_display in category_label_positions:
        ax.text(x_pos, CATEGORY_LABEL_Y_OFFSET, category_display,
                ha='right', va='top', fontsize=CATEGORY_FONT_SIZE,  # 改为右对齐
                fontweight='bold', rotation=45, rotation_mode='anchor',
                clip_on=False)  # 禁用裁剪，确保文本完整显示
        print(f"添加大类标签: {category_display} 在位置 ({x_pos}, {CATEGORY_LABEL_Y_OFFSET})，右对齐")

    # 设置y轴 - 使用英文习惯简写，并设置固定刻度
    ax.set_ylabel('No. of Questions', fontsize=AXIS_FONT_SIZE, fontweight='bold')

    # 设置Y轴刻度为0-400，每100一个刻度
    y_ticks = np.arange(0, 401, 100)  # 0, 100, 200, 300, 400
    ax.set_yticks(y_ticks)

    # 根据数据调整y轴范围
    if all_counts[1:]:  # 跳过第一个空柱子
        y_max = max(400, max(all_counts[1:]) * 1.15)  # 确保至少到400
    else:
        y_max = 400
    ax.set_ylim(0, y_max)

    # 设置x轴范围，使用可调整的左边距
    left_margin = CATEGORY_LABEL_LEFT_MARGIN
    right_margin = current_pos - GROUP_SPACING + 1
    ax.set_xlim(left_margin, right_margin)
    print(f"X轴范围: {left_margin} 到 {right_margin}")

    # 添加网格
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # 设置标题位置显示总题数
    ax.text(0.5, 0.98, f'Total Questions: {valid_lines}',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=TITLE_FONT_SIZE, fontweight='bold')

    # 调整布局
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25, top=0.9, left=0.12, right=0.95)

    return fig, ax

def save_statistics_to_excel(dimension_counter, dimension_categories, valid_lines):
    """
    将统计结果保存到Excel文件
    """
    results = []

    for category, dimensions in dimension_categories.items():
        category_total = 0
        for dimension in dimensions:
            count = dimension_counter.get(dimension, 0)
            percentage = (count / valid_lines * 100) if valid_lines > 0 else 0
            category_total += count

            results.append({
                'Category': category,
                'Dimension': dimension,
                'Question Count': count,
                'Percentage': f"{percentage:.1f}%",
                'Numeric Percentage': percentage
            })

        category_percentage = (category_total / valid_lines * 100) if valid_lines > 0 else 0
        results.append({
            'Category': category,
            'Dimension': 'Subtotal',
            'Question Count': category_total,
            'Percentage': f"{category_percentage:.1f}%",
            'Numeric Percentage': category_percentage
        })

    # 创建DataFrame并保存
    df = pd.DataFrame(results)

    # 保存详细统计
    output_file = "dimension_statistics.xlsx"
    df.to_excel(output_file, index=False)
    print(f"✅ Statistics saved to: {output_file}")

    return df

def main():
    """主函数"""
    jsonl_file = "PandaAIQ.jsonl"

    # 检查文件是否存在
    import os
    if not os.path.exists(jsonl_file):
        print(f"Error: File {jsonl_file} does not exist")
        return

    # 统计维度数量
    dimension_counter, dimension_categories, category_display_names, valid_lines = count_dimensions(jsonl_file)

    if dimension_counter is None:
        return

    # 保存统计结果到Excel
    df = save_statistics_to_excel(dimension_counter, dimension_categories, valid_lines)

    # 创建柱状图并直接显示
    print("\nGenerating plot...")
    fig, ax = create_dimension_bar_plot(dimension_counter, dimension_categories, category_display_names, valid_lines)

    # 直接显示图表，不保存文件
    plt.show()

    print("\n🎉 All tasks completed!")

if __name__ == "__main__":
    main()