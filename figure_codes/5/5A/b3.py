import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. 超参数设置 (这里控制一切)
# ==========================================

# 图片整体尺寸
FIG_SIZE = (12, 6)
FONT_FAMILY = 'Arial'

# --- 字体大小 ---
SIZE_Y_LABEL   = 7   # Y轴标题大小
SIZE_X_TICKS   = 5   # X轴柱子名称大小
SIZE_Y_TICKS   = 6   # Y轴数值大小
SIZE_LEGEND    = 4   # 图例文字大小

# --- 位置调整 (核心修改) ---
Y_LABEL_PAD    = 3    # <--- 修改这里：数值越小，Score越靠近Y轴（向右移）；数值越大越靠左。

# --- 颜色与图例顺序 ---
# 根据新的数据格式调整
LEGEND_ORDER = [
    'Base Model', 'Fine-tuned Model', 'DeepSeek-V3.2'
]
CUSTOM_COLORS = ["#15718A", "#C04949", "#8A9191"]  # 灰色, 红色, 绿色
LEGEND_POS     = (0.5, 1.05)

# ==========================================
# 2. 数据处理与绘图
# ==========================================
file_path = 'b3.xlsx'
df = pd.read_excel(file_path)

# 检查数据格式并处理
print("原始数据列名:", df.columns.tolist())
print("数据前几行:")
print(df.head())

# 将数据从宽格式转换为长格式
df_melted = df.melt(id_vars='Benchmark', var_name='Model', value_name='Score')

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [FONT_FAMILY, 'DejaVu Sans']

fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=300)

sns.barplot(
    data=df_melted, x='Benchmark', y='Score', hue='Model',
    hue_order=LEGEND_ORDER,
    palette=CUSTOM_COLORS,
    ax=ax,
    edgecolor='black', linewidth=0.8, alpha=0.9, zorder=3
)

# ==========================================
# 3. 细节调整
# ==========================================

# 应用 Y_LABEL_PAD 参数
ax.set_ylabel("Score", fontsize=SIZE_Y_LABEL, fontweight='bold', labelpad=Y_LABEL_PAD)
ax.set_xlabel("", fontsize=1)

# 调整刻度标签
ax.tick_params(axis='x', labelsize=SIZE_X_TICKS, length=5, width=1)
ax.tick_params(axis='y', labelsize=SIZE_Y_TICKS, length=5, width=1)
plt.xticks(rotation=45, ha='right', rotation_mode='anchor')

# 图例
ax.legend(
    title=None,
    loc='upper center',
    bbox_to_anchor=LEGEND_POS,
    ncol=3,  # 改为3列以容纳3个模型
    frameon=False,
    fontsize=SIZE_LEGEND,
    columnspacing=2.0,
    labelspacing=0.5
)

# 边框与网格
ax.yaxis.grid(True, linestyle='--', color='grey', alpha=0.3, zorder=0)
ax.xaxis.grid(False)
sns.despine(ax=ax, top=True, right=True)
ax.spines['left'].set_linewidth(1)
ax.spines['bottom'].set_linewidth(1)

# 调整Y轴范围以适应数据
y_min = df_melted['Score'].min()
y_max = df_melted['Score'].max()
ax.set_ylim([min(0, y_min * 0.9), y_max * 1.15])

plt.tight_layout()
plt.subplots_adjust(top=0.85)

plt.show()

# 打印数据处理后的结果以供验证
print("\n处理后的数据格式:")
print(df_melted.head())
print(f"\n共 {len(df_melted)} 行数据")
print(f"基准数量: {len(df['Benchmark'].unique())}")
print(f"模型数量: {len(df_melted['Model'].unique())}")