import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 样式配置 ====================
# 设置全局字体
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# 关键：设置 SVG 文字类型，确保导出后文字可编辑而非轮廓化
plt.rcParams['svg.fonttype'] = 'none'

# 颜色定义
COLOR_GEMINI = '#1f77b4'   # 蓝色
COLOR_DEEPSEEK = '#ff7f0e' # 橙色
GRID_COLOR = '#D3D3D3'     # 网格灰

# 字体大小设置
FONT_SIZE_LABEL = 21       
FONT_SIZE_TICK = 19        
FONT_SIZE_LEGEND = 18      

# ==================== 数据处理逻辑 ====================
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
    subcategories = df.iloc[:, 0].tolist()
    category_data = {}

    model_columns = []
    current_model = None
    model_data_cols = []

    for col_idx in range(1, len(df.columns)):
        col_name = df.columns[col_idx]
        if len(model_data_cols) == 0:
            current_model = col_name
            model_data_cols.append(col_idx)
        elif len(model_data_cols) < 5:
            model_data_cols.append(col_idx)

        if len(model_data_cols) == 5:
            model_columns.append((current_model, model_data_cols))
            model_data_cols = []
            current_model = None

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

    if os.path.exists(input_filename):
        df = pd.read_excel(input_filename)
        category_data = process_data(df)
    else:
        print("未找到 a3.xlsx，生成测试数据预览效果...")
        category_data = {
            'Gemini-3-pro': [0.05, 0.03, 0.06, 0.08, 0.06],
            'Deepseek-r1': [0.10, 0.08, 0.13, 0.11, 0.07]
        }

    categories = [CATEGORY_MAPPING[str(i)] for i in range(1, 6)]
    N = len(categories)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1] 

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    models = list(category_data.keys())
    styles = [
        {'color': COLOR_GEMINI, 'ls': '-', 'label': 'Gemini-3-pro'},
        {'color': COLOR_DEEPSEEK, 'ls': '--', 'label': 'Deepseek-r1'}
    ]

    for idx, model_name in enumerate(models[:2]):
        values = category_data[model_name]
        values += values[:1]
        style = styles[idx] if idx < len(styles) else styles[0]

        ax.plot(angles, values,
                color=style['color'],
                linewidth=4, 
                linestyle=style['ls'],
                label=model_name)
        ax.fill(angles, values, color=style['color'], alpha=0.15)

    # 坐标轴与网格
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=FONT_SIZE_LABEL, color='#333333')
    ax.tick_params(axis='x', pad=35) 

    ax.set_ylim(0, 0.15)
    yticks = [0.05, 0.10, 0.15]
    ax.set_yticks(yticks)
    ax.set_rlabel_position(0)
    ax.set_yticklabels([str(y) for y in yticks],
                       fontsize=FONT_SIZE_TICK,
                       fontweight='bold',
                       color='#404040')

    ax.grid(True, color=GRID_COLOR, linestyle='-', linewidth=1.5, alpha=0.7)
    ax.spines['polar'].set_color('black')
    ax.spines['polar'].set_linewidth(1.5)

    legend = ax.legend(loc='upper right',
                      bbox_to_anchor=(1.35, 1.15), 
                      fontsize=FONT_SIZE_LEGEND,
                      title='Models',
                      title_fontsize=FONT_SIZE_LEGEND + 2,
                      frameon=True,
                      edgecolor='black',
                      facecolor='white',
                      framealpha=1)
    legend.get_frame().set_linewidth(1.5)

    plt.tight_layout()

    # ==================== 保存为 SVG ====================
    svg_file = "Model_Comparison_Radar.svg"
    # 使用 bbox_inches='tight' 确保旋转的标签不被切掉
    plt.savefig(svg_file, format='svg', bbox_inches='tight')
    
    # 同时也保存一个预览 PNG
    plt.savefig("Model_Comparison_Radar_Preview.png", format='png', dpi=300, bbox_inches='tight')

    print(f"✅ 成功! 矢量图已保存为: {svg_file}")
    plt.show()

if __name__ == '__main__':
    generate_radar_chart()