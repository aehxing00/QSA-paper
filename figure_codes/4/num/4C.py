import matplotlib.pyplot as plt
import numpy as np

# 设置字体
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# 设置CNS风格
plt.style.use('seaborn-v0_8-white')
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 10,
    'axes.linewidth': 1.2,
    'grid.linewidth': 0,
    'patch.linewidth': 1.2,
})

# 数据
conditions = [
    'Official Generation Parameters',
    'TEMPERATURE=0.01',
    'TEMPERATURE=1.5',
    'REPETITION_PENALTY=1.1',
    'TOP_P=0.3',
    'TOP_K=100',
    'USE_SAMPLING=False'
]
scores = [0.4275, 0.4280, 0.4289, 0.4335, 0.4330, 0.4275, 0.4114]

# 创建配色方案
colors = ['#1C4E63', '#2E86AB', '#F18F01', '#73A580', '#6C5B7B', '#355C7D', '#C06C84']

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

# 绘制柱状图 - 使用range(len(conditions))作为x坐标
x_positions = np.arange(len(conditions))
bars = ax.bar(x_positions, scores, color=colors, edgecolor='black',
              linewidth=1.2, alpha=0.85, width=0.65)

# 设置x轴刻度和标签 - 关键修改在这里！
ax.set_xticks(x_positions)
ax.set_xticklabels(conditions, rotation=45, ha='right', va='top',
                   rotation_mode='anchor', fontsize=6)

# 设置Y轴
ax.set_ylim(0.40, 0.44)
ax.set_yticks([0.40, 0.42, 0.44])
ax.set_ylabel('5D3S-QSA Score', fontsize=12, fontweight='bold', labelpad=10)

# 添加数值标签
for i, (bar, score) in enumerate(zip(bars, scores)):
    height = bar.get_height()
    va_position = 'bottom' if height < 0.46 else 'top'
    y_offset = 0.001 if va_position == 'bottom' else -0.001
    ax.text(bar.get_x() + bar.get_width()/2., height + y_offset,
            f'{score:.4f}', ha='center', va=va_position,
            fontsize=7, fontweight='medium')

# 添加基准线
ax.axhline(y=scores[0], color='gray', linewidth=1.0, alpha=0.5,
           linestyle='--', xmin=0.05, xmax=0.95)

# 添加底部的基线
ax.axhline(y=0.40, color='black', linewidth=1.2, alpha=0.7)

# 设置边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

# 调整布局
plt.tight_layout(pad=2.5)
# 显示图形
plt.show()