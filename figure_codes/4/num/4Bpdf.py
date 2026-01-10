import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# ==================== 样式配置 ====================
# 设置全局字体为 Arial
plt.rcParams['font.family'] = 'Arial'
# 关键：设置 PDF 字体类型为 42 (TrueType)，确保导出后文字可编辑
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# CNS风格参数设置
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 12,
    'figure.dpi': 300,
    'axes.linewidth': 1.2, # 边框加粗
    'grid.linewidth': 0.8,
    'lines.linewidth': 2.5, # 折线加粗
})

# 颜色定义 (提取自图片)
COLOR_BLUE = '#1f77b4'
COLOR_ORANGE = '#ff7f0e'
COLOR_GREEN = '#2ca02c'
COLOR_RED = '#d62728'
COLOR_HIGHLIGHT_BG = '#FFF8DC' # 浅黄色背景 (Cornsilk)
COLOR_LABEL_BG = '#F0F0F0'     # 顶部标签灰底

# ==================== 数据准备 ====================
# 数据与图片对应
x_labels = [
    'Population=25', 'Population=50', 'Population=75', 'Population=150',
    'Meta-Lr:0.1-0.5', 'Meta-Lr:0.1-0.4', 'Meta-Lr:0.1-0.3',
    'Lr=1e-5', 'Lr=2e-5', 'Lr=5e-5',
    'LoRA_r=8', 'LoRA_r=16', 'LoRA_r=32'
]

values = [
    0.2854, 0.413, 0.3538, 0.3513, # Population
    0.3005, 0.3512, 0.351,         # Meta-Lr
    0.1834, 0.351, 0.3577,         # Learning Rate (注意：图片中选中的是中间那个)
    0.1765, 0.351, 0.3304          # LoRA Rank
]

# 定义分段信息
# 注意：high_idx 是该段落内第几个点是最高点/选中点 (从0开始)
segments = [
    {'name': 'Population',    'indices': [0, 1, 2, 3], 'values': values[0:4],   'color': COLOR_BLUE,   'high_idx': 1},
    {'name': 'Meta-Lr',       'indices': [4, 5, 6],    'values': values[4:7],   'color': COLOR_ORANGE, 'high_idx': 2},
    {'name': 'Learning Rate', 'indices': [7, 8, 9],    'values': values[7:10],  'color': COLOR_GREEN,  'high_idx': 1}, # 图片中选的是中间的 Lr=2e-5
    {'name': 'LoRA Rank',     'indices': [10, 11, 12], 'values': values[10:13], 'color': COLOR_RED,    'high_idx': 1}
]

# 全局高亮索引 (在整个x_labels中的索引)
global_highlight_indices = [1, 6, 8, 11] 

def plot_parameter_search():
    # 创建画布，长宽比接近图片
    fig, ax = plt.subplots(figsize=(10, 5))

    # ==================== 绘制折线与点 ====================
    for seg in segments:
        indices = seg['indices']
        vals = seg['values']
        color = seg['color']
        high_local_idx = seg['high_idx']
        
        # 1. 绘制折线 (段内连线)
        ax.plot(indices, vals, color=color, zorder=2)
        
        # 2. 绘制普通点 (空心圆)
        # 先绘制所有点为空心
        ax.plot(indices, vals, 
                marker='o', linestyle='None', 
                markersize=10, 
                markerfacecolor='white', 
                markeredgecolor=color, 
                markeredgewidth=2, 
                zorder=3)
        
        # 3. 绘制高亮选中点 (巨大实心圆 + 黑边框)
        high_global_idx = indices[high_local_idx]
        high_val = vals[high_local_idx]
        
        ax.plot(high_global_idx, high_val,
                marker='o', 
                markersize=16, # 巨大
                markerfacecolor=color, # 实心颜色
                markeredgecolor='black', # 黑边框
                markeredgewidth=2.5, 
                zorder=4)
        
        # 4. 添加数值标签框
        # 这里的数值需要手动匹配图片，或者直接读取
        label_text = f"{high_val:.3f}"
        
        ax.annotate(label_text,
                    xy=(high_global_idx, high_val),
                    xytext=(0, 25), # 向上偏移
                    textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold', color=color,
                    bbox=dict(boxstyle='round,pad=0.3', 
                              facecolor='white', 
                              edgecolor=color, 
                              linewidth=1.5))

    # ==================== 坐标轴设置 ====================
    # Y轴
    ax.set_ylim(0.1, 0.5)
    ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_ylabel('5D3S-QSA Score', fontsize=16, fontweight='bold', labelpad=10)
    
    # X轴
    ax.set_xlim(-0.8, len(x_labels) - 0.2)
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=12)

    # ==================== 美化 X 轴标签 ====================
    # 获取所有标签对象
    xtick_labels = ax.get_xticklabels()
    
    for i, label in enumerate(xtick_labels):
        if i in global_highlight_indices:
            # 高亮样式：黑色，加粗，黄色圆角背景
            label.set_color('black')
            label.set_fontweight('bold')
            label.set_bbox(dict(facecolor=COLOR_HIGHLIGHT_BG, 
                                edgecolor='#FFD700', # 金色边框 
                                boxstyle='round,pad=0.2', 
                                alpha=0.6))
        else:
            # 普通样式：灰色
            label.set_color('gray')
            label.set_fontweight('normal')

    # ==================== 添加分割线 ====================
    # 在每组之间添加灰色虚线
    dividers = [3.5, 6.5, 9.5]
    for x in dividers:
        ax.axvline(x=x, color='#A0A0A0', linestyle=':', linewidth=1.5, zorder=0)

    # 添加横向基准线 (虚线)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#D0D0D0')
    ax.grid(axis='x', linestyle='--', alpha=0.3, color='#E0E0E0') # X轴网格淡一点

    # ==================== 添加顶部组名标签 ====================
    # 计算每组的中心位置
    group_centers = [1.5, 5.0, 8.0, 11.0] # 大概的视觉中心
    group_names = ['Population', 'Meta-Lr', 'Learning Rate', 'LoRA Rank']
    
    y_pos = 0.53 # 放在图表上方
    
    for x, name in zip(group_centers, group_names):
        ax.text(x, y_pos, name, 
                ha='center', va='center', 
                fontsize=13, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', 
                          facecolor=COLOR_LABEL_BG, 
                          edgecolor='#C0C0C0', 
                          linewidth=1.0),
                transform=ax.transData, # 使用数据坐标
                clip_on=False) # 允许画在图表外面

    # 调整顶部边距以容纳标签
    plt.subplots_adjust(top=0.85, bottom=0.25)

    # 隐藏上右边框
    # ax.spines['top'].set_visible(False) # 图片里似乎保留了框，只是上面的标签盖住了
    # ax.spines['right'].set_visible(False)
    
    # 确保左下边框是黑色的
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')

    # ==================== 保存输出 ====================
    # 保存为 PDF (矢量)
    pdf_file = "Parameter_Sensitivity_Analysis.pdf"
    plt.savefig(pdf_file, format='pdf', dpi=300, bbox_inches='tight')
    
    # 保存为 PNG (预览)
    png_file = "Parameter_Sensitivity_Analysis.png"
    plt.savefig(png_file, format='png', dpi=300, bbox_inches='tight')
    
    print(f"图表已生成:\n1. {pdf_file} (矢量图)\n2. {png_file} (预览图)")
    plt.show()

if __name__ == '__main__':
    plot_parameter_search()