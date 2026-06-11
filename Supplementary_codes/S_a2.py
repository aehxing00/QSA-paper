import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 读取数据
# 假设第一列为行索引，加载 Excel 文件 p2.xlsx
df = pd.read_excel('2E2.xlsx', index_col=0)

# 2. 设置 CNS 杂志风格（简洁、无多余网格、大字体）
plt.rcParams.update({
    'font.size': 14,              # 全局字体大小
    'axes.linewidth': 1.2,        # 坐标轴线宽度
    'xtick.top': True,            # X 轴刻度显示在上方
    'xtick.bottom': False,        # 关闭下方刻度
    'ytick.left': True,           # Y 轴刻度显示在左侧
    'ytick.right': False,         # 关闭右侧刻度
    'axes.grid': False,           # 关闭网格
    'figure.facecolor': 'white',  # 白色背景
    'axes.facecolor': 'white'     # 坐标区白色背景
})

# 3. 绘制热图
fig, ax = plt.subplots(figsize=(8, 6))

# 将 X 轴刻度移动到上方
ax.xaxis.set_ticks_position('top')

# 使用 seaborn 绘制带数值标注的热图
sns.heatmap(
    df,
    ax=ax,
    cmap='vlag',               # Divergent 色带，可按需更换
    linewidths=1,            # 每个单元格边界宽度
    linecolor='white',          # 边界颜色
    annot=True,                # 在色块中显示数值
    fmt='.2f',                 # 数值格式，可根据需要调整
    annot_kws={'size': 12},    # 数值字体大小
    cbar_kws={'shrink': 0.6}   # 颜色条缩放
)

# 4. 调整布局 & 标注
ax.set_xlabel('')  # 如不需要显示 xlabel，可留空
ax.set_ylabel('')  # 如不需要显示 ylabel，可留空
plt.xticks(rotation=45, ha='left')  # X 轴标签旋转，靠左对齐
plt.yticks(rotation=0)
plt.tight_layout()

# 5. 显示图形
plt.show()
