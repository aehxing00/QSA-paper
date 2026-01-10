import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 样式配置 ====================
# 设置全局字体为 Arial (或系统无衬线字体)，保证粗体效果
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
# 关键：设置 PDF 字体类型为 42 (TrueType)，确保导出后文字可编辑
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 颜色定义 (提取自图片)
COLOR_GEMINI = '#1f77b4'  # 蓝色
COLOR_DEEPSEEK = '#ff7f0e' # 橙色
GRID_COLOR = '#D3D3D3'     # 网格灰

# 字体大小设置
FONT_SIZE_LABEL = 21       # 外部大类标签字体
FONT_SIZE_TICK = 19        # 内部数值刻度字体
FONT_SIZE_LEGEND = 18      # 图例字体

# ==================== 数据处理逻辑 ====================
# 定义大类映射关系
CATEGORY_MAPPING = {
    '1': 'Ontological\nDistinction',
    '2': 'Depth\nPerception',
    '3': 'Recursive\nThinking',
    '4': 'Social\nMirroring',
    '5': 'Identity\n&\nPersonality' # 手动换行以匹配图片布局
}

# 子项到大类的映射
SUBCATEGORY_MAPPING = {
    '1A': '1', '1B': '1', '1C': '1',
    '2A': '2', '2B': '2', '2C': '2',
    '3A': '3', '3B': '3', '3C': '3',
    '4A': '4', '4B': '4', '4C': '4',
    '5A': '5', '5B': '5', '5C': '5'
}

def process_data(df):
    """处理数据，将子项合并为大类并计算平均值"""
    subcategories = df.iloc[:, 0].tolist()
    category_data = {}

    # 识别模型列 (假设每5列为一个模型)
    model_columns = []
    current_model = None
    model_data_cols = []

    for col_idx in range(1, len(df.columns)):
        col_name = df.columns[col_idx]
        # 简单逻辑：每5列一组
        if len(model_data_cols) == 0:
            current_model = col_name
            model_data_cols.append(col_idx)
        elif len(model_data_cols) < 5:
            model_data_cols.append(col_idx)

        if len(model_data_cols) == 5:
            model_columns.append((current_model, model_data_cols))
            model_data_cols = []
            current_model = None

    # 计算均值
    for model_name, col_indices in model_columns:
        category_means = {k: [] for k in ['1', '2', '3', '4', '5']}

        for row_idx, subcat in enumerate(subcategories):
            if not isinstance(subcat, str): continue
            subcat_key = subcat.strip().split()[0]

            if subcat_key in SUBCATEGORY_MAPPING:
                cat_id = SUBCATEGORY_MAPPING[subcat_key]
                vals = []
                for c_idx in col_indices:
                    val = df.iloc[row_idx, c_idx]
                    try:
                        v = float(val)
                        if not np.isnan(v): vals.append(v)
                    except: pass

                if vals:
                    category_means[cat_id].append(np.mean(vals))

        final_means = []
        for cat_id in ['1', '2', '3', '4', '5']:
            vals = category_means[cat_id]
            final_means.append(np.mean(vals) if vals else 0)

        category_data[model_name] = final_means

    return category_data

def generate_radar_chart():
    input_filename = "a3.xlsx"

    try:
        df = pd.read_excel(input_filename)
        print(f"成功读取: {input_filename}")
    except Exception as e:
        print(f"读取错误: {e}")
        # 为了演示，如果读取失败，生成假数据
        print("生成测试数据用于演示图表效果...")
        df = pd.DataFrame() # 实际使用请确保文件存在

    # 处理数据
    if not df.empty:
        category_data = process_data(df)
    else:
        # 兜底假数据 (仅用于展示代码效果)
        category_data = {
            'Gemini-3-pro': [0.05, 0.03, 0.06, 0.08, 0.06],
            'Deepseek-r1': [0.10, 0.08, 0.13, 0.11, 0.07]
        }

    # 准备绘图数据
    categories = [CATEGORY_MAPPING[str(i)] for i in range(1, 6)]
    N = len(categories)

    # 角度设置：从12点钟方向开始，顺时针旋转
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1] # 闭合

    # 创建画布
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # 设置方向：正北(12点)为0度，顺时针旋转
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # 绘制数据
    models = list(category_data.keys())

    # 强制样式映射，以符合图片要求
    # Model 1 (Gemini): 蓝色实线
    # Model 2 (Deepseek): 橙色虚线

    styles = [
        {'color': COLOR_GEMINI, 'ls': '-', 'label': 'Gemini-3-pro'}, # 默认第一个
        {'color': COLOR_DEEPSEEK, 'ls': '--', 'label': 'Deepseek-r1'}  # 默认第二个
    ]

    for idx, model_name in enumerate(models[:2]): # 只取前两个
        values = category_data[model_name]
        values += values[:1] # 闭合

        style = styles[idx] if idx < len(styles) else styles[0]
        # 如果Excel里的名字不一样，优先使用Excel里的名字，但保留样式
        label_text = model_name

        ax.plot(angles, values,
                color=style['color'],
                linewidth=4, # 加粗线条
                linestyle=style['ls'],
                label=label_text)

        # 填充颜色
        ax.fill(angles, values, color=style['color'], alpha=0.15)

    # ==================== 坐标轴与网格设置 ====================
    # 设置大类标签 (外部)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=FONT_SIZE_LABEL, color='#333333')

    # 调整标签位置，避免重叠
    ax.tick_params(axis='x', pad=30) # 增加标签与图的距离

    # 设置数值标签 (内部同心圆)
    ax.set_ylim(0, 0.15)
    yticks = [0.05, 0.10, 0.15]
    ax.set_yticks(yticks)
    # y轴标签显示在正北方向稍微偏右一点，避免遮挡线
    ax.set_rlabel_position(0)
    ax.set_yticklabels([str(y) for y in yticks],
                       fontsize=FONT_SIZE_TICK,
                       fontweight='bold',
                       color='#404040')

    # 美化网格线
    ax.grid(True, color=GRID_COLOR, linestyle='-', linewidth=1.5, alpha=0.7)

    # 移除外圈的圆形边框 spine，或者设为灰色
    ax.spines['polar'].set_color('black')
    ax.spines['polar'].set_linewidth(1.5)

    # ==================== 图例设置 ====================
    # 放置在右上角，带边框
    legend = ax.legend(loc='upper right',
                      bbox_to_anchor=(1.3, 1.15), # 手动调整位置
                      fontsize=FONT_SIZE_LEGEND,
                      title='Models',
                      title_fontsize=FONT_SIZE_LEGEND + 2,
                      frameon=True,
                      edgecolor='black', # 黑框
                      facecolor='white', # 白底
                      framealpha=1)

    # 加粗图例边框
    legend.get_frame().set_linewidth(1.5)

    # 调整布局
    plt.tight_layout()

    # ==================== 保存输出 ====================
    # 保存为 PDF (矢量)
    pdf_file = "Model_Comparison_Radar.pdf"
    plt.savefig(pdf_file, format='pdf', dpi=300, bbox_inches='tight')

    # 保存为 PNG (预览)
    png_file = "Model_Comparison_Radar.png"
    plt.savefig(png_file, format='png', dpi=300, bbox_inches='tight', transparent=False)

    print(f"图表已生成:\n1. {pdf_file} (矢量图，适合投稿)\n2. {png_file} (预览图)")
    plt.show()

if __name__ == '__main__':
    generate_radar_chart()