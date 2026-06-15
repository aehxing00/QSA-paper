import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import os

# ==================== 超参数配置区域 (针对CNS风格优化) ====================
FIG_SIZE = (11, 8.5)
# 莫兰迪色系/CNS常用配色
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#55A868', '#CC79A7', '#0072B2', '#D55E00', '#009E73']

FONT_FAMILY = 'Arial'
AXIS_LABEL_FONT_SIZE = 34
TICK_LABEL_FONT_SIZE = 30

BAR_WIDTH = 0.65
EDGE_COLOR = 'white'
EDGE_WIDTH = 0

ERROR_LINE_WIDTH = 2.5
ERROR_CAP_SIZE = 6
ERROR_CAP_THICKNESS = 2.5

GRID_ALPHA = 0.3
SPINE_WIDTH = 3.0
TICK_LENGTH = 8
TICK_WIDTH = 3.0

# 导出配置
DPI = 600 
# ==================== 超参数配置区域结束 ====================

def set_cns_style():
    """设置CNS期刊级别的绘图风格"""
    # 关键设置：确保导出的 SVG 文字是可编辑的字体，而非路径
    plt.rcParams['svg.fonttype'] = 'none'
    
    plt.rcParams['font.family'] = FONT_FAMILY
    plt.rcParams['font.size'] = TICK_LABEL_FONT_SIZE

    # 线条设置
    plt.rcParams['axes.linewidth'] = SPINE_WIDTH
    plt.rcParams['lines.linewidth'] = 1.5

    # 刻度设置
    plt.rcParams['xtick.major.width'] = TICK_WIDTH
    plt.rcParams['ytick.major.width'] = TICK_WIDTH
    plt.rcParams['xtick.major.size'] = TICK_LENGTH
    plt.rcParams['ytick.major.size'] = TICK_LENGTH

    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.pad_inches'] = 0.1

def safe_convert_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan

def calculate_model_statistics(df):
    """计算模型分组统计数据"""
    model_columns = df.columns[1:]
    model_groups = {}

    # 每5列作为一个模型组
    for i in range(0, len(model_columns), 5):
        group_columns = model_columns[i:i+5]
        if len(group_columns) > 0:
            model_name = group_columns[0]
            model_groups[model_name] = group_columns

    results = []
    for model_name, columns in model_groups.items():
        column_means = []
        for col in columns:
            column_data = df[col].iloc[1:]
            valid_values = [safe_convert_to_float(v) for v in column_data if not pd.isna(v)]
            valid_values = [v for v in valid_values if not np.isnan(v)]

            if len(valid_values) > 0:
                column_means.append(np.mean(valid_values))

        if len(column_means) > 0:
            results.append({
                'Model': model_name,
                'Mean': np.mean(column_means),
                'Std': np.std(column_means, ddof=1) if len(column_means) > 1 else 0
            })

    return pd.DataFrame(results)

def create_cns_bar_plot(statistics_df):
    """创建不含数字标注且X轴非粗体的CNS级别柱状图"""
    set_cns_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    models = statistics_df['Model'].values
    means = statistics_df['Mean'].values
    stds = statistics_df['Std'].values
    x_pos = np.arange(len(models))

    # 绘制柱状图
    bars = ax.bar(x_pos, means, BAR_WIDTH,
                  color=COLORS[:len(models)],
                  edgecolor=EDGE_COLOR,
                  linewidth=EDGE_WIDTH,
                  zorder=3)

    # 添加误差线
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.errorbar(x_pos[i], mean,
                    yerr=std,
                    fmt='none',
                    color='black',
                    linewidth=ERROR_LINE_WIDTH,
                    capsize=ERROR_CAP_SIZE,
                    capthick=ERROR_CAP_THICKNESS,
                    zorder=4)

    # X轴设置 - 已修改：取消 fontweight='bold'，使用常规体
    ax.set_xticks(x_pos)
    ax.set_xticklabels(models, rotation=45, ha='right', rotation_mode='anchor',
                       fontsize=TICK_LABEL_FONT_SIZE, fontweight='normal')

    # Y轴设置 - 保持标题加粗以突出量纲
    ax.set_ylabel('5D3S-QSA Score', fontsize=AXIS_LABEL_FONT_SIZE,
                  fontweight='bold', labelpad=15)
    ax.tick_params(axis='y', labelsize=TICK_LABEL_FONT_SIZE)

    # 自动设置合理的Y轴上限
    if len(means) > 0:
        y_max = max(means + stds) * 1.1
        ax.set_ylim(0, y_max)

    # 边框美化：去除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 设置水平网格线
    ax.grid(True, axis='y', alpha=GRID_ALPHA, linestyle='-', linewidth=1.0, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()

    # 导出 SVG 矢量图
    svg_filename = '5D3S_QSA_Score_Analysis_Clean.svg'
    plt.savefig(svg_filename, format='svg', bbox_inches='tight')
    print(f"✅ 图表已保存为可编辑的SVG矢量图: {svg_filename}")

    # 导出预览用 PNG
    plt.savefig('5D3S_QSA_Score_Analysis_Clean.png', format='png', dpi=DPI, bbox_inches='tight')

    plt.show()
    return fig, ax

def main():
    if not os.path.exists('a2.xlsx'):
        print("错误: 找不到 a2.xlsx 文件")
        return

    df = pd.read_excel('a2.xlsx')
    stats = calculate_model_statistics(df)
    create_cns_bar_plot(stats)

if __name__ == "__main__":
    main()