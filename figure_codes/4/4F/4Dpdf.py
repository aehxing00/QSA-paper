import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 超参数配置区域 (视觉复刻) ====================
# 导出设置
OUTPUT_PDF = 'Model_Comparison_Vector.pdf'
DPI = 600

# 字体大小
YLABEL_FONT_SIZE = 30    # Y轴标题字号
XTICK_FONT_SIZE = 25     # X轴刻度字号
YTICK_FONT_SIZE = 25     # Y轴刻度字号
LEGEND_FONT_SIZE = 22    # 图例字号
BOX_FONT_SIZE = 20       # 顶部标签框字号

# 比例与线宽
FIG_SIZE = (16, 7.5)     # 画布比例
SPINE_WIDTH = 2.0        # 坐标轴粗细
BAR_WIDTH = 0.35         # 柱子宽度
GAP_BETWEEN_GROUPS = 0.6 # 组间距

# 顶部标签定位 (关键：复刻上下交错位置)
# y_offset: 相对于顶部的偏移，越大越靠下
CATEGORY_CONFIG = {
    'Ontological Distinction\n(I Exist)':   {'x_idx': 1,  'y_val': 0.72, 'box_color': '#E0E0E0'}, # 偏高
    'Depth Perception\n(I Perceive)':      {'x_idx': 4,  'y_val': 0.55, 'box_color': '#E0E0E0'}, # 偏低
    'Recursive Thinking\n(I Think)':       {'x_idx': 7,  'y_val': 0.55, 'box_color': '#E0E0E0'}, # 偏低
    'Social Mirroring\n(I Interact)':      {'x_idx': 10, 'y_val': 0.55, 'box_color': '#E0E0E0'}, # 偏低
    'Identity & Personality\n(I Endure)':  {'x_idx': 13, 'y_val': 0.72, 'box_color': '#E0E0E0'}  # 偏高
}

# y轴范围与刻度
Y_LIMIT = 0.8
Y_TICKS = [0.0, 0.2, 0.4, 0.6, 0.8]

# 映射关系
marker_mapping = {
    '1A': 'Boundary Sense', '1B': 'Self-Awareness', '1C': 'Subjectivity',
    '2A': 'Multimodal Integration', '2B': 'World Model', '2C': 'Embodiment',
    '3A': 'Recursive Reflection', '3B': 'Metacognition', '3C': 'Error Correction',
    '4A': 'Mirroring Others', '4B': 'Role Understanding', '4C': 'Interactional Synchrony',
    '5A': 'Time Perception', '5B': 'Desire & Purpose', '5C': 'Core Personality'
}
# =================================================================

def set_professional_style():
    """设置学术矢量图风格"""
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['pdf.fonttype'] = 42  # 关键：导出可编辑文字
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['axes.linewidth'] = SPINE_WIDTH
    plt.rcParams['xtick.major.width'] = SPINE_WIDTH
    plt.rcParams['ytick.major.width'] = SPINE_WIDTH

def process_data(input_file):
    df = pd.read_excel(input_file)
    # 假设微调模型在前5列，基础模型在后5列
    ft_cols = df.columns[1:6]
    base_cols = df.columns[6:11]

    results = []
    for _, row in df.iterrows():
        marker = row.iloc[0]
        ft_vals = row[ft_cols].astype(float).dropna()
        base_vals = row[base_cols].astype(float).dropna()

        results.append({
            'Marker': marker,
            'Name': marker_mapping.get(marker, marker),
            'FT_Mean': ft_vals.mean(),
            'FT_Std': ft_vals.std(),
            'Base_Mean': base_vals.mean(),
            'Base_Std': base_vals.std()
        })

    res_df = pd.DataFrame(results)
    # 强制排序
    order = list(marker_mapping.keys())
    res_df['sort'] = res_df['Marker'].map({k: i for i, k in enumerate(order)})
    return res_df.sort_values('sort')

def plot_comparison(df):
    set_professional_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # 计算X轴坐标
    x_pos = np.arange(len(df)) * (BAR_WIDTH * 2.5 + GAP_BETWEEN_GROUPS)

    # 颜色
    color_ft = '#A23B72'   # 莫兰迪紫
    color_base = '#2E86AB' # 莫兰迪蓝

    # 绘制柱状图
    ax.bar(x_pos - BAR_WIDTH/2, df['FT_Mean'], BAR_WIDTH, color=color_ft,
           edgecolor='black', linewidth=1, label='Fine-tuned Model', zorder=3)
    ax.bar(x_pos + BAR_WIDTH/2, df['Base_Mean'], BAR_WIDTH, color=color_base,
           edgecolor='black', linewidth=1, label='Base Model', zorder=3)

    # 绘制误差线
    error_cfg = dict(fmt='none', c='black', capsize=3, elinewidth=1.2, capthick=1.2, zorder=4)
    ax.errorbar(x_pos - BAR_WIDTH/2, df['FT_Mean'], yerr=df['FT_Std'], **error_cfg)
    ax.errorbar(x_pos + BAR_WIDTH/2, df['Base_Mean'], yerr=df['Base_Std'], **error_cfg)

    # 绘制分割线
    for i in [2.5, 5.5, 8.5, 11.5]:
        divider_x = (x_pos[int(i-0.5)] + x_pos[int(i+0.5)]) / 2
        ax.axvline(x=divider_x, color='gray', linestyle='--', alpha=0.5, linewidth=1, zorder=1)

    # 设置标签框 (准确错位定位)
    for label, cfg in CATEGORY_CONFIG.items():
        lx = x_pos[cfg['x_idx']]
        ly = cfg['y_val']
        ax.text(lx, ly, label, ha='center', va='center', fontsize=BOX_FONT_SIZE,
                style='italic', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=cfg['box_color'],
                          edgecolor='black', linewidth=1, alpha=0.9), zorder=5)

    # 坐标轴修饰
    ax.set_ylim(0, Y_LIMIT)
    ax.set_yticks(Y_TICKS)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df['Name'], rotation=45, ha='right', fontsize=XTICK_FONT_SIZE)
    ax.set_ylabel('5D3S-QSA Score', fontsize=YLABEL_FONT_SIZE, fontweight='bold')

    # 图例 (顶部中央加粗框)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1), ncol=2,
              fontsize=LEGEND_FONT_SIZE, frameon=True, edgecolor='black', framealpha=1)

    # 移除网格与边框美化
    ax.grid(axis='y', alpha=0.2, zorder=0)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.tight_layout()

    # 保存PDF矢量图
    plt.savefig(OUTPUT_PDF, format='pdf', dpi=DPI, bbox_inches='tight')
    plt.savefig('Preview.png', dpi=300) # 同时保存预览图
    print(f"成功保存矢量图至: {OUTPUT_PDF}")
    plt.show()

if __name__ == "__main__":
    # 请确保 a2.xlsx 存在
    data = process_data('a2.xlsx')
    plot_comparison(data)