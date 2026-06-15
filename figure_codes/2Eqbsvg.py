import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# ==========================================
# 1. 样式与配色配置 (全量 Arial)
# ==========================================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 2.5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2

# 关键设置：确保导出的 SVG 文本在矢量软件中可编辑
plt.rcParams['svg.fonttype'] = 'none'

# 基础配色库
CUSTOM_COLORS = [
    '#4472C4', '#ED7D31', '#548235', '#997300', '#A5A5A5',
    '#FF66CC', '#BCBD22', '#17BECF', '#AEC7E8', '#98DF8A',
    '#FF9896', '#C5B0D5', '#1F77B4', '#FF7F0E', '#2CA02C'
]

# 核心映射：确保同名柱子在不同图表中颜色一致
NAME_TO_COLOR = {
    "Boundary Sense": CUSTOM_COLORS[0], "Self-Awareness": CUSTOM_COLORS[1], "Subjectivity": CUSTOM_COLORS[2],
    "Multimodal Integration": CUSTOM_COLORS[3], "World Model": CUSTOM_COLORS[4], "Embodiment": CUSTOM_COLORS[5],
    "Recursive Reflection": CUSTOM_COLORS[6], "Metacognition": CUSTOM_COLORS[7], "Error Correction": CUSTOM_COLORS[8],
    "Mirroring Others": CUSTOM_COLORS[9], "Role Understanding": CUSTOM_COLORS[10], "Interactional Synchrony": CUSTOM_COLORS[11],
    "Time Perception": CUSTOM_COLORS[12], "Desire & Purpose": CUSTOM_COLORS[13], "Core Personality": CUSTOM_COLORS[14]
}

def calculate_cronbach_stats(df_subset):
    """ 计算 Cronbach's Alpha """
    item_scores = df_subset.T
    n_samples, n_items = item_scores.shape
    if n_items < 2:
        return np.nan
    item_variances = item_scores.var(axis=0, ddof=1)
    total_scores = item_scores.sum(axis=1)
    total_variance = total_scores.var(ddof=1)
    if total_variance == 0:
        alpha = 0.0
    else:
        alpha = (n_items / (n_items - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha

def plot_custom_style(summary_data, output_filename='panda_alpha_final.svg'):
    print(f"准备绘图...")
    fig, ax = plt.subplots(figsize=(16, 7))

    x_positions = []
    x_labels = []
    heights = []
    bar_colors = []
    major_label_indices = []

    current_x = 0
    gap_width = 1.5

    df_sum = pd.DataFrame(summary_data)
    major_ids = sorted(list(set([x[0] for x in df_sum['ID']])))

    for maj_id in major_ids:
        # 1. 绘制大类
        maj_row_df = df_sum[df_sum['ID'] == maj_id]
        if not maj_row_df.empty:
            maj_row = maj_row_df.iloc[0]
            x_positions.append(current_x)
            x_labels.append(maj_row['Name'])
            major_label_indices.append(len(x_labels) - 1)
            heights.append(maj_row['Cronbach_Alpha'])
            bar_colors.append("#403F3F")
            current_x += 1

        # 2. 绘制小类
        sub_rows = df_sum[
            (df_sum['ID'].str.startswith(maj_id)) & (df_sum['ID'].str.len() > 1)
        ].sort_values('ID')

        for _, sub_row in sub_rows.iterrows():
            x_positions.append(current_x)
            x_labels.append(sub_row['Name'])
            heights.append(sub_row['Cronbach_Alpha'])
            bar_colors.append(NAME_TO_COLOR.get(sub_row['Name'], "#252323"))
            current_x += 1

        current_x += gap_width - 1

    # 绘制柱子
    heights = [0 if pd.isna(h) else h for h in heights]
    bars = ax.bar(x_positions, heights,
           color=bar_colors,
           edgecolor='black',
           linewidth=2.0,
           width=0.85,
           zorder=3)

    # Y轴设置
    ax.set_ylim(0.8, 1.0)
    custom_yticks = [0.8, 0.9, 1.0]
    ax.set_yticks(custom_yticks)
    ax.set_yticklabels([f"{y:.1f}" for y in custom_yticks], fontsize=26, fontweight='bold', fontfamily='Arial')
    ax.set_ylabel("Cronbach's α Coefficient", fontsize=30, fontweight='bold', labelpad=12, fontfamily='Arial')

    # X轴设置
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontfamily='Arial')
    ax.set_xlim(-0.8, current_x - gap_width + 0.8)

    # 标签样式
    xtick_labels = ax.get_xticklabels()
    for i, label in enumerate(xtick_labels):
        label.set_fontsize(24)
        if i in major_label_indices:
            label.set_fontweight('bold')
        else:
            label.set_fontweight('normal')

    # 背景网格线 (极淡风格)
    ax.grid(axis='y', linestyle='-', alpha=0.1, color='#E0E0E0', zorder=0)

    # 边框设置
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5)

    plt.subplots_adjust(bottom=0.35, top=0.95, left=0.08, right=0.98)

    print(f"正在保存为 {output_filename} ...")
    # 修改点：保存为 SVG
    plt.savefig(output_filename, format='svg', bbox_inches='tight')
    print("保存成功！")

def main():
    file_path = 'panda_detailed_scores.xlsx'
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        return

    df = pd.read_excel(file_path)
    id_col = df.columns[0]
    score_cols = df.columns[1:]
    df[id_col] = df[id_col].astype(str)

    cat_names = {
        '1': 'Ontological Distinction', '2': 'Depth Perception', '3': 'Recursive Thinking',
        '4': 'Social Mirroring', '5': 'Identity & Personality',
        '1A': 'Boundary Sense', '1B': 'Self-Awareness', '1C': 'Subjectivity',
        '2A': 'Multimodal Integration', '2B': 'World Model', '2C': 'Embodiment',
        '3A': 'Recursive Reflection', '3B': 'Metacognition', '3C': 'Error Correction',
        '4A': 'Mirroring Others', '4B': 'Role Understanding', '4C': 'Interactional Synchrony',
        '5A': 'Time Perception', '5B': 'Desire & Purpose', '5C': 'Core Personality'
    }

    results_list = []
    df['Group_ID'] = df[id_col].str[:2]
    df['Major_ID'] = df[id_col].str[0]

    unique_sub_groups = sorted(df['Group_ID'].unique())
    unique_major_groups = sorted(df['Major_ID'].unique())

    for sub_id in unique_sub_groups:
        if len(sub_id) < 2: continue
        subset = df[df['Group_ID'] == sub_id]
        if len(subset) > 1:
            alpha = calculate_cronbach_stats(subset.set_index(id_col)[score_cols])
            results_list.append({'Level': 'Sub-Category', 'ID': sub_id, 'Name': cat_names.get(sub_id, sub_id), 'Cronbach_Alpha': alpha})

    for maj_id in unique_major_groups:
        subset = df[df['Major_ID'] == maj_id]
        if len(subset) > 1:
            alpha = calculate_cronbach_stats(subset.set_index(id_col)[score_cols])
            results_list.append({'Level': 'Major-Category', 'ID': maj_id, 'Name': cat_names.get(maj_id, f"Major {maj_id}"), 'Cronbach_Alpha': alpha})

    if results_list:
        plot_custom_style(results_list)

if __name__ == "__main__":
    main()