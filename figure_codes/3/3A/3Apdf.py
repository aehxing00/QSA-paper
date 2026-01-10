import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# ==================== 超参数配置区域 (针对CNS风格优化) ====================
# 图表尺寸 - 调整为更接近图片的长宽比 (不再过于扁长)
FIG_SIZE = (11, 8.5)

# 颜色配置 (保持原样或根据需要修改)
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#55A868', '#CC79A7', '#0072B2', '#D55E00', '#009E73']

# 字体设置 - 对应图片中的大号字体风格
FONT_FAMILY = 'Arial'  # 确保系统安装了Arial，否则会回退
AXIS_LABEL_FONT_SIZE = 24  # Y轴标题非常大
TICK_LABEL_FONT_SIZE = 20  # 坐标轴刻度字体
BAR_LABEL_FONT_SIZE = 20   # 柱子上方数字字体

# 柱状图样式
BAR_WIDTH = 0.65       # 稍微变窄一点点增加间隙感
EDGE_COLOR = 'white'
EDGE_WIDTH = 0         # 图片中柱子似乎没有明显的边框线，设为0或很细

# 误差线样式
ERROR_LINE_WIDTH = 2.5 # 加粗误差线
ERROR_CAP_SIZE = 6     # 加宽误差线帽子
ERROR_CAP_THICKNESS = 2.5

# 柱子数字标签高度
LABEL_HEIGHT_OFFSET = 0.005 # 根据数值量级微调

# 网格和边框
GRID_ALPHA = 0.3
SPINE_WIDTH = 3.0      # 图片中的坐标轴线很粗
TICK_LENGTH = 8        # 刻度线长度
TICK_WIDTH = 3.0       # 刻度线宽度

# 保存设置
DPI = 600
# ==================== 超参数配置区域结束 ====================

def set_cns_style():
    """设置CNS期刊级别的绘图风格"""
    # 关键设置：设置字体类型为42，这样导出的PDF文字是可编辑的(TrueType)，而不是轮廓
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    plt.rcParams['font.family'] = FONT_FAMILY
    plt.rcParams['font.size'] = TICK_LABEL_FONT_SIZE

    # 线条设置
    plt.rcParams['axes.linewidth'] = SPINE_WIDTH
    plt.rcParams['lines.linewidth'] = 1.5

    # 刻度设置 - 加粗加大
    plt.rcParams['xtick.major.width'] = TICK_WIDTH
    plt.rcParams['ytick.major.width'] = TICK_WIDTH
    plt.rcParams['xtick.major.size'] = TICK_LENGTH
    plt.rcParams['ytick.major.size'] = TICK_LENGTH

    # 布局
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = DPI
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.pad_inches'] = 0.1

def safe_convert_to_float(value):
    """安全地将值转换为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan

def calculate_model_statistics(df):
    """计算每个模型的统计量"""
    # 获取所有模型列（排除第一列Category）
    model_columns = df.columns[1:]

    # 识别重复测量的模型组（每5列是同一个模型的重复测量）
    model_groups = {}

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
            valid_values = []
            for value in column_data:
                float_value = safe_convert_to_float(value)
                if not np.isnan(float_value):
                    valid_values.append(float_value)

            if len(valid_values) > 0:
                column_mean = np.mean(valid_values)
                column_means.append(column_mean)

        if len(column_means) > 0:
            model_mean = np.mean(column_means)
            model_std = np.std(column_means, ddof=1)

            results.append({
                'Model': model_name,
                'Mean': model_mean,
                'Std': model_std,
                'N_columns': len(column_means),
            })

    return pd.DataFrame(results)

def create_cns_bar_plot(statistics_df):
    """创建CNS级别的柱状图并导出PDF"""

    # 设置样式
    set_cns_style()

    # 创建图形
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # 准备数据
    models = statistics_df['Model'].values
    means = statistics_df['Mean'].values
    stds = statistics_df['Std'].values

    # 生成x轴位置
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

    # 设置x轴标签 - 字体加大，旋转45度
    ax.set_xticks(x_pos)
    # 使用 set_fontweight('normal') 或 'bold' 取决于你的喜好，图片中X轴标签看起来是Regular
    ax.set_xticklabels(models, rotation=45, ha='right', rotation_mode='anchor',
                       fontsize=TICK_LABEL_FONT_SIZE, fontweight='normal')

    # 设置y轴标签 - 粗体，巨大
    ax.set_ylabel('5D3S-QSA Score', fontsize=AXIS_LABEL_FONT_SIZE,
                  fontweight='bold', labelpad=15)

    # 设置Y轴刻度字体
    ax.tick_params(axis='y', labelsize=TICK_LABEL_FONT_SIZE)

    # 自动调整y轴范围
    if len(means) > 0 and len(stds) > 0:
        y_max = max(means + stds) * 1.15 # 留出更多顶部空间给数字
        ax.set_ylim(0, y_max) # 强制从0开始，除非数据特殊

    # 添加数值标签在柱子上方 - 粗体，大号
    for i, (bar, mean) in enumerate(zip(bars, means)):
        height = bar.get_height()
        # 计算误差线顶端位置，确保文字在误差线之上
        error_height = stds[i] if len(stds) > i else 0
        text_y = height + error_height + LABEL_HEIGHT_OFFSET

        ax.text(bar.get_x() + bar.get_width()/2., text_y,
                f'{mean:.2f}',
                ha='center', va='bottom',
                fontsize=BAR_LABEL_FONT_SIZE,
                fontweight='bold') # 图片中的数字是加粗的

    # 美化图表 - 移除上边框和右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 确保左边和底部的线是黑色的且可见
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')

    # 添加Y轴网格 (可选，图片中似乎是非常淡的线或者没有)
    ax.grid(True, axis='y', alpha=GRID_ALPHA, linestyle='-', linewidth=1.0, zorder=0)
    ax.set_axisbelow(True)

    # 调整布局
    plt.tight_layout()

    # ==================== 导出部分 ====================
    # 保存为 PDF (矢量图)
    pdf_filename = '5D3S_QSA_Score_Analysis.pdf'
    plt.savefig(pdf_filename, format='pdf', dpi=DPI, bbox_inches='tight')
    print(f"图表已保存为PDF矢量图: {pdf_filename}")

    # 同时保存一张PNG用于快速预览
    plt.savefig('5D3S_QSA_Score_Analysis.png', format='png', dpi=DPI, bbox_inches='tight')

    plt.show()

    return fig, ax

def main():
    """主函数"""
    try:
        df = pd.read_excel('a2.xlsx')
        print("成功读取 a2.xlsx")
    except Exception as e:
        print(f"读取文件错误: {e}")
        # 为了演示，如果读取失败，这里可以生成假数据进行测试
        # create_dummy_data_and_plot()
        return

    print("计算模型统计量...")
    statistics_df = calculate_model_statistics(df)

    print("生成图表...")
    create_cns_bar_plot(statistics_df)

if __name__ == "__main__":
    main()