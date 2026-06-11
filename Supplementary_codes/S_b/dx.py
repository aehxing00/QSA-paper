import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import warnings

warnings.filterwarnings('ignore')

# ==================== 超参数设置 ====================
TOP_N_CORRELATIONS_TO_LABEL = 30      # 只标注相关系数绝对值排名前N的相关性连线
MIN_CORRELATION_TO_PLOT = 0.95         # 只绘制相关系数绝对值大于此值的连线
MIN_CORRELATION_TO_LABEL = 0.95        # 只有相关系数绝对值大于此值才可能被标注
NODE_RADIUS_SCALE = 0.6              # 节点圆圈半径缩放因子
CIRCLE_RADIUS = 6                    # 布局圆环半径
DIMENSION_LABEL_SIZE = 18            # 圆形内维度标注的字号
CORRELATION_LABEL_SIZE = 16           # 相关系数字号
# ===================================================

print(f"超参数设置:")
print(f"  标注前 {TOP_N_CORRELATIONS_TO_LABEL} 个最强相关性")
print(f"  只绘制 |r| > {MIN_CORRELATION_TO_PLOT} 的连线")
print(f"  只标注 |r| > {MIN_CORRELATION_TO_LABEL} 的连线")
print(f"  维度标注字号: {DIMENSION_LABEL_SIZE}")
print(f"  相关系数字号: {CORRELATION_LABEL_SIZE}")

# 1. 读取数据
file_path = 'a1_alllll.xlsx'
df = pd.read_excel(file_path)

print("\n正在处理数据...")
print(f"总题目数量: {len(df)}")
print(f"模型数量: {len(df.columns) - 1}")

# 2. 解析题目ID，获取大类和小类信息
def parse_question_id(q_id):
    """解析题目ID，返回(大类, 小类)"""
    if isinstance(q_id, str):
        major_category = q_id[0]
        minor_category = q_id[1]
        return major_category, minor_category
    return None, None

# 添加类别列
df['Major_Category'] = df['Question_ID'].apply(lambda x: parse_question_id(x)[0])
df['Minor_Category'] = df['Question_ID'].apply(lambda x: parse_question_id(x)[1])

# 3. 将题目分组为15个维度（5个大类 × 3个小类）
model_columns = [col for col in df.columns if col not in ['Question_ID', 'Major_Category', 'Minor_Category']]

# 假设的维度顺序：1A, 1B, 1C, 2A, 2B, 2C, 3A, 3B, 3C, 4A, 4B, 4C, 5A, 5B, 5C
expected_dimensions = []
for major in ['1', '2', '3', '4', '5']:
    for minor in ['A', 'B', 'C']:
        expected_dimensions.append(f"{major}{minor}")

dimensions = []
dimension_names = []

for dim_name in expected_dimensions:
    major, minor = dim_name[0], dim_name[1]
    mask = (df['Major_Category'] == major) & (df['Minor_Category'] == minor)
    dimension_questions = df[mask]
    
    if len(dimension_questions) > 0:
        dimension_names.append(dim_name)
        # 计算该维度下所有题目的平均得分
        dimension_scores = [dimension_questions[model].mean() for model in model_columns]
        dimensions.append(dimension_scores)

print(f"\n总共创建了 {len(dimensions)} 个维度")

# 4. 计算相关系数矩阵
dimension_array = np.array(dimensions)
n_dimensions = len(dimensions)

# 计算斯皮尔曼相关系数
spearman_corr = np.ones((n_dimensions, n_dimensions))
for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        corr, _ = spearmanr(dimension_array[i], dimension_array[j])
        spearman_corr[i, j] = corr
        spearman_corr[j, i] = corr

# 5. 准备所有相关性数据
all_correlations = []
for i in range(n_dimensions):
    for j in range(i+1, n_dimensions):
        corr = spearman_corr[i, j]
        if abs(corr) > MIN_CORRELATION_TO_PLOT:
            all_correlations.append({
                'dim1': dimension_names[i],
                'dim2': dimension_names[j],
                'correlation': corr,
                'abs_correlation': abs(corr)
            })

print(f"  总共 {len(all_correlations)} 条连线满足 |r| > {MIN_CORRELATION_TO_PLOT}")

# 6. 筛选需要标注的连线
if len(all_correlations) > 0:
    # 按相关系数绝对值排序
    sorted_correlations = sorted(all_correlations, key=lambda x: x['abs_correlation'], reverse=True)
    
    # 筛选前N个且满足最小标注阈值的
    correlations_to_label = []
    for corr_data in sorted_correlations:
        if (len(correlations_to_label) < TOP_N_CORRELATIONS_TO_LABEL and 
            corr_data['abs_correlation'] > MIN_CORRELATION_TO_LABEL):
            correlations_to_label.append(corr_data)
    
    print(f"  将标注 {len(correlations_to_label)} 条最强连线")
    label_set = {(corr['dim1'], corr['dim2']) for corr in correlations_to_label}
else:
    print("  警告：没有找到满足条件的相关性连线")
    label_set = set()

# 7. 创建图形（调整尺寸，去除边距）
plt.figure(figsize=(16, 16), facecolor='white')

# 计算15个点在圆上的位置
angles = np.linspace(0, 2 * np.pi, n_dimensions, endpoint=False)
pos = {}
for i, (dim, angle) in enumerate(zip(dimension_names, angles)):
    x = CIRCLE_RADIUS * np.cos(angle)
    y = CIRCLE_RADIUS * np.sin(angle)
    pos[dim] = (x, y)

# 为每个大类设置颜色（按第一个数字）
major_colors = {
    '1': '#FF6B6B',  # 红色 - 第1大类
    '2': '#4ECDC4',  # 青色 - 第2大类
    '3': '#45B7D1',  # 蓝色 - 第3大类
    '4': '#96CEB4',  # 绿色 - 第4大类
    '5': '#FFEAA7',  # 黄色 - 第5大类
}

# 设置线条颜色映射
def get_edge_color(corr_value):
    """根据相关系数返回颜色"""
    if corr_value > 0:
        intensity = min(0.8, abs(corr_value))
        return (0.8, 0.2, 0.2, intensity)  # 暗红色
    else:
        intensity = min(0.8, abs(corr_value))
        return (0.2, 0.2, 0.8, intensity)  # 暗蓝色

# 8. 绘制连线（弱相关先画，强相关后画，这样强相关显示在上层）
all_correlations_sorted = sorted(all_correlations, key=lambda x: x['abs_correlation'])

for corr_data in all_correlations_sorted:
    dim1, dim2, corr = corr_data['dim1'], corr_data['dim2'], corr_data['correlation']
    
    x1, y1 = pos[dim1]
    x2, y2 = pos[dim2]
    
    # 线条宽度与相关系数绝对值成正比
    linewidth = corr_data['abs_correlation'] * 5
    
    # 绘制线条
    plt.plot([x1, x2], [y1, y2], 
            color=get_edge_color(corr),
            linewidth=linewidth,
            alpha=0.7,
            solid_capstyle='round')

# 9. 绘制节点圆圈（按大类配色）
node_radius = NODE_RADIUS_SCALE * 1.2
for i, dim in enumerate(dimension_names):
    x, y = pos[dim]
    major = dim[0]  # 获取大类编号
    color = major_colors.get(major, '#888888')  # 按大类获取颜色
    
    # 绘制圆圈
    circle = plt.Circle((x, y), node_radius, 
                       facecolor=color, 
                       edgecolor='black',
                       linewidth=1.5,
                       alpha=0.9)
    plt.gca().add_patch(circle)
    
    # 在圆圈中心显示维度名称（使用超参数控制的字号）
    plt.text(x, y, dim, 
             fontsize=DIMENSION_LABEL_SIZE, 
             fontweight='bold',
             ha='center', 
             va='center',
             color='black')

# 10. 在连线上标注相关系数（写在连线上）
for corr_data in correlations_to_label:
    dim1, dim2, corr = corr_data['dim1'], corr_data['dim2'], corr_data['correlation']
    
    x1, y1 = pos[dim1]
    x2, y2 = pos[dim2]
    
    # 计算连线上的位置（中间位置）
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    
    # 计算连线角度
    dx = x2 - x1
    dy = y2 - y1
    angle = np.degrees(np.arctan2(dy, dx))
    
    # 确保文本角度在[-90, 90]度范围内，便于阅读
    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180
    
    # 添加直接写在连线上的文本
    label_text = f'{corr:.2f}'
    
    # 根据相关性正负选择文字颜色和背景色
    if corr > 0:
        text_color = 'darkred'
        # 使用RGBA元组格式，而不是字符串
        bg_color = (1.0, 0.8, 0.8, 0.8)  # 浅红色背景，RGBA格式
    else:
        text_color = 'darkblue'
        bg_color = (0.8, 0.8, 1.0, 0.8)  # 浅蓝色背景，RGBA格式
    
    # 在连线上添加文字
    plt.text(mid_x, mid_y,
            label_text,
            fontsize=CORRELATION_LABEL_SIZE,
            fontweight='bold',
            ha='center',
            va='center',
            color=text_color,
            bbox=dict(boxstyle='round,pad=0.15', 
                     facecolor=bg_color,  # 使用RGBA元组
                     alpha=0.8,
                     edgecolor='none',
                     linewidth=0),
            rotation=angle,
            rotation_mode='anchor')

# 11. 设置图形属性
plt.axis('equal')
plt.xlim(-CIRCLE_RADIUS*1.15, CIRCLE_RADIUS*1.15)
plt.ylim(-CIRCLE_RADIUS*1.15, CIRCLE_RADIUS*1.15)
plt.axis('off')

# 去除所有边距
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# 12. 保存图形
output_filename = f'dimensions_correlation_top{TOP_N_CORRELATIONS_TO_LABEL}_clean.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight', pad_inches=0)
print(f"\n图形已保存为: {output_filename}")

# 13. 显示标注的连线详情
if correlations_to_label:
    print(f"\n标注的连线详情（前{len(correlations_to_label)}个最强相关性）:")
    print("-" * 60)
    for i, corr_data in enumerate(correlations_to_label, 1):
        sign = "+" if corr_data['correlation'] > 0 else ""
        print(f"{i:2d}. {corr_data['dim1']} ↔ {corr_data['dim2']}: "
              f"r = {sign}{corr_data['correlation']:.3f}")

plt.show()