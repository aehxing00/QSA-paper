import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import warnings

warnings.filterwarnings('ignore')

# ==================== HYPERPARAMETER SETTINGS (FOR SVG EXPORT) ====================
MIN_CORRELATION_TO_PLOT = 0.95       # 仅显示 |r| > 0.95 的强关联
NODE_RADIUS_SCALE = 0.6              # 节点半径缩放
CIRCLE_RADIUS = 4                    # 布局圆半径
DIMENSION_LABEL_SIZE = 40            # 圆圈内标签字号
BASE_LINE_WIDTH = 10.0               # 连线基础宽度
MIN_ALPHA = 0.3                      # 连线最小透明度
MAX_ALPHA = 0.7                      # 连线最大透明度

# 全局字体设置
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
# 关键：设置 SVG 字体不转为路径，保持文字可编辑
plt.rcParams['svg.fonttype'] = 'none' 
# =================================================================================

# 1. 读取数据
file_path = 'a1_alllll.xlsx'
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"错误: 未找到文件 {file_path}")
    # 这里仅为演示，如果文件不存在则创建一个假数据以便展示代码结构
    df = pd.DataFrame({'Question_ID': [f"{m}{n}01" for m in '12345' for n in 'ABC']})

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

# 计算圆周位置
angles = np.linspace(0, 2 * np.pi, n_dimensions, endpoint=False)
pos = {name: (CIRCLE_RADIUS * np.cos(a), CIRCLE_RADIUS * np.sin(a)) 
       for name, a in zip(dimension_names, angles)}

# 莫兰迪配色
major_colors = {
    '1': '#FF8A8A',  # 浅红色
    '2': '#7AD6D0',  # 浅青色
    '3': '#6AC4D9',  # 浅蓝色
    '4': '#A8D6C0',  # 浅绿色
    '5': '#FFF2B2',  # 浅黄色
}

# 5. 绘制连线
all_links = []
for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        r = spearman_corr[i, j]
        if abs(r) > MIN_CORRELATION_TO_PLOT:
            all_links.append((dimension_names[i], dimension_names[j], r))

all_links.sort(key=lambda x: abs(x[2]))

for d1, d2, r in all_links:
    p1, p2 = pos[d1], pos[d2]
    weight = (abs(r) - MIN_CORRELATION_TO_PLOT) / (1.0 - MIN_CORRELATION_TO_PLOT)
    alpha = MIN_ALPHA + weight * (MAX_ALPHA - MIN_ALPHA)
    
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
            color='#C95D5D', # 红褐色
            alpha=alpha,
            linewidth=BASE_LINE_WIDTH, 
            solid_capstyle='round',
            zorder=1)

# 6. 绘制节点
for dim in dimension_names:
    x, y = pos[dim]
    color = major_colors.get(dim[0], '#CCCCCC')
    
    # 绘制圆圈 (强制纯黑边框)
    circle = plt.Circle((x, y), NODE_RADIUS_SCALE, 
                        facecolor=color, 
                        edgecolor='#000000', 
                        linewidth=2.5, 
                        zorder=2)
    ax.add_patch(circle)
    
    # 标注文本 (纯黑加粗)
    ax.text(x, y, dim, 
            fontsize=DIMENSION_LABEL_SIZE, 
            fontweight='bold', 
            ha='center', va='center', 
            color='#000000',
            zorder=3)

# 7. 格式化输出
ax.set_aspect('equal')
ax.axis('off')
limit = CIRCLE_RADIUS * 1.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# 8. 保存为 SVG 矢量图
output_svg = 'correlation_graph_final.svg'
plt.savefig(output_svg, format='svg', bbox_inches='tight', pad_inches=0)

# 同时保存 PNG 用于快速查看
plt.savefig('correlation_graph_preview.png', format='png', dpi=300, bbox_inches='tight', pad_inches=0)

print(f"✅ 成功! 矢量图已保存至: {output_svg}")
plt.show()