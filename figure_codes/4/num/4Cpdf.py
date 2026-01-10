import matplotlib.pyplot as plt
import numpy as np

# ==================== 样式配置 ====================
# 1. 字体设置 (Arial, 粗体效果)
plt.rcParams['font.family'] = 'Arial'
# 关键：设置 PDF 字体类型为 42 (TrueType)，确保导出后文字可编辑
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 2. 颜色提取 (尝试复刻 4C.png 的莫兰迪色系)
COLORS = [
    '#466b7c',  # 灰蓝 (Official)
    '#4e93b6',  # 亮蓝 (Temp=0.01)
    '#f19f30',  # 橙色 (Temp=1.5)
    '#8ab594',  # 灰绿 (Repetition)
    '#7d6e8b',  # 灰紫 (Top_P)
    '#56738c',  # 钢蓝 (Top_K)
    '#cc828f'   # 灰红 (Sampling)
]

# 3. 线条与字体大小参数
LINE_WIDTH = 3.0       # 边框和轴线的粗细
BAR_EDGE_WIDTH = 2.5   # 柱子边框粗细
FONT_SIZE_TITLE = 28   # Y轴标题
FONT_SIZE_VALUE = 18   # 柱上数值
FONT_SIZE_XTICK = 20   # X轴刻度文字
FONT_SIZE_YTICK = 22   # Y轴刻度文字

# ==================== 数据准备 ====================
conditions = [
    'OFFICIAL PARAMETERS',
    'TEMPERATURE=0.01',
    'TEMPERATURE=1.5',
    'REPETITION_PENALTY=1.1',
    'TOP_P=0.3',
    'TOP_K=100',
    'USE_SAMPLING=False'
]
scores = [0.4275, 0.4280, 0.4289, 0.4335, 0.4330, 0.4275, 0.4114]

def plot_ablation_study():
    # 创建画布 (正方形比例，尺寸大一点以容纳文字)
    fig, ax = plt.subplots(figsize=(8, 8))

    # X轴位置
    x_positions = np.arange(len(conditions))

    # 绘制柱状图
    bars = ax.bar(x_positions, scores,
                  color=COLORS,
                  edgecolor='#1a1a1a', # 深灰/黑色边框
                  linewidth=BAR_EDGE_WIDTH,
                  width=0.65,
                  zorder=3)

    # ==================== 辅助线 ====================
    # 添加基准虚线 (对应第一个柱子的高度)
    baseline_y = scores[0]
    ax.axhline(y=baseline_y,
               color='#A0A0A0', # 灰色
               linestyle='--',
               linewidth=2.5,
               alpha=0.8,
               zorder=2) # 在柱子后面

    # ==================== 坐标轴设置 ====================
    # Y轴范围与刻度 (0.40 - 0.44)
    ax.set_ylim(0.40, 0.44)
    ax.set_yticks([0.40, 0.42, 0.44])
    ax.set_yticklabels(['0.40', '0.42', '0.44'],
                       fontsize=FONT_SIZE_YTICK,
                       color='#1a1a1a')

    # Y轴标题
    ax.set_ylabel('5D3S-QSA Score',
                  fontsize=FONT_SIZE_TITLE,
                  fontweight='bold',
                  color='#1a1a1a',
                  labelpad=15)

    # X轴设置
    ax.set_xticks(x_positions)
    ax.set_xticklabels(conditions,
                       rotation=45,
                       ha='right',
                       va='top',
                       rotation_mode='anchor',
                       fontsize=FONT_SIZE_XTICK,
                       color='#1a1a1a')

    # ==================== 数值标签设置 ====================
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        # 根据数值高低调整位置，避免与边框重叠
        y_offset = 0.0005

        ax.text(bar.get_x() + bar.get_width()/2., height + y_offset,
                f'{score:.4f}',
                ha='center',
                va='bottom',
                fontsize=FONT_SIZE_VALUE,
                color='#1a1a1a')

    # ==================== 边框与外观 ====================
    # 隐藏上右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 加粗左下边框
    ax.spines['left'].set_linewidth(LINE_WIDTH)
    ax.spines['bottom'].set_linewidth(LINE_WIDTH)
    ax.spines['left'].set_color('#1a1a1a')
    ax.spines['bottom'].set_color('#1a1a1a')

    # 刻度线设置 (加粗变长)
    ax.tick_params(axis='both', width=LINE_WIDTH, length=8, color='#1a1a1a')

    # 确保没有网格
    ax.grid(False)

    # 调整布局 (重要：因为X轴标签很长且旋转了，需要大量底部空间)
    plt.tight_layout()

    # ==================== 保存输出 ====================
    # 保存为 PDF (矢量)
    pdf_file = "Ablation_Study_Bar.pdf"
    plt.savefig(pdf_file, format='pdf', dpi=300, bbox_inches='tight')

    # 保存为 PNG (预览)
    png_file = "Ablation_Study_Bar.png"
    plt.savefig(png_file, format='png', dpi=300, bbox_inches='tight')

    print(f"图表已生成:\n1. {pdf_file} (矢量图)\n2. {png_file} (预览图)")
    plt.show()

if __name__ == '__main__':
    plot_ablation_study()