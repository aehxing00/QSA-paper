import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# ==================== 超参数配置区域 ====================
# 图例位置和样式参数
LEGEND_X = 0.35          # 图例x位置（0-1之间，0为最左）
LEGEND_Y = 1          # 图例y位置（0-1之间，1为最顶）
LEGEND_FONT_SIZE = 7     # 图例字体大小
LEGEND_BOX_ALPHA = 0.9   # 图例框透明度

# 大类别标签详细位置参数 - 每个类别单独设置
CATEGORY_LABELS = {
    'Ontological Distinction\n(I Exist)': {
        'x': 1.0,    # x坐标位置（对应1B位置）
        'y': 0.9,   # y坐标位置（相对于y轴最大值）
        'fontsize': 6,  # 字体大小
        'box_alpha': 0.7  # 标签框透明度
    },
    'Depth Perception\n(I Perceive)': {
        'x': 4.0,    # x坐标位置（对应2B位置）
        'y': 0.75,
        'fontsize': 6,
        'box_alpha': 0.7
    },
    'Recursive Thinking\n(I Think)': {
        'x': 7.0,    # x坐标位置（对应3B位置）
        'y': 0.75,
        'fontsize': 6,
        'box_alpha': 0.7
    },
    'Social Mirroring\n(I Interact)': {
        'x': 10.0,   # x坐标位置（对应4B位置）
        'y': 0.75,
        'fontsize': 6,
        'box_alpha': 0.7
    },
    'Identity & Personality\n(I Endure)': {
        'x': 13.0,   # x坐标位置（对应5B位置）
        'y': 0.9,
        'fontsize': 6,
        'box_alpha': 0.7
    }
}

# 分割虚线位置参数 - 修正为大组之间的位置
# 每组有3个子项，分割线应该在第3个和第4个子项之间、第6个和第7个之间等
DIVIDER_POSITIONS = [
    2.5,  # 第1组(1A-1C)和第2组(2A-2C)之间（在1C和2A之间）
    5.5,  # 第2组和第3组之间（在2C和3A之间）
    8.5,  # 第3组和第4组之间（在3C和4A之间）
    11.5  # 第4组和第5组之间（在4C和5A之间）
]

# 柱状图样式参数
BAR_WIDTH = 0.3                # 每个柱子的宽度
GROUP_WIDTH = 0.8              # 每组两个柱子的总宽度
GAP_BETWEEN_GROUPS = 0.4       # 组之间的间距

# 误差线样式参数
ERROR_CAP_SIZE = 1             # 误差线帽子大小
ERROR_CAP_THICK = 0.5          # 误差线帽子粗细
ERROR_LINE_WIDTH = 0.5         # 误差线粗细

# 坐标轴标签字体大小
YLABEL_FONT_SIZE = 10           # y轴标签字体大小
XTICK_FONT_SIZE = 7            # x轴刻度标签字体大小
YTICK_FONT_SIZE = 7            # y轴刻度标签字体大小

# y轴刻度设置
Y_TICKS = [0, 0.2, 0.4, 0.6, 0.8]  # y轴刻度值
# ==================== 超参数配置区域结束 ====================

# 定义标记到英文的映射关系
marker_mapping = {
    # 本体区分（我存在）Ontological Distinction (I Exist)
    '1A': 'Boundary Sense',
    '1B': 'Self-Awareness',
    '1C': 'Subjectivity',

    # 深度知觉（我感知）Depth Perception (I Perceive)
    '2A': 'Multimodal Integration',
    '2B': 'World Model',
    '2C': 'Embodiment',

    # 递归思考（我思考）Recursive Thinking (I Think)
    '3A': 'Recursive Reflection',
    '3B': 'Metacognition',
    '3C': 'Error Correction',

    # 社会镜像（我互动）Social Mirroring (I Interact)
    '4A': 'Mirroring Others',
    '4B': 'Role Understanding',
    '4C': 'Interactional Synchrony',

    # 身份个性（我延续）Identity & Personality (I Endure)
    '5A': 'Time Perception',
    '5B': 'Desire & Purpose',
    '5C': 'Core Personality'
}

# 定义类别分组
category_groups = {
    'Ontological Distinction\n(I Exist)': ['1A', '1B', '1C'],
    'Depth Perception\n(I Perceive)': ['2A', '2B', '2C'],
    'Recursive Thinking\n(I Think)': ['3A', '3B', '3C'],
    'Social Mirroring\n(I Interact)': ['4A', '4B', '4C'],
    'Identity & Personality\n(I Endure)': ['5A', '5B', '5C']
}

def set_cns_style():
    """设置CNS期刊级别的绘图风格"""
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 8
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['lines.linewidth'] = 1.2
    plt.rcParams['xtick.major.width'] = 1.0
    plt.rcParams['ytick.major.width'] = 1.0
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 600
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.pad_inches'] = 0.1

def safe_convert_to_float(value):
    """安全转换为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan

def calculate_statistics_and_plot(input_file):
    """计算统计量并生成柱状图"""

    # 读取数据
    df = pd.read_excel(input_file)

    print("数据列名:", df.columns.tolist())
    print("数据形状:", df.shape)
    print("\n前几行数据:")
    print(df.head())

    # 转换第一列为英文名称
    df['Subitem_English'] = df.iloc[:, 0].map(marker_mapping)
    df['Original_Marker'] = df.iloc[:, 0]

    # 手动指定列分组（根据您的描述）
    # 假设第一列是标记，第2-6列是微调模型，第7-11列是基础模型
    fine_tuned_cols = df.columns[1:6]    # 第2-6列：微调后模型
    base_cols = df.columns[6:11]         # 第7-11列：基础模型
    # 取消other组

    # 移除可能包含非数值数据的列
    fine_tuned_cols = [col for col in fine_tuned_cols if col not in ['Subitem_English', 'Original_Marker']]
    base_cols = [col for col in base_cols if col not in ['Subitem_English', 'Original_Marker']]

    print(f"\n微调模型列 ({len(fine_tuned_cols)}): {list(fine_tuned_cols)}")
    print(f"基础模型列 ({len(base_cols)}): {list(base_cols)}")

    # 计算统计量
    results = []
    for _, row in df.iterrows():
        subitem_en = row['Subitem_English']
        original_marker = row['Original_Marker']

        # 安全地转换为数值类型
        fine_tuned_vals = [safe_convert_to_float(row[col]) for col in fine_tuned_cols]
        base_vals = [safe_convert_to_float(row[col]) for col in base_cols]

        # 转换为Series并移除NaN值
        fine_tuned_series = pd.Series(fine_tuned_vals).dropna()
        base_series = pd.Series(base_vals).dropna()

        # 计算各组的平均值和标准差
        fine_tuned_mean = fine_tuned_series.mean() if len(fine_tuned_series) > 0 else np.nan
        fine_tuned_std = fine_tuned_series.std() if len(fine_tuned_series) > 0 else np.nan

        base_mean = base_series.mean() if len(base_series) > 0 else np.nan
        base_std = base_series.std() if len(base_series) > 0 else np.nan

        # 确定所属的大类别
        category = None
        for cat_name, markers in category_groups.items():
            if original_marker in markers:
                category = cat_name
                break

        results.append({
            'Subitem_English': subitem_en,
            'Original_Marker': original_marker,
            'Category': category,
            'Fine-tuned_Mean': fine_tuned_mean,
            'Fine-tuned_Std': fine_tuned_std,
            'Base_Mean': base_mean,
            'Base_Std': base_std
        })

    result_df = pd.DataFrame(results)

    # 按原始标记排序以确保正确的顺序
    marker_order = ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C', '4A', '4B', '4C', '5A', '5B', '5C']
    result_df['Marker_Order'] = pd.Categorical(result_df['Original_Marker'], categories=marker_order, ordered=True)
    result_df = result_df.sort_values('Marker_Order')

    # 打印统计结果
    print("\n" + "="*80)
    print("详细统计结果")
    print("="*80)
    for _, row in result_df.iterrows():
        print(f"{row['Subitem_English']} ({row['Original_Marker']}):")
        print(f"  微调模型: {row['Fine-tuned_Mean']:.4f} ± {row['Fine-tuned_Std']:.4f}")
        print(f"  基础模型: {row['Base_Mean']:.4f} ± {row['Base_Std']:.4f}")
        print()

    # 创建柱状图
    set_cns_style()
    fig, ax = plt.subplots(figsize=(16, 6))

    # 设置柱状图参数
    x_pos = np.arange(len(result_df)) * (GROUP_WIDTH + GAP_BETWEEN_GROUPS)

    # CNS风格配色
    colors = ['#A23B72', '#2E86AB']  # 紫色(微调), 蓝色(基础)

    # 计算每个柱子在组内的位置
    offset = GROUP_WIDTH / 2 - BAR_WIDTH / 2

    # 绘制柱状图 - 两个柱子紧挨在一起
    bars1 = ax.bar(x_pos - offset/2, result_df['Fine-tuned_Mean'], BAR_WIDTH,
                   color=colors[0], edgecolor='white', linewidth=0.8,
                   label='Fine-tuned Model')

    bars2 = ax.bar(x_pos + offset/2, result_df['Base_Mean'], BAR_WIDTH,
                   color=colors[1], edgecolor='white', linewidth=0.8,
                   label='Base Model')

    # 手动添加误差线
    for i, (_, row) in enumerate(result_df.iterrows()):
        # 微调模型误差线
        if not np.isnan(row['Fine-tuned_Mean']) and not np.isnan(row['Fine-tuned_Std']):
            ax.errorbar(x_pos[i] - offset/2, row['Fine-tuned_Mean'],
                       yerr=[[row['Fine-tuned_Std']/2], [row['Fine-tuned_Std']/2]],
                       fmt='none', c='black', capsize=ERROR_CAP_SIZE,
                       capthick=ERROR_CAP_THICK, elinewidth=ERROR_LINE_WIDTH)

        # 基础模型误差线
        if not np.isnan(row['Base_Mean']) and not np.isnan(row['Base_Std']):
            ax.errorbar(x_pos[i] + offset/2, row['Base_Mean'],
                       yerr=[[row['Base_Std']/2], [row['Base_Std']/2]],
                       fmt='none', c='black', capsize=ERROR_CAP_SIZE,
                       capthick=ERROR_CAP_THICK, elinewidth=ERROR_LINE_WIDTH)

    # 设置x轴标签
    ax.set_xticks(x_pos)
    ax.set_xticklabels(result_df['Subitem_English'], rotation=45, ha='right', fontsize=XTICK_FONT_SIZE)

    # 设置y轴刻度和范围
    ax.set_yticks(Y_TICKS)
    ax.set_ylim(bottom=min(Y_TICKS), top=max(Y_TICKS))
    ax.yaxis.set_tick_params(labelsize=YTICK_FONT_SIZE)

    # 绘制分割虚线 - 修正为大组之间的位置
    for pos in DIVIDER_POSITIONS:
        if pos < len(x_pos):
            # 计算大组之间的实际x坐标位置
            divider_x = (x_pos[int(np.floor(pos))] + x_pos[int(np.ceil(pos))]) / 2
            ax.axvline(x=divider_x, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
            print(f"分割线位置: {divider_x} (在 {result_df.iloc[int(np.floor(pos))]['Subitem_English']} 和 {result_df.iloc[int(np.ceil(pos))]['Subitem_English']} 之间)")

    # 添加大类别标签 - 使用超参数配置
    for category_name, label_params in CATEGORY_LABELS.items():
        if label_params['x'] < len(x_pos):
            label_x = x_pos[int(label_params['x'])]
            label_y = ax.get_ylim()[1] * label_params['y']

            ax.text(label_x, label_y, category_name,
                    ha='center', va='top', fontsize=label_params['fontsize'], style='italic',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgray',
                             alpha=label_params['box_alpha']))
            print(f"标签位置 {category_name}: x={label_x}")

    # 设置y轴标签
    ax.set_ylabel('5D3S-QSA Score', fontsize=YLABEL_FONT_SIZE, fontweight='bold', labelpad=8)

    # 添加图例 - 使用超参数配置
    ax.legend(frameon=True, fancybox=False, shadow=False,
              edgecolor='black', facecolor='white', framealpha=LEGEND_BOX_ALPHA,
              loc='upper left', bbox_to_anchor=(LEGEND_X, LEGEND_Y), fontsize=LEGEND_FONT_SIZE)

    # 移除上右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 添加网格
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # 调整布局
    plt.tight_layout()

    # 显示统计摘要
    print("\n" + "="*80)
    print("统计摘要")
    print("="*80)
    print(f"微调模型总体: {result_df['Fine-tuned_Mean'].mean():.4f} ± {result_df['Fine-tuned_Mean'].std():.4f}")
    print(f"基础模型总体: {result_df['Base_Mean'].mean():.4f} ± {result_df['Base_Mean'].std():.4f}")

    # 保存详细统计结果
    result_df.to_excel('model_comparison_statistics.xlsx', index=False)
    print(f"\n详细统计结果已保存到 'model_comparison_statistics.xlsx'")

    plt.show()

    return result_df

# 运行主函数
if __name__ == "__main__":
    statistics_result = calculate_statistics_and_plot('a2.xlsx')