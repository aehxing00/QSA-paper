import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# ==================== CNS 风格全局配置 ====================
plt.rcParams.update({
    'font.family': 'Arial',
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
    'pdf.fonttype': 42,  # 确保PDF文字可编辑
    'ps.fonttype': 42,
    'figure.autolayout': True
})

# 颜色与线条定义（精确复刻图片颜色）
COLOR_BASE = '#1f77b4'       # 基础模型：蓝色
COLOR_FINETUNED = '#ff7f0e'  # 微调模型：橙色
GRID_COLOR = '#d9d9d9'       # 网格线颜色

# 定义大类映射（匹配图片的换行布局）
CATEGORY_MAPPING = {
    '1': 'Ontological\nDistinction',
    '2': 'Depth\nPerception',
    '3': 'Recursive\nThinking',
    '4': 'Social\nMirroring',
    '5': 'Identity\n&\nPersonality'
}

SUBCATEGORY_MAPPING = {
    '1A': '1', '1B': '1', '1C': '1',
    '2A': '2', '2B': '2', '2C': '2',
    '3A': '3', '3B': '3', '3C': '3',
    '4A': '4', '4B': '4', '4C': '4',
    '5A': '5', '5B': '5', '5C': '5'
}

def process_data(df):
    """处理数据：自动识别模型组并计算5类均值"""
    subcategories = df.iloc[:, 0].tolist()
    category_data = {}
    model_columns = []

    # 识别模型（假设每5列为一个模型的重复实验）
    for i in range(1, len(df.columns), 5):
        model_name = df.columns[i]
        cols = list(range(i, min(i + 5, len(df.columns))))
        model_columns.append((model_name, cols))

    for model_name, col_indices in model_columns:
        cat_agg = {k: [] for k in ['1', '2', '3', '4', '5']}
        for row_idx, subcat in enumerate(subcategories):
            key = str(subcat).strip().split()[0]
            if key in SUBCATEGORY_MAPPING:
                cat_id = SUBCATEGORY_MAPPING[key]
                vals = df.iloc[row_idx, col_indices].dropna().astype(float).values
                if len(vals) > 0:
                    cat_agg[cat_id].append(np.mean(vals))

        final_means = [np.mean(cat_agg[c]) if cat_agg[c] else 0 for c in ['1', '2', '3', '4', '5']]
        category_data[model_name] = final_means
    return category_data

def generate_radar_pdf():
    input_filename = "a3.xlsx"
    try:
        df = pd.read_excel(input_filename)
        data = process_data(df)
        models = list(data.keys())[:2] # 仅对比前两个

        # 雷达图几何设置
        categories = [CATEGORY_MAPPING[str(i)] for i in range(1, 6)]
        N = len(categories)
        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        angles += angles[:1] # 闭合

        # 创建矢量画布
        fig = plt.figure(figsize=(10, 10), dpi=300)
        ax = fig.add_subplot(111, polar=True)

        # 布局调整：起始位置12点钟方向，顺时针旋转
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        # 绘制模型数据
        # 1. Base Model (蓝色实线)
        val0 = data[models[0]] + [data[models[0]][0]]
        ax.plot(angles, val0, color=COLOR_BASE, linewidth=4, linestyle='-', label='Base Model', zorder=3)
        ax.fill(angles, val0, color=COLOR_BASE, alpha=0.1)

        # 2. Fine-tuned Model (橙色粗虚线)
        val1 = data[models[1]] + [data[models[1]][0]]
        ax.plot(angles, val1, color=COLOR_FINETUNED, linewidth=5, linestyle='--', label='Fine-tuned Model', zorder=4)
        ax.fill(angles, val1, color=COLOR_FINETUNED, alpha=0.2)

        # 坐标轴与网格美化
        ax.set_ylim(0, 0.6)
        ax.set_yticks([0.2, 0.4, 0.6])
        ax.set_yticklabels(["0.2", "0.4", "0.6"], fontsize=20, weight='bold', color='#333333')
        ax.set_rlabel_position(0) # 刻度文字放在12点钟线

        # 设置外圈大类标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=22, weight='bold', color='#262626')
        ax.tick_params(axis='x', pad=35) # 标签外扩

        # 网格样式
        ax.grid(True, color=GRID_COLOR, linewidth=1.2, linestyle='-')
        ax.spines['polar'].set_linewidth(2)
        ax.spines['polar'].set_edgecolor('#000000')

        # 图例复刻：右上角，黑框白底
        legend = ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1),
                           frameon=True, fontsize=20, title='Models',
                           title_fontsize=18, edgecolor='black', facecolor='white')
        legend.get_frame().set_linewidth(1.5)
        legend.get_frame().set_alpha(1.0)

        # 保存为PDF矢量图和预览用PNG
        pdf_path = "radar_chart_standard.pdf"
        plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
        plt.savefig("radar_chart_preview.png", format='png', bbox_inches='tight', dpi=300)

        print(f"成功导出矢量图: {pdf_path}")
        plt.show()

    except Exception as e:
        print(f"处理出错: {e}")

if __name__ == '__main__':
    generate_radar_pdf()