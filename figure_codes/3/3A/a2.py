import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# ==================== 超参数配置区域 ====================
# 图表尺寸
FIG_SIZE = (14, 6)

# 颜色配置
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#55A868', '#CC79A7', '#0072B2', '#D55E00', '#009E73']

# 字体设置
FONT_FAMILY = 'Arial'
TITLE_FONT_SIZE = 16
AXIS_LABEL_FONT_SIZE = 12
TICK_LABEL_FONT_SIZE = 12
LEGEND_FONT_SIZE = 12

# 柱状图样式
BAR_WIDTH = 0.7
EDGE_COLOR = 'white'
EDGE_WIDTH = 1.2

# 误差线样式
ERROR_LINE_WIDTH = 1.5
ERROR_CAP_SIZE = 3
ERROR_CAP_THICKNESS = 1.5

# 柱子数字标签高度
LABEL_HEIGHT_OFFSET = 0.01

# 网格和边框
GRID_ALPHA = 0.3
SPINE_WIDTH = 1.2

# 保存设置
DPI = 600
# ==================== 超参数配置区域结束 ====================

def set_cns_style():
    """设置CNS期刊级别的绘图风格"""
    plt.rcParams['font.family'] = FONT_FAMILY
    plt.rcParams['font.size'] = TICK_LABEL_FONT_SIZE
    plt.rcParams['axes.linewidth'] = SPINE_WIDTH
    plt.rcParams['lines.linewidth'] = 1.5
    plt.rcParams['xtick.major.width'] = SPINE_WIDTH
    plt.rcParams['ytick.major.width'] = SPINE_WIDTH
    plt.rcParams['xtick.major.size'] = 6
    plt.rcParams['ytick.major.size'] = 6
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
        # 获取当前组的5列
        group_columns = model_columns[i:i+5]
        if len(group_columns) > 0:
            # 使用每5列的第一列名称作为模型名称
            model_name = group_columns[0]
            model_groups[model_name] = group_columns

    print("识别到的模型分组:")
    for model, cols in model_groups.items():
        print(f"  {model}: {len(cols)}列")

    # 计算每个模型的统计量
    results = []
    for model_name, columns in model_groups.items():
        # 计算每列的平均值（排除第一行）
        column_means = []

        for col in columns:
            # 获取该列数据（排除第一行）
            column_data = df[col].iloc[1:]  # 从第二行开始

            # 安全转换为浮点数并移除NaN值
            valid_values = []
            for value in column_data:
                float_value = safe_convert_to_float(value)
                if not np.isnan(float_value):
                    valid_values.append(float_value)

            if len(valid_values) > 0:
                column_mean = np.mean(valid_values)
                column_means.append(column_mean)
                print(f"    {col}: 平均值 = {column_mean:.4f} (有效数据点: {len(valid_values)})")

        if len(column_means) > 0:
            # 计算5列平均值的平均值作为模型平均值
            model_mean = np.mean(column_means)
            # 计算5列平均值的标准差作为模型标准差
            model_std = np.std(column_means, ddof=1)

            results.append({
                'Model': model_name,
                'Mean': model_mean,
                'Std': model_std,
                'N_columns': len(column_means),
                'Column_Means': column_means  # 保存每列的平均值用于调试
            })

    return pd.DataFrame(results)

def create_cns_bar_plot(statistics_df):
    """创建CNS级别的柱状图"""

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

    # 添加误差线（显示平均值±标准差）
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.errorbar(x_pos[i], mean,
                   yerr=std,  # 完整的标准差
                   fmt='none',
                   color='black',
                   linewidth=ERROR_LINE_WIDTH,
                   capsize=ERROR_CAP_SIZE,
                   capthick=ERROR_CAP_THICKNESS,
                   zorder=4)

    # 设置x轴标签 - 45度倾斜
    ax.set_xticks(x_pos)
    ax.set_xticklabels(models, rotation=45, ha='right', rotation_mode='anchor')

    # 设置y轴
    ax.set_ylabel('5D3S-QSA Score', fontsize=AXIS_LABEL_FONT_SIZE,
                  fontweight='bold', labelpad=10)

    # 自动调整y轴范围，留出空间给误差线
    if len(means) > 0 and len(stds) > 0:
        y_min = max(0, min(means - stds) * 0.95)
        y_max = max(means + stds) * 1.05
        ax.set_ylim(y_min, y_max)

    # 添加数值标签在柱子上方 - 只显示平均值
    for i, (bar, mean) in enumerate(zip(bars, means)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + LABEL_HEIGHT_OFFSET,
                f'{mean:.2f}',  # 只显示平均值，不显示标准差
                ha='center', va='bottom', fontsize=TICK_LABEL_FONT_SIZE-1,
                fontweight='bold')

    # 美化图表
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 添加网格
    ax.grid(True, axis='y', alpha=GRID_ALPHA, linestyle='-', linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)

    # 调整布局以适应倾斜的标签
    plt.tight_layout()

    # 只显示图表，不保存
    plt.show()

    return fig, ax

def main():
    """主函数"""
    # 读取数据
    try:
        df = pd.read_excel('a2.xlsx')
        print("成功读取 a2.xlsx")
        print(f"数据形状: {df.shape}")
        print(f"列名: {df.columns.tolist()}")
        print("\n前5行数据:")
        print(df.head())

    except Exception as e:
        print(f"读取文件错误: {e}")
        return

    # 计算模型统计量
    print("\n" + "="*60)
    print("计算模型统计量")
    print("="*60)

    statistics_df = calculate_model_statistics(df)

    print("\n模型统计结果:")
    print(statistics_df.to_string(index=False))

    # 创建柱状图
    print("\n" + "="*60)
    print("生成CNS级别柱状图")
    print("="*60)

    fig, ax = create_cns_bar_plot(statistics_df)

    # 打印统计摘要
    print("\n" + "="*60)
    print("统计摘要")
    print("="*60)
    for _, row in statistics_df.iterrows():
        print(f"{row['Model']}: {row['Mean']:.4f} ± {row['Std']:.4f} (列数: {row['N_columns']})")
        # 打印每列的平均值用于验证
        if 'Column_Means' in row:
            print(f"  各列平均值: {[f'{x:.4f}' for x in row['Column_Means']]}")

    # 保存统计结果（不包含Column_Means列）
    output_df = statistics_df.drop('Column_Means', axis=1, errors='ignore')
    output_df.to_excel('model_performance_statistics.xlsx', index=False)
    print(f"\n详细统计结果已保存到 'model_performance_statistics.xlsx'")

    return statistics_df

if __name__ == "__main__":
    # 运行主程序
    result_df = main()