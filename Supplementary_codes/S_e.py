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
COLOR_Codes = '#1F77B4'    # Codes 专用蓝

# ============================ 2. 数据准备 ============================
data = {
    'Ratio': [0, 0.5, 1, 1.5, 2, 3, 5],
    'QSA_KL': [-5.98824E-05, 0.296416321, 1.273739624, 2.596323242, 3.981962891, 6.2909375, 9.017460938],
    'QSA_Sensitivity': [-5.98824E-05, 0.592952406, 0.977323303, 0.881722412, 0.692819824, 0.769658203, 0.545304688],
    'Codes_KL': [-7.42745E-05, 0.056425171, 0.207070313, 0.505664063, 1.155332031, 3.185859375, 2.80671875],
    'Codes_Sensitivity': [-7.42745E-05, 0.112998891, 0.150645142, 0.1990625, 0.324833984, 0.676842448, -0.075828125]
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
lns2 = ax1.plot(df['Ratio'], df['Codes_KL'], color=COLOR_Codes, marker='s',
                markersize=MARKER_SIZE, linewidth=LINE_WIDTH, linestyle='--', label='$\Delta$ KL (Codes)')

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
# Codes 柱状图
ax2.bar(df['Ratio'] + BAR_WIDTH/2, df['Codes_Sensitivity'], width=BAR_WIDTH,
        color=COLOR_Codes, alpha=BAR_ALPHA, edgecolor='black', linewidth=0.5, label='Sens. (Codes)')

ax2.set_ylabel('Sensitivity [dKL/dR]', fontsize=FONT_SIZE_LABEL, fontweight='bold', rotation=270, labelpad=20)
ax2.tick_params(axis='y', labelsize=FONT_SIZE_TICK)
ax2.set_ylim(0, 1.2)

# --- 图例与边框美化 ---
# 合并图例并放置
lines, labels = ax1.get_legend_handles_labels()
bars, bar_labels = ax2.get_legend_handles_labels()
ax1.legend(lines + bars, labels + bar_labels, loc='upper left', bbox_to_anchor=(0, 1.3), frameon=False,
           fontsize=FONT_SIZE_LEGEND, ncol=1)

# 移除上方边框，保留右侧轴
sns.despine(top=True, right=False)

# ============================ 4. 导出 SVG ============================
plt.tight_layout()
plt.savefig("Causal_Ablation_Nature_Style.svg", format='svg', bbox_inches='tight')
plt.show()

print("✅ 超参数化 SVG 矢量图已生成。")