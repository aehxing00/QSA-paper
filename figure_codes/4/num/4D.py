import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体（如果需要显示中文）
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# 设置CNS风格 - 取消网格背景
plt.style.use('seaborn-v0_8-white')
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 12,
    'axes.linewidth': 1.2,
    'grid.linewidth': 0,  # 设置为0以完全取消网格线
    'lines.linewidth': 2,
    'patch.linewidth': 1.2,
})

# 数据
models = [
    'Qwen3-0.6B',
    'Qwen3-1.7B',
    'Qwen3-4B'
]
scores = [0.1305, 0.1303, 0.4267]
colors = ['#2E86AB', '#A23B72', '#F18F01']  # 学术风格的配色

# 创建图形
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# 绘制柱状图
bars = ax.bar(models, scores, color=colors, edgecolor='black', linewidth=1.2,
              alpha=0.85, width=0.6)

# 自定义X轴标签 - 旋转45度
x_labels = ['Qwen3-0.6B', 'Qwen3-1.7B', 'Qwen3-4B']
ax.set_xticks(range(len(models)))
ax.set_xticklabels(x_labels, rotation=45, ha='right', va='top', rotation_mode='anchor')

# 设置Y轴
ax.set_ylim(0, 0.6)
ax.set_yticks([0, 0.2, 0.4, 0.6])
ax.set_ylabel('5D3S-QSA Score', fontsize=9, fontweight='bold')

# 添加数值标签
for i, (bar, score) in enumerate(zip(bars, scores)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{score:.4f}', ha='center', va='bottom', fontsize=9, fontweight='medium')

# 添加水平参考线（可选，如果需要参考线但不要网格）
# 取消注释以下代码以添加水平参考线但不显示网格
# for y in [0.1, 0.2, 0.3, 0.4, 0.5]:
#     ax.axhline(y=y, color='gray', linewidth=0.5, alpha=0.3, linestyle='--')

# 添加底部的基线
ax.axhline(y=0, color='black', linewidth=1.2, alpha=0.7)

# 取消网格背景
ax.grid(False)

# 设置边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

# 调整布局以适应旋转的标签
plt.tight_layout(pad=2.0)  # 增加内边距以适应旋转的标签
# 显示图形
plt.show()