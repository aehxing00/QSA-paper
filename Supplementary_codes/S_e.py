import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================ 1. 绘图超参数配置 ============================
FONT_SIZE_LABEL = 20      # 轴标签字体大小
FONT_SIZE_TICK = 18      # 刻度字体大小
FONT_SIZE_LEGEND = 17     # 图例字体大小
LINE_WIDTH = 2.0          # 线条宽度
MARKER_SIZE = 7           # 标记点大小
BAR_ALPHA = 0.6           # 柱状图透明度（增加对比度）
BAR_WIDTH = 0.2          # 柱状图宽度
COLOR_QSA = '#D62728'     # QSA 专用红
COLOR_STEM = '#1F77B4'    # STEM 专用蓝

# ============================ 2. 数据准备 ============================
data = {
    'Ratio': [0, 0.5, 1, 1.5, 2, 3, 5],
    'QSA_KL': [-0.00019, 0.1169, 0.549, 1.285, 2.289, 4.888, 8.945],
    'QSA_Sensitivity': [-0.00019, 0.234, 0.432, 0.491, 0.501, 0.866, 0.811],
    'STEM_KL': [-0.0004, 0.074, 0.315, 0.699, 1.274, 2.697, 4.555],
    'STEM_Sensitivity': [-0.0004, 0.149, 0.241, 0.255, 0.287, 0.474, 0.371]
}
df = pd.DataFrame(data)

# ============================ 3. 核心绘图逻辑 ============================
# 设置学术风格
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'svg.fonttype': 'none',
    'axes.unicode_minus': False
})

fig, ax1 = plt.subplots(figsize=(6, 6))

# --- 绘制 KL 散度 (左轴：折线图) ---
lns1 = ax1.plot(df['Ratio'], df['QSA_KL'], color=COLOR_QSA, marker='o', 
                markersize=MARKER_SIZE, linewidth=LINE_WIDTH, label='$\Delta$ KL (QSA)')
lns2 = ax1.plot(df['Ratio'], df['STEM_KL'], color=COLOR_STEM, marker='s', 
                markersize=MARKER_SIZE, linewidth=LINE_WIDTH, linestyle='--', label='$\Delta$ KL (STEM)')

ax1.set_xlabel('Ablation Intensity (Ratio)', fontsize=FONT_SIZE_LABEL, fontweight='bold')
ax1.set_ylabel('Representation Shift (KL)', fontsize=FONT_SIZE_LABEL, fontweight='bold')
ax1.tick_params(axis='both', labelsize=FONT_SIZE_TICK)
ax1.set_ylim(-0.5, 10)
ax1.grid(True, linestyle=':', alpha=0.5)

# --- 绘制 敏感度比值 (右轴：高对比度柱状图) ---
ax2 = ax1.twinx()
# QSA 柱状图
ax2.bar(df['Ratio'] - BAR_WIDTH/2, df['QSA_Sensitivity'], width=BAR_WIDTH, 
        color=COLOR_QSA, alpha=BAR_ALPHA, edgecolor='black', linewidth=0.5, label='Sens. (QSA)')
# STEM 柱状图
ax2.bar(df['Ratio'] + BAR_WIDTH/2, df['STEM_Sensitivity'], width=BAR_WIDTH, 
        color=COLOR_STEM, alpha=BAR_ALPHA, edgecolor='black', linewidth=0.5, label='Sens. (STEM)')

ax2.set_ylabel('Sensitivity [dKL/dR]', fontsize=FONT_SIZE_LABEL, fontweight='bold', rotation=270, labelpad=20)
ax2.tick_params(axis='y', labelsize=FONT_SIZE_TICK)
ax2.set_ylim(0, 1.2)

# --- 图例与边框美化 ---
# 合并图例并放置
lines, labels = ax1.get_legend_handles_labels()
bars, bar_labels = ax2.get_legend_handles_labels()
ax1.legend(lines + bars, labels + bar_labels, loc='upper left', frameon=False, 
           fontsize=FONT_SIZE_LEGEND, ncol=1)

# 移除上方边框，保留右侧轴
sns.despine(top=True, right=False)

# ============================ 4. 导出 SVG ============================
plt.tight_layout()
plt.savefig("Causal_Ablation_Nature_Style.svg", format='svg', bbox_inches='tight')
plt.show()

print("✅ 超参数化 SVG 矢量图已生成。")