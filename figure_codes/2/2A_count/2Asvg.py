import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

# ==============================
# 1. 全局样式配置
# ==============================
plt.rcParams['font.family'] = 'Arial'
# 关键设置：确保导出的 SVG 文本在矢量软件中可编辑
plt.rcParams['svg.fonttype'] = 'none'

STYLE_CONFIG = {
    'font_family': 'Arial',
    'font_weight_bold': 'bold',
    'font_size_title': 30,
    'font_size_ylabel': 40,
    'font_size_tick': 30,
    'font_size_major': 40,      # 大类标签字号
    'font_size_minor': 40,      # 小类标签字号

    # 线条参数
    'axes_linewidth': 2.5,
    'tick_width': 2.5,
    'tick_length': 6,
    'bar_width': 0.8,
    'group_gap': 1.0,            # 组间距
    'label_slot_width': 1.0,    # 大类标签占用的“空位”宽度
}

# 配色方案
CUSTOM_COLORS = [
    '#4472C4', '#ED7D31', '#548235',
    '#997300', '#A5A5A5', '#FF66CC',
    '#BCBD22', '#17BECF', '#AEC7E8',
    '#98DF8A', '#FF9896', '#C5B0D5',
    '#1F77B4', '#FF7F0E', '#2CA02C'
]

def get_default_data():
    """默认数据"""
    return {
        "Ontological Distinction": [
            ("Boundary Sense", 102), ("Self-Awareness", 286), ("Subjectivity", 353)
        ],
        "Depth Perception": [
            ("Multimodal Integration", 241), ("World Model", 116), ("Embodiment", 240)
        ],
        "Recursive Thinking": [
            ("Recursive Reflection", 118), ("Metacognition", 195), ("Error Correction", 115)
        ],
        "Social Mirroring": [
            ("Mirroring Others", 230), ("Role Understanding", 322), ("Interactional Synchrony", 185)
        ],
        "Identity & Personality": [
            ("Time Perception", 127), ("Desire & Purpose", 125), ("Core Personality", 179)
        ]
    }

def plot_cns_style_bar(data_map, total_count, output_filename="panda_distribution_fixed_layout.svg"):
    # 1. 设置画布
    fig, ax = plt.subplots(figsize=(16, 9))

    # 绘图数据容器
    bar_x_positions = []
    bar_heights = []
    bar_colors = []

    # 轴刻度容器
    all_xticks = []
    all_xlabels = []

    current_x = 0
    color_idx = 0

    # 2. 构建数据
    for major_cat, sub_items in data_map.items():
        # --- A. 放置大类标签 ---
        major_label_text = major_cat + ":"
        all_xticks.append(current_x)
        all_xlabels.append(major_label_text)
        current_x += STYLE_CONFIG['label_slot_width']

        # --- B. 放置该组的柱子 ---
        for sub_name, count in sub_items:
            bar_x_positions.append(current_x)
            bar_heights.append(count)
            bar_colors.append(CUSTOM_COLORS[color_idx % len(CUSTOM_COLORS)])
            all_xticks.append(current_x)
            all_xlabels.append(sub_name)
            color_idx += 1
            current_x += 1

        # --- C. 组间距 ---
        current_x += STYLE_CONFIG['group_gap'] - 1

    # 3. 绘制柱子
    bars = ax.bar(bar_x_positions, bar_heights,
                  width=STYLE_CONFIG['bar_width'],
                  color=bar_colors,
                  edgecolor='black',
                  linewidth=1.2,
                  zorder=3)

    # 5. 设置 X 轴刻度与标签
    ax.set_xticks(all_xticks)
    xtick_labels = ax.set_xticklabels(all_xlabels, rotation=45, ha='right')

    # 6. 差异化设置标签样式
    for label_obj, text_str in zip(xtick_labels, all_xlabels):
        label_obj.set_fontfamily(STYLE_CONFIG['font_family'])
        if text_str.endswith(":"):
            label_obj.set_fontsize(STYLE_CONFIG['font_size_major'])
            label_obj.set_fontweight('bold')
        else:
            label_obj.set_fontsize(STYLE_CONFIG['font_size_minor'])
            label_obj.set_fontweight('normal')

    # 7. Y轴与其他装饰
    ax.set_ylabel("No. of Questions",
                  fontsize=STYLE_CONFIG['font_size_ylabel'],
                  fontweight='bold', labelpad=10)

    max_height = max(bar_heights) if bar_heights else 400
    ax.set_ylim(0, max_height * 1.15)
    ax.set_yticks(np.arange(0, max_height + 50, 100))

    # 刻度设置
    ax.tick_params(axis='both', which='major', direction='out',
                   length=STYLE_CONFIG['tick_length'],
                   width=STYLE_CONFIG['tick_width'],
                   labelsize=STYLE_CONFIG['font_size_tick'])

    # 8. 边框设置
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(STYLE_CONFIG['axes_linewidth'])
    ax.spines['bottom'].set_linewidth(STYLE_CONFIG['axes_linewidth'])

    # 9. 顶部标题
    ax.text(0.5, 0.95, f"Total Questions: {total_count}",
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=STYLE_CONFIG['font_size_title'],
            fontweight='bold',
            fontfamily=STYLE_CONFIG['font_family'])

    # --- 修改点：设置极淡的网格线 ---
    # alpha=0.1 使其非常透明，color='#E0E0E0' 是极浅的灰色
    ax.grid(axis='y', linestyle='-', alpha=0.1, color='#E0E0E0', zorder=0)

    # 10. 保存 SVG
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)

    print(f"正在保存为 {output_filename} ...")
    plt.savefig(output_filename, format='svg', bbox_inches='tight')
    print("保存成功！")

def main():
    data_map = get_default_data()
    total_count = 2934
    if data_map:
        plot_cns_style_bar(data_map, total_count)
    else:
        print("无数据可绘图")

if __name__ == "__main__":
    main()