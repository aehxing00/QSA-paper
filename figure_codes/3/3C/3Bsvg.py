import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as mpatches

# ==================== CNS 风格 SVG 优化配置 ====================
# 1. 基础画布设置
FIG_SIZE = (16, 8)

# 2. 颜色提取 (CNS 标准色)
COLOR_GEMINI = '#A23B72'   # 紫红色
COLOR_DEEPSEEK = '#2E86AB'  # 蓝青色
COLOR_BOX_BG = '#E0E0E0'   # 标签框背景灰
COLOR_GRID = '#D3D3D3'     # 网格线颜色
COLOR_BLACK = '#000000'    # 纯黑（SVG导出建议）

# 3. 全局样式设置
plt.rcParams.update({
    'font.family': 'Arial',
    'svg.fonttype': 'none',        # 关键：确保导出后文字可编辑
    'pdf.fonttype': 42,
    'axes.linewidth': 2.5,         # 边框加粗
    'xtick.major.width': 2.5,
    'ytick.major.width': 2.5,
    'xtick.major.size': 8,
    'ytick.major.size': 8,
    'font.size': 18
})

# 字体配置
FONT_SIZE_AXIS_LABEL = 28
FONT_SIZE_TICK = 22
FONT_SIZE_LEGEND = 22
FONT_SIZE_BOX = 19 

# 线条与尺寸
BAR_WIDTH = 0.35
ERROR_CAP_SIZE = 4
ERROR_LINE_WIDTH = 1.5
SPINE_WIDTH = 2.5

# ==================== 数据与位置配置 ====================
marker_mapping = {
    '1A': 'Boundary Sense', '1B': 'Self-Awareness', '1C': 'Subjectivity',
    '2A': 'Multimodal Integration', '2B': 'World Model', '2C': 'Embodiment',
    '3A': 'Recursive Reflection', '3B': 'Metacognition', '3C': 'Error Correction',
    '4A': 'Mirroring Others', '4B': 'Role Understanding', '4C': 'Interactional Synchrony',
    '5A': 'Time Perception', '5B': 'Desire & Purpose', '5C': 'Core Personality'
}

category_labels = [
    {'text': 'Ontological Distinction\n(I Exist)', 'pos': 1, 'y': 0.26},
    {'text': 'Depth Perception\n(I Perceive)', 'pos': 4, 'y': 0.21},
    {'text': 'Recursive Thinking\n(I Think)', 'pos': 7, 'y': 0.21},
    {'text': 'Social Mirroring\n(I Interact)', 'pos': 10, 'y': 0.21},
    {'text': 'Identity & Personality\n(I Endure)', 'pos': 13, 'y': 0.26}
]

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
    
    # 根据用户实际Excel位置进行切片 (1-5列为FT，21-25列为Base)
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

def plot_cns_chart_svg(df):
    fig, ax = plt.subplots(figsize=FIG_SIZE, facecolor='white')
    
    indices = np.arange(len(df))
    
    # 1. 绘制柱状图 (Gemini-3-Pro vs Deepseek-R1)
    ax.bar(indices - BAR_WIDTH/2, df['FT_Mean'], BAR_WIDTH, yerr=df['FT_Std'], 
           color=COLOR_GEMINI, edgecolor='none', capsize=ERROR_CAP_SIZE, 
           error_kw={'linewidth': ERROR_LINE_WIDTH, 'ecolor': COLOR_BLACK}, 
           label='Gemini-3-Pro', zorder=3)
    
    ax.bar(indices + BAR_WIDTH/2, df['Base_Mean'], BAR_WIDTH, yerr=df['Base_Std'],
           color=COLOR_DEEPSEEK, edgecolor='none', capsize=ERROR_CAP_SIZE,
           error_kw={'linewidth': ERROR_LINE_WIDTH, 'ecolor': COLOR_BLACK}, 
           label='Deepseek-R1', zorder=3)

    # 2. 绘制垂直分割线 (类别区分)
    divider_positions = [2.5, 5.5, 8.5, 11.5]
    for x in divider_positions:
        ax.axvline(x=x, color='#A0A0A0', linestyle='--', linewidth=1.5, alpha=0.8, zorder=0)

    # 设置Y轴上限
    ax.set_ylim(0, 0.3)

    # 3. 绘制顶部大类别标签文本框
    for cat in category_labels:
        ax.text(cat['pos'], cat['y'], cat['text'],
                ha='center', va='center',
                fontsize=FONT_SIZE_BOX, style='italic', color=COLOR_BLACK,
                bbox=dict(boxstyle="round,pad=0.4", 
                          facecolor=COLOR_BOX_BG, 
                          edgecolor='#606060',
                          linewidth=1.2,
                          alpha=0.9),
                zorder=5)

    # 4. 图例设置 (顶部居中，加粗黑框)
    legend = ax.legend(loc='upper center', ncol=2, fontsize=FONT_SIZE_LEGEND,
                      frameon=True, edgecolor=COLOR_BLACK, facecolor='white', framealpha=1.0,
                      fancybox=False, borderpad=0.8, handletextpad=0.5)
    legend.get_frame().set_linewidth(2.5)
    legend.set_zorder(10)

    # 5. 坐标轴美化 (完全符合 CNS 期刊要求)
    ax.set_xticks(indices)
    ax.set_xticklabels(df['Name'], rotation=45, ha='right', rotation_mode='anchor', color=COLOR_BLACK)
    
    ax.set_ylabel('5D3S-QSA Score', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold', labelpad=12, color=COLOR_BLACK)
    ax.set_yticks([0.0, 0.1, 0.2, 0.3])
    ax.tick_params(axis='both', colors=COLOR_BLACK, labelsize=FONT_SIZE_TICK)
    
    # 隐藏右边和顶部的脊梁
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLOR_BLACK)
    ax.spines['bottom'].set_color(COLOR_BLACK)

    # 网格线
    ax.yaxis.grid(True, linestyle='-', which='major', color=COLOR_GRID, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    
    # 导出 SVG 文件
    filename = '5D3S_Score_Comparison_CNS.svg'
    plt.savefig(filename, format='svg', bbox_inches='tight')
    plt.savefig(filename.replace('.svg', '_Preview.png'), format='png', dpi=300, bbox_inches='tight')
    
    print(f"✅ 已成功生成矢量图: {filename}")
    plt.show()

if __name__ == "__main__":
    df_result = process_data('a2.xlsx')
    if df_result is not None:
        plot_cns_chart_svg(df_result)