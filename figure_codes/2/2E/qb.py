import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --- 绘图风格设置 ---
plt.rcParams['font.family'] = 'sans-serif'
# 优先使用 Arial (常用无衬线体)，备选 SimHei (黑体)
plt.rcParams['font.sans-serif'] = ['Arial', 'SimHei', 'DejaVu Sans']
# 基础字体不再全局设为粗体，以便我们在代码中手动控制大类/小类的粗细
plt.rcParams['font.weight'] = 'normal' 
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 2  # 图表边框加粗
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2

def calculate_cronbach_stats(df_subset):
    """ 计算 Cronbach's Alpha """
    item_scores = df_subset.T
    n_samples, n_items = item_scores.shape
    
    if n_items < 2:
        return np.nan
    
    item_variances = item_scores.var(axis=0, ddof=1)
    total_scores = item_scores.sum(axis=1)
    total_variance = total_scores.var(ddof=1)
    
    if total_variance == 0:
        alpha = 0.0
    else:
        alpha = (n_items / (n_items - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha

def plot_custom_style(summary_data, output_img='panda_alpha_final.png'):
    """
    绘制符合要求的柱状图:
    1. 大类仅加粗，字号不加大
    2. Y轴刻度重点展示 0.8, 0.9, 1.0
    """
    print("正在绘制图表...")
    
    fig, ax = plt.subplots(figsize=(18, 9))
    
    # 颜色池 (Tab20)
    colors = plt.cm.tab20.colors 
    color_idx = 0
    
    x_positions = []
    x_labels = []
    heights = []
    bar_colors = []
    
    # 记录大类标签的索引
    major_label_indices = [] 
    
    current_x = 0
    gap_width = 1.5 
    
    df_sum = pd.DataFrame(summary_data)
    major_ids = sorted(df_sum[df_sum['Level'] == 'Major-Category']['ID'].unique())
    
    # --- 数据构建 ---
    for maj_id in major_ids:
        # 1. 大类数据
        maj_row = df_sum[(df_sum['Level'] == 'Major-Category') & (df_sum['ID'] == maj_id)].iloc[0]
        
        x_positions.append(current_x)
        x_labels.append(maj_row['Name']) # 仅显示名称
        major_label_indices.append(len(x_labels) - 1) # 记录索引
        
        heights.append(maj_row['Cronbach_Alpha'])
        bar_colors.append(colors[color_idx % len(colors)])
        color_idx += 1
        current_x += 1
        
        # 2. 小类数据
        sub_rows = df_sum[
            (df_sum['Level'] == 'Sub-Category') & 
            (df_sum['ID'].str.startswith(maj_id))
        ].sort_values('ID')
        
        for _, sub_row in sub_rows.iterrows():
            x_positions.append(current_x)
            x_labels.append(sub_row['Name'])
            heights.append(sub_row['Cronbach_Alpha'])
            bar_colors.append(colors[color_idx % len(colors)])
            color_idx += 1
            current_x += 1
            
        # 3. 空隙
        current_x += gap_width - 1
        
    # --- 绘图 ---
    ax.bar(x_positions, heights, 
           color=bar_colors, 
           edgecolor='black',
           linewidth=1.5,
           width=0.8,
           zorder=3)

    # --- Y 轴刻度设置 (核心修改) ---
    ax.set_ylim(0.8, 1.0)
    # 显式设置刻度，包含底部基础刻度和顶部的高分段刻度
    custom_yticks = [0.8,0.9,1.0]
    ax.set_yticks(custom_yticks)
    # 刻度字体加粗，字号14
    ax.set_yticklabels([f"{y:.1f}" for y in custom_yticks], fontsize=14, fontweight='bold')
    
    ax.set_ylabel("Cronbach's α Coefficient", fontsize=18, fontweight='bold', labelpad=10)
    
    # --- X 轴设置 ---
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_xlim(-1, current_x - gap_width + 1)

    # --- X 轴标签差异化处理 (核心修改) ---
    xtick_labels = ax.get_xticklabels()
    
    for i, label in enumerate(xtick_labels):
        # 统一设置字号为 13
        label.set_fontsize(13)
        
        if i in major_label_indices:
            # 大类：设为粗体
            label.set_fontweight('bold')
            # 也可以选 'heavy' 更粗一点
        else:
            # 小类：设为普通 (根据你的要求：大类粗体就好)
            label.set_fontweight('normal')

    # --- 辅助线 ---
    ax.grid(axis='y', linestyle='-', alpha=0.4, color='gray', zorder=0)
    
    # --- 边框设置 ---
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('black')

    plt.show()

def main():
    # --- 1. 读取数据 ---
    file_path = 'panda_detailed_scores.xlsx'
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print("Loading data...")
    df = pd.read_excel(file_path)
    
    id_col = df.columns[0]
    score_cols = df.columns[1:]
    df[id_col] = df[id_col].astype(str)

    # --- 2. 类别解析 ---
    df['Major_Cat_ID'] = df[id_col].str[0]
    df['Sub_Cat_ID'] = df[id_col].str[:2]

    # --- 3. 英文名称映射 ---
    cat_names = {
        '1': 'Ontological Distinction',
        '2': 'Depth Perception',
        '3': 'Recursive Thinking',
        '4': 'Social Mirroring',
        '5': 'Identity & Personality',
        '1A': 'Boundary Sense', '1B': 'Self-Awareness', '1C': 'Subjectivity',
        '2A': 'Multimodal Integration', '2B': 'World Model', '2C': 'Embodiment',
        '3A': 'Recursive Reflection', '3B': 'Metacognition', '3C': 'Error Correction',
        '4A': 'Mirroring Others', '4B': 'Role Understanding', '4C': 'Interactional Synchrony',
        '5A': 'Time Perception', '5B': 'Desire & Purpose', '5C': 'Core Personality'
    }

    results_list = []

    print("Calculating Alpha...")

    # --- 4. 计算小类 ---
    sub_cats = sorted(df['Sub_Cat_ID'].unique())
    for sub in sub_cats:
        subset = df[df['Sub_Cat_ID'] == sub]
        data_for_calc = subset.set_index(id_col)[score_cols]
        alpha = calculate_cronbach_stats(data_for_calc)
        
        results_list.append({
            'Level': 'Sub-Category', 'ID': sub, 'Name': cat_names.get(sub, sub), 'Cronbach_Alpha': alpha
        })

    # --- 5. 计算大类 ---
    major_cats = sorted(df['Major_Cat_ID'].unique())
    for maj in major_cats:
        subset = df[df['Major_Cat_ID'] == maj]
        data_for_calc = subset.set_index(id_col)[score_cols]
        alpha = calculate_cronbach_stats(data_for_calc)
        
        results_list.append({
            'Level': 'Major-Category', 'ID': maj, 'Name': cat_names.get(maj, maj), 'Cronbach_Alpha': alpha
        })

    # --- 6. 导出数据 ---
    pd.DataFrame(results_list).to_excel('panda_alpha_analysis.xlsx', index=False)

    # --- 7. 绘图 ---
    plot_custom_style(results_list)

if __name__ == "__main__":
    main()