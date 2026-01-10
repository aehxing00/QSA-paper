import matplotlib.pyplot as plt
import numpy as np

# ==================== 专业绘图配置 ====================
# 设置全局字体为 Arial 并加粗
plt.rcParams['font.family'] = 'Arial'
# 关键：设置 SVG 文字不转路径，保持可编辑性
plt.rcParams['svg.fonttype'] = 'none'

# 精确参考图片的比例和视觉参数
FIG_WIDTH = 4
FIG_HEIGHT = 5
FONT_SIZE_LABEL = 20  # Y轴大标题
FONT_SIZE_TICK = 15   # 轴刻度
LINE_WIDTH = 3        # 轴线和刻度线粗细

# 数据准备
categories = ['Mean Score', 'Base Model', 'Fine-tuned Model','Identity-Shifting Probing']
values = [0.087, 0.065, 0.369, 0.4433]
colors = ['#2E86AB', '#A23B72', '#F18F01', "#F10101"]

# ==================== 开始绘图 ====================
fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=300, facecolor='white')

# 绘制柱状图 (柱子边框为纯白且较粗)
bars = ax.bar(categories, values, color=colors, width=0.6,
              edgecolor='white', linewidth=3, alpha=1.0, zorder=3)

# 【已取消】数值标注部分 (ax.text 已移除)

# 设置y轴
ax.set_ylim(0, 0.42)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4])
# 强制 Y 轴刻度为纯黑色加粗
ax.set_yticklabels(['0.0', '0.1', '0.2', '0.3', '0.4'],
                   fontsize=FONT_SIZE_TICK, fontweight='bold', color='#000000')

# 设置Y轴标题
ax.set_ylabel('5D3S-QSA Score',
              fontsize=FONT_SIZE_LABEL,
              fontweight='bold',
              color='#000000',
              labelpad=20)

# 设置x轴标签 (45度倾斜，对齐方式)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, rotation=45, ha='right',
                   fontsize=FONT_SIZE_TICK, fontweight='normal', color='#000000')

# ==================== 坐标轴精细化美化 ====================
# 移除上方和右侧边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 加粗左侧和下方轴线并设为纯黑
for spine in ['left', 'bottom']:
    ax.spines[spine].set_linewidth(LINE_WIDTH)
    ax.spines[spine].set_color('#000000')

# 调整刻度线 (颜色设为纯黑)
ax.tick_params(axis='y', width=LINE_WIDTH, length=8, colors='#000000')
ax.tick_params(axis='x', width=LINE_WIDTH, length=0) # X轴不显示刻度点

# 确保无网格线
ax.grid(False)

# 强制布局调整，防止标签切断
plt.tight_layout()

# ==================== 矢量化导出 ====================
# 保存为 SVG (可编辑矢量图)
svg_path = '5D3S_QSA_Score_Barplot.svg'
plt.savefig(svg_path, format='svg', bbox_inches='tight')

# 保存为高清 PNG (预览专用)
plt.savefig('5D3S_QSA_Score_Barplot_Preview.png', format='png', dpi=300, bbox_inches='tight')

print(f"✅ 成功导出矢量图: {svg_path}")
plt.show()