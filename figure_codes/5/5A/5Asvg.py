import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# ==========================================
# 1. 全局样式与 SVG 矢量化设置
# ==========================================
matplotlib.rcParams['font.family'] = 'Arial'
# 关键：导出 SVG 时文字不转路径，保持可编辑性
matplotlib.rcParams['svg.fonttype'] = 'none'

# --- 视觉超参数 ---
FIG_SIZE        = (10, 6)      # 比例更接近原图
SIZE_Y_LABEL    = 25           # Score 标题大小
SIZE_X_TICKS    = 19           # Benchmark 名称大小
SIZE_Y_TICKS    = 18           # 数值大小
SIZE_LEGEND     = 19           # 图例文字大小
SPINE_WIDTH     = 3.5          # 坐标轴粗细
TICK_WIDTH      = 3.5          # 刻度线粗细
BAR_EDGE_WIDTH  = 2.5          # 柱子边框粗细

# --- 颜色与顺序 ---
LEGEND_ORDER    = ['Base Model', 'Fine-tuned Model', 'DeepSeek-V3.2']
# 精确匹配原图颜色：深青色, 砖红色, 灰色
CUSTOM_COLORS   = ["#2A5D67", "#A56262", "#848888"] 
LEGEND_POS      = (0.52, 1.12)

# ==========================================
# 2. 数据处理
# ==========================================
file_path = 'b3.xlsx'
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    # 模拟数据
    data = {
        'Benchmark': ['BigCodeBench', 'MATH', 'TheoremQA', 'MMLU_Pro', 'GPQA', 'SuperGPQA', 'BBH', 'ToMATO', 'CPED', 'ARC_Challenge', 'PIQA'],
        'Base Model': [18, 20, 19, 10, 11, 18, 86, 7, 16, 84, 80],
        'Fine-tuned Model': [26, 25, 22, 40, 17, 22, 86, 13, 22, 78, 76],
        'DeepSeek-V3.2': [34, 65, 18, 34, 10, 27, 67, 4, 20, 53, 60]
    }
    df = pd.DataFrame(data)

df_melted = df.melt(id_vars='Benchmark', var_name='Model', value_name='Score')

# ==========================================
# 3. 绘图核心逻辑
# ==========================================
fig, ax = plt.subplots(figsize=FIG_SIZE, facecolor='white')

# 绘制柱状图
sns.barplot(
    data=df_melted, x='Benchmark', y='Score', hue='Model',
    hue_order=LEGEND_ORDER,
    palette=CUSTOM_COLORS,
    ax=ax,
    edgecolor='#000000', # 强制纯黑边框
    linewidth=BAR_EDGE_WIDTH,
    alpha=1.0,
    zorder=3
)

# --- 坐标轴细节调整 (强制纯黑处理) ---
ax.set_ylabel("Score", fontsize=SIZE_Y_LABEL, fontweight='bold', labelpad=10, color='#000000')
ax.set_xlabel("", fontsize=1)

# 加粗坐标轴线并设为纯黑
ax.spines['left'].set_linewidth(SPINE_WIDTH)
ax.spines['left'].set_color('#000000')
ax.spines['bottom'].set_linewidth(SPINE_WIDTH)
ax.spines['bottom'].set_color('#000000')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 加粗刻度线颜色
ax.tick_params(axis='both', which='major', labelsize=SIZE_Y_TICKS, 
                width=TICK_WIDTH, length=10, direction='out', colors='#000000')
ax.tick_params(axis='x', labelsize=SIZE_X_TICKS)

# X轴标签旋转
plt.xticks(rotation=45, ha='right', rotation_mode='anchor', fontweight='bold', color='#000000')

# 图例设置 (无框、横向、文字加粗)
ax.legend(
    loc='upper center',
    bbox_to_anchor=LEGEND_POS,
    ncol=3,
    frameon=False,
    fontsize=SIZE_LEGEND,
    columnspacing=1.5,
    handletextpad=0.5,
    prop={'weight': 'bold', 'size': SIZE_LEGEND}
)

# 网格线 (复刻原图灰色虚线)
ax.yaxis.grid(True, linestyle=(0, (5, 5)), color='#D1D1D1', linewidth=2.0, zorder=0)
ax.set_axisbelow(True)

# 限制Y轴并强制刻度为黑
ax.set_ylim(0, 100)
ax.set_yticks([0, 20, 40, 60, 80])
ax.set_yticklabels(['0', '20', '40', '60', '80'], 
                   fontweight='bold', fontsize=SIZE_Y_TICKS, color='#000000')

# ==========================================
# 4. 输出 SVG 矢量图
# ==========================================
plt.tight_layout()
plt.subplots_adjust(top=0.88)

output_filename = "Benchmark_Comparison_HighQual.svg"
plt.savefig(output_filename, format='svg', bbox_inches='tight')
# 保存预览图
plt.savefig("Benchmark_Comparison_Preview.png", dpi=300, bbox_inches='tight')

plt.show()

print(f"✅ 成功导出 SVG 矢量图: {output_filename}")