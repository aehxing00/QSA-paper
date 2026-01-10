import matplotlib.pyplot as plt
import numpy as np

# ==================== 专业绘图配置 ====================
# 设置全局字体为 Arial 并加粗
plt.rcParams['font.family'] = 'Arial'
# 设置 PDF 文字可编辑 (Type 42)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 精确参考图片的比例和视觉参数
FIG_WIDTH = 5
FIG_HEIGHT = 5
FONT_SIZE_LABEL = 24  # Y轴大标题
FONT_SIZE_TICK = 20   # 轴刻度
FONT_SIZE_VALUE = 22  # 柱上数值
LINE_WIDTH = 3        # 轴线和刻度线粗细

# 数据准备
categories = ['Mean Score', 'Base Model', 'Fine-tuned Model']
values = [0.087, 0.065, 0.369]
colors = ['#2E86AB', '#A23B72', '#F18F01'] # 蓝、紫、橙

# ==================== 开始绘图 ====================
fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=300)

# 绘制柱状图 (注意原图中柱子边框为纯白且较粗)
bars = ax.bar(categories, values, color=colors, width=0.6,
              edgecolor='white', linewidth=3, alpha=1.0)

# 在柱子顶部标注数值 (精确复刻 4f.png 样式：无背景框，位置紧贴)
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
            f'{value:.3f}',
            ha='center', va='bottom',
            fontsize=FONT_SIZE_VALUE,
            fontweight='bold',
            color='black')

# 设置y轴
ax.set_ylim(0, 0.42)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4])
ax.set_yticklabels(['0.0', '0.1', '0.2', '0.3', '0.4'],
                   fontsize=FONT_SIZE_TICK, fontweight='bold')

# 设置Y轴标题 (精确复刻原图中的拼写 "Scroe" 及其垂直加粗样式)
ax.set_ylabel('5D3S-QSA Score',
              fontsize=FONT_SIZE_LABEL,
              fontweight='bold',
              labelpad=20)

# 设置x轴标签 (45度倾斜，对齐方式)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, rotation=45, ha='right',
                   fontsize=FONT_SIZE_TICK, fontweight='bold')

# ==================== 坐标轴精细化美化 ====================
# 移除上方和右侧边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 加粗左侧和下方轴线
ax.spines['left'].set_linewidth(LINE_WIDTH)
ax.spines['bottom'].set_linewidth(LINE_WIDTH)

# 调整刻度线 (厚度与轴线一致)
ax.tick_params(axis='y', width=LINE_WIDTH, length=8)
ax.tick_params(axis='x', width=LINE_WIDTH, length=0) # X轴通常不显示刻度点

# 移除网格线 (根据 4f.png 原始样式，纯白底色)
ax.grid(False)

# 强制布局调整，防止标签切断
plt.tight_layout()

# ==================== 矢量化导出 ====================
# 保存为高清 PDF (投稿专用)
plt.savefig('5D3S_QSA_Score_Barplot.pdf', format='pdf', bbox_inches='tight')
# 保存为高清 PNG (预览专用)
plt.savefig('5D3S_QSA_Score_Barplot.png', format='png', dpi=300, bbox_inches='tight')

plt.show()