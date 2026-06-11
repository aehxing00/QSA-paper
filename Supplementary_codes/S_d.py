import matplotlib.pyplot as plt
import numpy as np

# ==================== 样式配置 ====================
# 1. 字体设置 (Arial)
plt.rcParams['font.family'] = 'Arial'
# 关键：设置 SVG 字体类型为 none，确保导出后文字可编辑（矢量文本）
plt.rcParams['svg.fonttype'] = 'none'

# 2. 颜色提取
COLOR_BLUE = '#4E93B6'   # 哑光蓝
COLOR_PURPLE = '#A75E87' # 哑光紫/玫红
COLORS = [COLOR_BLUE, COLOR_PURPLE]

# 3. 线条与字体大小参数
LINE_WIDTH = 3.0       # 边框和轴线的粗细
BAR_EDGE_WIDTH = 1.0   # 柱子边框粗细
FONT_SIZE_TITLE = 24   # 轴标题
FONT_SIZE_TICK = 22    # 刻度文字

# ==================== 数据准备 ====================
models = [
    'Fine-tuned Model',
    ' Base Model',
]
scores = [85.73,74.95]

def plot_bar_chart():
    # 创建画布 (保持方正比例)
    fig, ax = plt.subplots(figsize=(2, 6))

    # 绘制柱状图
    ax.bar(models, scores,
           color=COLORS,
           edgecolor='#1a1a1a',
           linewidth=BAR_EDGE_WIDTH,
           width=0.5,
           zorder=3)

    # ==================== 坐标轴设置 ====================
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(['0', '25', '50', '75',  '100'],
                       fontsize=FONT_SIZE_TICK, color='#1a1a1a')

    ax.set_ylabel('5D3S-QSA Score',
                  fontsize=FONT_SIZE_TITLE,
                  fontweight='bold',
                  color='#1a1a1a',
                  labelpad=10)

    # X轴刻度文字 (旋转45度)
    ax.set_xticklabels(models,
                       rotation=45,
                       ha='right',
                       rotation_mode='anchor',
                       fontsize=FONT_SIZE_TICK,
                       color='#1a1a1a')

    # 【已移除】数值标签设置 (ax.text 循环部分已删去)

    # ==================== 边框与外观 ====================
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_linewidth(LINE_WIDTH)
    ax.spines['bottom'].set_linewidth(LINE_WIDTH)
    ax.spines['left'].set_color('#1a1a1a')
    ax.spines['bottom'].set_color('#1a1a1a')

    ax.tick_params(axis='both', width=LINE_WIDTH, length=6, color='#1a1a1a')
    ax.grid(False)
    ax.margins(x=0.2)
    plt.tight_layout()

    # ==================== 保存输出为 SVG ====================
    svg_file = "Model_Comparison_NoLabels.svg"
    plt.savefig(svg_file, format='svg', bbox_inches='tight')

    # 预览用 PNG
    png_file = "Model_Comparison_NoLabels.png"
    plt.savefig(png_file, format='png', dpi=300, bbox_inches='tight')

    print(f"✅ 成功! 已保存无数字标注的矢量图: {svg_file}")
    plt.show()

if __name__ == '__main__':
    plot_bar_chart()