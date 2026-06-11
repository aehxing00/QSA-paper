import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import warnings

warnings.filterwarnings('ignore')

# ==================== HYPERPARAMETER SETTINGS (FOR PDF EXPORT) ====================
MIN_CORRELATION_TO_PLOT = 0.95       # 仅显示 |r| > 0.95 的强关联
NODE_RADIUS_SCALE = 0.6              # 节点半径缩放
CIRCLE_RADIUS = 4                    # 布局圆半径
DIMENSION_LABEL_SIZE = 40            # 圆圈内标签字号
BASE_LINE_WIDTH = 10.0               # 连线基础宽度 (加粗以匹配图片)
MIN_ALPHA = 0.3                      # 连线最小透明度
MAX_ALPHA = 0.7                      # 连线最大透明度

# 全局字体设置 (确保矢量 PDF 中的字体是 Arial)
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['pdf.fonttype'] = 42    # 关键：导出可编辑文字
plt.rcParams['ps.fonttype'] = 42
# =================================================================================

# 1. 读取数据
file_path = 'a1_alllll.xlsx'
df = pd.read_excel(file_path)

def parse_question_id(q_id):
    if isinstance(q_id, str):
        return q_id[0], q_id[1]
    return None, None

df['Major_Category'] = df['Question_ID'].apply(lambda x: parse_question_id(x)[0])
df['Minor_Category'] = df['Question_ID'].apply(lambda x: parse_question_id(x)[1])

# 2. 准备 15 个维度的分数 (1A-5C)
expected_dimensions = [f"{m}{n}" for m in '12345' for n in 'ABC']
dimension_names = []
dimensions = []
model_columns = [col for col in df.columns if col not in ['Question_ID', 'Major_Category', 'Minor_Category']]

for dim_name in expected_dimensions:
    m, n = dim_name[0], dim_name[1]
    mask = (df['Major_Category'] == m) & (df['Minor_Category'] == n)
    data = df[mask]
    if len(data) > 0:
        dimension_names.append(dim_name)
        dimensions.append([data[model].mean() for model in model_columns])

# 3. 计算相关性矩阵
dimension_array = np.array(dimensions)
n_dimensions = len(dimension_names)
spearman_corr = np.ones((n_dimensions, n_dimensions))

for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        corr, _ = spearmanr(dimension_array[i], dimension_array[j])
        spearman_corr[i, j] = spearman_corr[j, i] = corr

# 4. 绘图准备
fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')

# 计算圆周位置 (从 0 度开始均匀分布)
angles = np.linspace(0, 2 * np.pi, n_dimensions, endpoint=False)
pos = {name: (CIRCLE_RADIUS * np.cos(a), CIRCLE_RADIUS * np.sin(a)) 
       for name, a in zip(dimension_names, angles)}

# 精确匹配图片中的莫兰迪配色
major_colors = {
    '1': '#FF8A8A',  # 浅红色 (Ontological)
    '2': '#7AD6D0',  # 浅青色 (Depth)
    '3': '#6AC4D9',  # 浅蓝色 (Recursive)
    '4': '#A8D6C0',  # 浅绿色 (Social)
    '5': '#FFF2B2',  # 浅黄色 (Identity)
}

# 5. 绘制连线 (红褐色，饱和度/透明度随相关性变化)
all_links = []
for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        r = spearman_corr[i, j]
        if abs(r) > MIN_CORRELATION_TO_PLOT:
            all_links.append((dimension_names[i], dimension_names[j], r))

# 按相关性从小到大排，确保最强的线在最上面
all_links.sort(key=lambda x: abs(x[2]))

for d1, d2, r in all_links:
    p1, p2 = pos[d1], pos[d2]
    # 计算权重系数 (0.0 到 1.0)
    weight = (abs(r) - MIN_CORRELATION_TO_PLOT) / (1.0 - MIN_CORRELATION_TO_PLOT)
    alpha = MIN_ALPHA + weight * (MAX_ALPHA - MIN_ALPHA)
    
    # 绘制连线
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
            color='#C95D5D', # 图片中的红褐色
            alpha=alpha,
            linewidth=BASE_LINE_WIDTH, 
            solid_capstyle='round',
            zorder=1)

# 6. 绘制节点
for dim in dimension_names:
    x, y = pos[dim]
    color = major_colors.get(dim[0], '#CCCCCC')
    
    # 绘制圆圈 (带黑色细边框)
    circle = plt.Circle((x, y), NODE_RADIUS_SCALE, 
                        facecolor=color, 
                        edgecolor='black', 
                        linewidth=2.5, 
                        zorder=2)
    ax.add_patch(circle)
    
    # 标注文本 (Arial Black 风格)
    ax.text(x, y, dim, 
            fontsize=DIMENSION_LABEL_SIZE, 
            fontweight='bold', # 对应图片的极粗字体
            ha='center', va='center', 
            color='black',
            zorder=3)

# 7. 格式化输出
ax.set_aspect('equal')
ax.axis('off')
limit = CIRCLE_RADIUS * 1.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# 8. 保存为 PDF 矢量图和预览 PNG
output_pdf = 'correlation_graph.pdf'
plt.savefig(output_pdf, format='pdf', bbox_inches='tight', pad_inches=0)
plt.savefig('correlation_graph.png', format='png', dpi=300, bbox_inches='tight', pad_inches=0)

print(f"矢量图已输出至: {output_pdf}")
plt.show()