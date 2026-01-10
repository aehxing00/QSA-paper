import matplotlib.pyplot as plt
import numpy as np

# 设置专业字体和样式
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2

# 数据准备
categories = ['Mean Score', 'Base Model', 'Fine-tuned Model']
values = [0.087, 0.065, 0.369]

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(7, 8), dpi=300)

# 使用Nature期刊风格的配色
colors = ['#2E86AB', '#A23B72', '#F18F01']

# 绘制柱状图
bars = ax.bar(categories, values, color=colors, width=0.7,
              edgecolor='white', linewidth=2, alpha=0.95,
              capstyle='round')

# 在柱子顶部标注数值（更精致的样式）
for i, (bar, value) in enumerate(zip(bars, values)):
    height = bar.get_height()
    # 为不同柱子调整标注位置
    offset = 0.015 if value < 0.1 else 0.02
    ax.text(bar.get_x() + bar.get_width()/2., height + offset,
            f'{value:.3f}',
            ha='center', va='bottom',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white',
                     edgecolor='none', alpha=0.8))

# 设置y轴
y_ticks = [0, 0.1, 0.2, 0.3, 0.4]
ax.set_ylim(0, 0.42)
ax.set_yticks(y_ticks)
ax.set_ylabel('5D3S-QSA Scroe',
              fontsize=14, fontweight='bold', labelpad=15)

# 设置x轴标签45度倾斜
plt.xticks(rotation=45, ha='right', fontsize=12, fontweight='semibold')
ax.tick_params(axis='x', which='major', pad=10)

# 移除x轴标题（根据要求）
ax.set_xlabel('')  # 明确设置为空

# 精细美化图形
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)

# 设置精致的网格线
ax.grid(True, axis='y', alpha=0.4, linestyle='-', linewidth=0.8)
ax.set_axisbelow(True)

# 添加轻微的阴影效果
for bar in bars:
    bar.set_edgecolor('white')
    bar.set_linewidth(2)

# 调整布局以适应倾斜的标签
plt.tight_layout()

# 保存高质量图片
plt.savefig('CNS_quality_barplot_rotated.png', dpi=300,
            bbox_inches='tight', facecolor='white')
plt.savefig('CNS_quality_barplot_rotated.pdf',
            bbox_inches='tight', facecolor='white')

# 显示图形
plt.show()