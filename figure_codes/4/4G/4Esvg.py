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
    # 关键：设置 SVG 字体类型为 none，确保导出后文字可编辑而非转为路径
    'svg.fonttype': 'none',
    'figure.autolayout': True
})

# 颜色与线条定义
COLOR_BASE = '#1f77b4'       # 基础模型：蓝色
COLOR_FINETUNED = '#ff7f0e'  # 微调模型：橙色
GRID_COLOR = '#d9d9d9'       # 网格线颜色

# 定义大类映射
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

    # 识别模型
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

def generate_radar_svg():
    input_filename = "a3.xlsx"
    try:
        df = pd.read_excel(input_filename)
        data = process_data(df)
        models = list(data.keys())[:2] 

        # 雷达图几何设置
        categories = [CATEGORY_MAPPING[str(i)] for i in range(1, 6)]
        N = len(categories)
        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        angles += angles[:1] 

        # 创建矢量画布
        fig = plt.figure(figsize=(10, 10), dpi=300, facecolor='white')
        ax = fig.add_subplot(111, polar=True)

        # 布局调整
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        # 绘制模型数据
        # 1. Base Model
        val0 = data[models[0]] + [data[models[0]][0]]
        ax.plot(angles, val0, color=COLOR_BASE, linewidth=4, linestyle='-', label='Base Model', zorder=3)
        ax.fill(angles, val0, color=COLOR_BASE, alpha=0.1)

        # 2. Fine-tuned Model
        val1 = data[models[1]] + [data[models[1]][0]]
        ax.plot(angles, val1, color=COLOR_FINETUNED, linewidth=5, linestyle='--', label='Fine-tuned Model', zorder=4)
        ax.fill(angles, val1, color=COLOR_FINETUNED, alpha=0.2)

        # 坐标轴与网格美化 (强制纯黑标注)
        ax.set_ylim(0, 0.6)
        ax.set_yticks([0.2, 0.4, 0.6])
        ax.set_yticklabels(["0.2", "0.4", "0.6"], fontsize=24, weight='bold', color='#000000')
        ax.set_rlabel_position(0) 

        # 设置外圈标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=26, weight='bold', color='#000000')
        ax.tick_params(axis='x', pad=35, colors='#000000') 

        # 网格与边框样式
        ax.grid(True, color=GRID_COLOR, linewidth=1.2, linestyle='-')
        ax.spines['polar'].set_linewidth(2.5)
        ax.spines['polar'].set_edgecolor('#000000') # 强制外圆为纯黑

        # 图例：右上角，黑框白底
        legend = ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1),
                           frameon=True, fontsize=23, title='Models',
                           title_fontsize=18, edgecolor='#000000', facecolor='white')
        legend.get_frame().set_linewidth(1.5)
        legend.get_frame().set_alpha(1.0)

        # 保存为 SVG 矢量图
        svg_path = "radar_chart_final.svg"
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        
        # 保存 PNG 用于快速查看
        plt.savefig("radar_chart_preview.png", format='png', bbox_inches='tight', dpi=300)

        print(f"✅ 成功! 矢量图已保存为: {svg_path}")
        plt.show()

    except Exception as e:
        print(f"处理出错: {e}")

if __name__ == '__main__':
    generate_radar_svg()