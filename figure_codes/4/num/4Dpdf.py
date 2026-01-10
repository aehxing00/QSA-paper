import matplotlib.pyplot as plt
import numpy as np

# ==================== 样式配置 ====================
# 1. 字体设置 (Arial, 粗体效果)
plt.rcParams['font.family'] = 'Arial'
# 关键：设置 PDF 字体类型为 42 (TrueType)，确保导出后文字可编辑
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 2. 颜色提取 (从 4B.png 提取的近似色)
COLOR_BLUE = '#4E93B6'   # 哑光蓝
COLOR_PURPLE = '#A75E87' # 哑光紫/玫红
COLOR_ORANGE = '#F19F30' # 亮橙色
COLORS = [COLOR_BLUE, COLOR_PURPLE, COLOR_ORANGE]

# 3. 线条与字体大小参数
LINE_WIDTH = 3.0       # 边框和轴线的粗细
BAR_EDGE_WIDTH = 3.0   # 柱子边框粗细
FONT_SIZE_TITLE = 24   # 轴标题
FONT_SIZE_VALUE = 24   # 柱上数值
FONT_SIZE_TICK = 22    # 刻度文字

# ==================== 数据准备 ====================
models = [
    'Qwen3-0.6B',
    'Qwen3-1.7B',
    'Qwen3-4B'
]
scores = [0.1305, 0.1303, 0.4267]

def plot_bar_chart():
    # 创建画布 (保持方正比例)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))

    # 绘制柱状图
    # zorder=3 确保柱子在图层上方
    bars = ax.bar(models, scores, 
                  color=COLORS, 
                  edgecolor='#1a1a1a', # 近乎黑色的深灰，比纯黑更有质感
                  linewidth=BAR_EDGE_WIDTH,
                  width=0.6,           # 柱子宽度
                  zorder=3)

    # ==================== 坐标轴设置 ====================
    # Y轴范围与刻度
    ax.set_ylim(0, 0.6)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6])
    # Y轴刻度文字
    ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6'], 
                       fontsize=FONT_SIZE_TICK, color='#1a1a1a')
    
    # Y轴标题 (加粗，巨大)
    ax.set_ylabel('5D3S-QSA Score', 
                  fontsize=FONT_SIZE_TITLE, 
                  fontweight='bold', 
                  color='#1a1a1a',
                  labelpad=10)

    # X轴刻度文字 (旋转45度)
    ax.set_xticklabels(models, 
                       rotation=45, 
                       ha='right', 
                       rotation_mode='anchor', # 确保旋转轴点正确
                       fontsize=FONT_SIZE_TICK, 
                       color='#1a1a1a')

    # ==================== 数值标签设置 ====================
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.015,
                f'{score:.4f}',
                ha='center', va='bottom',
                fontsize=FONT_SIZE_VALUE,
                color='#1a1a1a')

    # ==================== 边框与外观 ====================
    # 隐藏上右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 加粗左下边框 (关键：复刻图片中的粗黑线)
    ax.spines['left'].set_linewidth(LINE_WIDTH)
    ax.spines['bottom'].set_linewidth(LINE_WIDTH)
    ax.spines['left'].set_color('#1a1a1a')
    ax.spines['bottom'].set_color('#1a1a1a')

    # 调整刻度线长度和粗细
    ax.tick_params(axis='both', width=LINE_WIDTH, length=6, color='#1a1a1a')

    # 确保没有网格
    ax.grid(False)

    # 调整布局，防止标签被切断
    plt.tight_layout()

    # ==================== 保存输出 ====================
    # 保存为 PDF (矢量)
    pdf_file = "Model_Comparison_Bar.pdf"
    plt.savefig(pdf_file, format='pdf', dpi=300, bbox_inches='tight')
    
    # 保存为 PNG (预览)
    png_file = "Model_Comparison_Bar.png"
    plt.savefig(png_file, format='png', dpi=300, bbox_inches='tight')
    
    print(f"图表已生成:\n1. {pdf_file} (矢量图)\n2. {png_file} (预览图)")
    plt.show()

if __name__ == '__main__':
    plot_bar_chart()