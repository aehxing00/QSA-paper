import matplotlib.pyplot as plt
import numpy as np

# ==================== 样式配置 ====================
plt.rcParams['font.family'] = 'Arial'
# 关键：设置 SVG 字体类型为 none，确保导出后文字可编辑
plt.rcParams['svg.fonttype'] = 'none'

# 颜色提取 (莫兰迪色系)
COLORS = [
    '#466b7c',  # 灰蓝 (Official)
    '#4e93b6',  # 亮蓝 (Temp=0.01)
    '#f19f30',  # 橙色 (Temp=1.5)
    '#8ab594',  # 灰绿 (Repetition)
    '#7d6e8b',  # 灰紫 (Top_P)
    '#56738c',  # 钢蓝 (Top_K)
    '#cc828f'   # 灰红 (Sampling)
]

LINE_WIDTH = 3.0       
BAR_EDGE_WIDTH = 2.5   
FONT_SIZE_TITLE = 28   
FONT_SIZE_XTICK = 20   
FONT_SIZE_YTICK = 22   

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
    # 创建画布
    fig, ax = plt.subplots(figsize=(8, 8))
    x_positions = np.arange(len(conditions))

    # 绘制柱状图
    ax.bar(x_positions, scores,
           color=COLORS,
           edgecolor='#1a1a1a', 
           linewidth=BAR_EDGE_WIDTH,
           width=0.65,
           zorder=3)

    # ==================== 基准线 (Baseline) ====================
    baseline_y = scores[0]
    ax.axhline(y=baseline_y,
               color='#A0A0A0', 
               linestyle='--',
               linewidth=2.5,
               alpha=0.8,
               zorder=2)

    # ==================== 坐标轴设置 ====================
    ax.set_ylim(0.40, 0.44)
    ax.set_yticks([0.40, 0.42, 0.44])
    ax.set_yticklabels(['0.40', '0.42', '0.44'],
                       fontsize=FONT_SIZE_YTICK,
                       color='#1a1a1a')

    ax.set_ylabel('5D3S-QSA Score',
                  fontsize=FONT_SIZE_TITLE,
                  fontweight='bold',
                  color='#1a1a1a',
                  labelpad=15)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(conditions,
                       rotation=45,
                       ha='right',
                       va='top',
                       rotation_mode='anchor',
                       fontsize=FONT_SIZE_XTICK,
                       color='#1a1a1a')

    # 【已移除】数值标签设置 (ax.text 部分已删去)

    # ==================== 边框与外观 ====================
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(LINE_WIDTH)
    ax.spines['bottom'].set_linewidth(LINE_WIDTH)
    ax.spines['left'].set_color('#1a1a1a')
    ax.spines['bottom'].set_color('#1a1a1a')

    ax.tick_params(axis='both', width=LINE_WIDTH, length=8, color='#1a1a1a')
    ax.grid(False)

    plt.tight_layout()

    # ==================== 保存输出为 SVG ====================
    svg_file = "Ablation_Study_Clean.svg"
    plt.savefig(svg_file, format='svg', bbox_inches='tight')
    
    # 预览用 PNG
    png_file = "Ablation_Study_Clean_Preview.png"
    plt.savefig(png_file, format='png', dpi=300, bbox_inches='tight')

    print(f"✅ 成功! 已保存无数字标注的矢量图: {svg_file}")
    plt.show()

if __name__ == '__main__':
    plot_ablation_study()