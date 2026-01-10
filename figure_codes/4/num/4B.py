import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# 设置中文字体，解决冒号乱码问题
try:
    # Windows系统中文字体
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 黑体
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['axes.unicode_minus'] = False
except:
    # 备选方案：使用系统默认字体
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['axes.unicode_minus'] = False

# 设置CNS期刊风格
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'figure.autolayout': False,
    'axes.linewidth': 0.8,
    'grid.linewidth': 0.5,
    'grid.alpha': 0.3,
    'lines.linewidth': 1.5,
    'lines.markersize': 8,
    'axes.grid': True,
    'grid.linestyle': '--',
})

# 数据
x_labels = [
    'Population=25', 'Population=50', 'Population=75', 'Population=150',
    'Meta-Lr:0.1-0.5', 'Meta-Lr:0.1-0.4', 'Meta-Lr:0.1-0.3',
    'Lr=1e-5', 'Lr=2e-5', 'Lr=5e-5',
    'LoRA_r=8', 'LoRA_r=16', 'LoRA_r=32'
]

values = [
    0.2854, 0.4134, 0.3538, 0.3513,
    0.3005, 0.3512, 0.3513,
    0.1834, 0.3513, 0.3577,
    0.1765, 0.3513, 0.3304
]

# 定义4个段落
segments = [
    {'name': 'Population', 'indices': [0, 1, 2, 3], 'values': values[0:4], 'color': '#1f77b4'},
    {'name': 'Meta-Lr', 'indices': [4, 5, 6], 'values': values[4:7], 'color': '#ff7f0e'},
    {'name': 'Learning Rate', 'indices': [7, 8, 9], 'values': values[7:10], 'color': '#2ca02c'},
    {'name': 'LoRA Rank', 'indices': [10, 11, 12], 'values': values[10:13], 'color': '#d62728'}
]

# 创建图形
fig, ax = plt.subplots(figsize=(11, 5.5))

# 用于存储需要突出显示的x轴标签索引
highlight_indices = []

# 绘制每个段落（段落之间不连线）
for seg_idx, segment in enumerate(segments):
    indices = segment['indices']
    seg_values = segment['values']
    color = segment['color']

    # 特别处理Learning Rate段落：选择Lr=2e5（索引8）而不是最大值0.3577（索引9）
    if seg_idx == 2:  # Learning Rate段落的索引为2
        # 手动指定Lr=2e5为最高值（索引8）
        max_idx = 8
        max_val = values[8]
    else:
        # 其他段落正常计算最高值
        max_val = max(seg_values)
        max_idx = indices[seg_values.index(max_val)]

    # 将最高值的索引添加到突出显示列表中
    highlight_indices.append(max_idx)

    # 绘制当前段落的折线（只在段落内部连线）
    ax.plot(indices, seg_values,
            color=color, marker='o', linewidth=1.5,
            markersize=8, markerfacecolor='white',
            markeredgewidth=1.5, markeredgecolor=color,
            zorder=3)

    # 高亮显示每个段落内的最高值
    ax.plot(max_idx, max_val,
            marker='o', markersize=12, color=color,
            markeredgecolor='black', markeredgewidth=2,
            zorder=4)

    # 标注最高值的数值
    ax.annotate(f'{max_val:.3f}',
                xy=(max_idx, max_val),
                xytext=(0, 15),  # 向上偏移15个点
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold',
                color=color,
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor='white',
                         edgecolor=color,
                         alpha=0.9),
                zorder=5)

# 设置y轴
ax.set_ylim(0.1, 0.5)
ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
ax.set_ylabel('5D3S-QSA Score', fontsize=12, fontweight='bold')

# 设置x轴
ax.set_xlim(-0.5, len(x_labels) - 0.5)
ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, rotation=45, ha='right')

# 设置x轴标签样式：用颜色突出显示重要标签
for i, tick in enumerate(ax.get_xticklabels()):
    if i in highlight_indices:
        # 突出显示的标签：黑色加粗，带浅色背景
        tick.set_color('black')
        tick.set_fontweight('bold')
        tick.set_bbox(dict(facecolor='lightyellow', alpha=0.5, edgecolor='gold',
                          boxstyle='round,pad=0.2', linewidth=0.5))
    else:
        # 普通标签：灰色
        tick.set_color('gray')
        tick.set_fontweight('normal')
        # 移除普通标签的背景
        tick.set_bbox(None)

# 添加段落间的分隔线（更明显的分隔）
break_positions = [3.5, 6.5, 9.5]  # 段落之间的位置
for bp in break_positions:
    ax.axvline(x=bp, color='gray', linestyle=':', linewidth=1.2, alpha=0.7, zorder=1)

# 添加段落标题背景 - 字体缩小一号（从10改为9）
for i, seg in enumerate(segments):
    if i == 0:
        title_x = np.mean([0, 3])  # 第一个段落的中点
    elif i == 1:
        title_x = np.mean([4, 6])  # 第二个段落的中点
    elif i == 2:
        title_x = np.mean([7, 9])  # 第三个段落的中点
    else:
        title_x = np.mean([10, 12])  # 第四个段落的中点

    # 添加段落标题，字体大小改为9
    ax.text(title_x, 0.52, seg['name'],
            ha='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3',
                     facecolor='lightgray',
                     edgecolor='gray',
                     alpha=0.3),
            zorder=2)

# 添加基线参考线（0.3513）- 只保留线条，不添加文字标注
baseline_value = 0.3513
ax.axhline(y=baseline_value, color='gray', linestyle='--',
           linewidth=0.8, alpha=0.5, zorder=1)

# 添加网格
ax.grid(True, linestyle='--', alpha=0.3, zorder=0)

# 设置边框
for spine in ax.spines.values():
    spine.set_linewidth(0.8)

# 调整布局，给x轴标签更多空间
plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.95])

plt.show()