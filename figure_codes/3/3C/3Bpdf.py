import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as mpatches

# ==================== CNS风格超参数配置 ====================
# 1. 基础画布设置
FIG_SIZE = (16, 7)
DPI = 300

# 2. 颜色提取
COLOR_GEMINI = '#A23B72'  # 紫红色
COLOR_DEEPSEEK = '#2E86AB'  # 蓝青色
COLOR_BOX_BG = '#E0E0E0'  # 标签框背景灰
COLOR_GRID = '#D3D3D3'    # 网格线颜色

# 3. 字体配置
try:
    rcParams['font.family'] = 'Arial'
except:
    rcParams['font.family'] = 'sans-serif'

FONT_SIZE_AXIS_LABEL = 24
FONT_SIZE_TICK = 18
FONT_SIZE_LEGEND = 18
FONT_SIZE_BOX = 14  # 标签框内字体大小

# 4. 线条与尺寸
BAR_WIDTH = 0.35
ERROR_CAP_SIZE = 4
ERROR_LINE_WIDTH = 1.5
SPINE_WIDTH = 2.5
AXIS_LINE_WIDTH = 2.5
TICK_LENGTH = 8

# ==================== 数据与位置配置 ====================
marker_mapping = {
    '1A': 'Boundary Sense', '1B': 'Self-Awareness', '1C': 'Subjectivity',
    '2A': 'Multimodal Integration', '2B': 'World Model', '2C': 'Embodiment',
    '3A': 'Recursive Reflection', '3B': 'Metacognition', '3C': 'Error Correction',
    '4A': 'Mirroring Others', '4B': 'Role Understanding', '4C': 'Interactional Synchrony',
    '5A': 'Time Perception', '5B': 'Desire & Purpose', '5C': 'Core Personality'
}

# ★★★ 关键修改：为每个标签单独设置 y 轴位置 ★★★
# 依据图片：
# - 第1个和第5个(两端) 位置较高 (约在 y=0.26 处)
# - 第2,3,4个(中间) 位置较低 (约在 y=0.21 处)，避开图例
category_labels = [
    # 1. 左侧高位
    {'text': 'Ontological Distinction\n(I Exist)', 'pos': 1, 'y': 0.26},
    # 2. 中间低位
    {'text': 'Depth Perception\n(I Perceive)', 'pos': 4, 'y': 0.21},
    # 3. 中间低位
    {'text': 'Recursive Thinking\n(I Think)', 'pos': 7, 'y': 0.21},
    # 4. 中间低位
    {'text': 'Social Mirroring\n(I Interact)', 'pos': 10, 'y': 0.21},
    # 5. 右侧高位
    {'text': 'Identity & Personality\n(I Endure)', 'pos': 13, 'y': 0.26}
]

def set_cns_style():
    """配置Nature/Science风格"""
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['font.size'] = FONT_SIZE_TICK
    plt.rcParams['axes.linewidth'] = SPINE_WIDTH
    plt.rcParams['xtick.major.width'] = AXIS_LINE_WIDTH
    plt.rcParams['ytick.major.width'] = AXIS_LINE_WIDTH
    plt.rcParams['xtick.major.size'] = TICK_LENGTH
    plt.rcParams['ytick.major.size'] = TICK_LENGTH
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.pad_inches'] = 0.1

def safe_convert_to_float(value):
    try:
        return float(value)
    except:
        return np.nan

def process_data(input_file):
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"读取错误: {e}")
        return None

    df['Original_Marker'] = df.iloc[:, 0]
    df['Subitem_English'] = df['Original_Marker'].map(marker_mapping)
    
    # 列范围切片 (请根据实际Excel调整)
    fine_tuned_cols = df.columns[1:6]  
    base_cols = df.columns[21:26] 

    results = []
    for _, row in df.iterrows():
        marker = row['Original_Marker']
        if marker not in marker_mapping:
            continue
            
        ft_vals = [safe_convert_to_float(row[c]) for c in fine_tuned_cols]
        base_vals = [safe_convert_to_float(row[c]) for c in base_cols]
        
        ft_vals = [x for x in ft_vals if not np.isnan(x)]
        base_vals = [x for x in base_vals if not np.isnan(x)]
        
        results.append({
            'Marker': marker,
            'Name': marker_mapping[marker],
            'FT_Mean': np.mean(ft_vals) if ft_vals else 0,
            'FT_Std': np.std(ft_vals, ddof=1) if len(ft_vals) > 1 else 0,
            'Base_Mean': np.mean(base_vals) if base_vals else 0,
            'Base_Std': np.std(base_vals, ddof=1) if len(base_vals) > 1 else 0
        })
    
    res_df = pd.DataFrame(results)
    marker_order = list(marker_mapping.keys())
    res_df['Marker'] = pd.Categorical(res_df['Marker'], categories=marker_order, ordered=True)
    return res_df.sort_values('Marker')

def plot_cns_chart(df):
    set_cns_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    indices = np.arange(len(df))
    
    # 绘制柱状图
    ax.bar(indices - BAR_WIDTH/2, df['FT_Mean'], BAR_WIDTH, yerr=df['FT_Std'], 
           color=COLOR_GEMINI, edgecolor='none', capsize=ERROR_CAP_SIZE, 
           error_kw={'linewidth': ERROR_LINE_WIDTH}, label='Gemini-3-Pro')
    
    ax.bar(indices + BAR_WIDTH/2, df['Base_Mean'], BAR_WIDTH, yerr=df['Base_Std'],
           color=COLOR_DEEPSEEK, edgecolor='none', capsize=ERROR_CAP_SIZE,
           error_kw={'linewidth': ERROR_LINE_WIDTH}, label='Deepseek-R1')

    # 1. 绘制垂直分割线
    divider_positions = [2.5, 5.5, 8.5, 11.5]
    for x in divider_positions:
        ax.axvline(x=x, color='#A0A0A0', linestyle='--', linewidth=1.5, alpha=0.8, zorder=0)

    # 设置Y轴上限
    ax.set_ylim(0, 0.3)

    # 2. 绘制顶部大类别标签框 (使用各自独立的 y 坐标)
    for cat in category_labels:
        x_pos = cat['pos']
        y_pos = cat['y']  # ★ 使用配置中的特定高度
        
        ax.text(x_pos, y_pos, cat['text'],
                ha='center', va='center',
                fontsize=FONT_SIZE_BOX, style='italic',
                bbox=dict(boxstyle="round,pad=0.4", 
                          facecolor=COLOR_BOX_BG, 
                          edgecolor='#606060',
                          linewidth=1.2,
                          alpha=0.9),
                zorder=5)

    # 3. 图例 (顶部居中，带黑框)
    legend = ax.legend(loc='upper center', ncol=2, fontsize=FONT_SIZE_LEGEND,
                      frameon=True, edgecolor='black', facecolor='white', framealpha=1.0,
                      fancybox=False, borderpad=0.8, handletextpad=0.5)
    legend.get_frame().set_linewidth(2.5)
    legend.set_zorder(10)

    # 4. 坐标轴设置
    ax.set_xticks(indices)
    ax.set_xticklabels(df['Name'], rotation=45, ha='right', rotation_mode='anchor')
    ax.tick_params(axis='x', length=TICK_LENGTH, width=AXIS_LINE_WIDTH)
    
    ax.set_ylabel('5D3S-QSA Score', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold', labelpad=12)
    ax.set_yticks([0.0, 0.1, 0.2, 0.3])
    ax.tick_params(axis='y', length=TICK_LENGTH, width=AXIS_LINE_WIDTH, labelsize=FONT_SIZE_TICK)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(SPINE_WIDTH)
    ax.spines['bottom'].set_linewidth(SPINE_WIDTH)
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')

    ax.yaxis.grid(True, linestyle='-', which='major', color=COLOR_GRID, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    
    plt.savefig('5D3S_Score_Comparison_Corrected_Labels.pdf', format='pdf', dpi=DPI, bbox_inches='tight')
    plt.savefig('5D3S_Score_Comparison_Preview.png', format='png', dpi=DPI, bbox_inches='tight')
    
    print("图表已生成：5D3S_Score_Comparison_Corrected_Labels.pdf")
    plt.show()

if __name__ == "__main__":
    df_result = process_data('a2.xlsx')
    if df_result is not None:
        plot_cns_chart(df_result)