import matplotlib.pyplot as plt
import numpy as np

# ==================== 样式配置 ====================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['svg.fonttype'] = 'none'

# CNS风格参数设置
plt.rcParams.update({
    'font.size': 12,
    'axes.labelcolor': 'black', # 显式设置轴标签颜色
    'xtick.color': 'black',     # 显式设置刻度线颜色
    'ytick.color': 'black',
    'axes.linewidth': 1.5,
})

# 颜色定义
COLOR_BLUE = '#1f77b4'
COLOR_ORANGE = '#ff7f0e'
COLOR_GREEN = '#2ca02c'
COLOR_RED = '#d62728'
COLOR_HIGHLIGHT_GOLD = '#FFD700' 
COLOR_LABEL_BG = '#F0F0F0'      

# ==================== 数据准备 ====================
x_labels = [
    'Population=25', 'Population=50', 'Population=75', 'Population=150',
    'Meta-Lr:0.1-0.5', 'Meta-Lr:0.1-0.4', 'Meta-Lr:0.1-0.3',
    'Lr=1e-5', 'Lr=2e-5', 'Lr=5e-5',
    'LoRA_r=8', 'LoRA_r=16', 'LoRA_r=32'
]

values = [
    0.2854, 0.413, 0.3538, 0.3513, 
    0.3005, 0.3512, 0.351,         
    0.1834, 0.351, 0.3577,         
    0.1765, 0.351, 0.3304          
]

segments = [
    {'name': 'Population',    'indices': [0, 1, 2, 3], 'values': values[0:4],   'color': COLOR_BLUE,   'high_idx': 1},
    {'name': 'Meta-Lr',       'indices': [4, 5, 6],    'values': values[4:7],   'color': COLOR_ORANGE, 'high_idx': 2},
    {'name': 'Learning Rate', 'indices': [7, 8, 9],    'values': values[7:10],  'color': COLOR_GREEN,   'high_idx': 1},
    {'name': 'LoRA Rank',     'indices': [10, 11, 12], 'values': values[10:13], 'color': COLOR_RED,    'high_idx': 1}
]

global_highlight_indices = [1, 6, 8, 11] 

def plot_parameter_search():
    # 强制指定背景为白色，防止导出透明或灰底
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')

    for seg in segments:
        indices = seg['indices']
        vals = seg['values']
        color = seg['color']
        high_local_idx = seg['high_idx']
        
        ax.plot(indices, vals, color=color, zorder=2)
        ax.plot(indices, vals, marker='o', linestyle='None', markersize=10, 
                markerfacecolor='white', markeredgecolor=color, markeredgewidth=2, zorder=3)
        
        high_global_idx = indices[high_local_idx]
        high_val = vals[high_local_idx]
        ax.plot(high_global_idx, high_val, marker='o', markersize=16, 
                markerfacecolor=color, markeredgecolor='black', markeredgewidth=2.5, zorder=4)

    # ==================== 坐标轴彻底黑色化 ====================
    ax.set_ylim(0.1, 0.5)
    ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
    
    # 直接修改 Y 轴刻度标注的每一项属性，确保 100% 黑色
    for label in ax.get_yticklabels():
        label.set_color('#000000')  # 强制纯黑十六进制
        label.set_fontweight('bold')
        label.set_fontsize(12)
    
    # 强制修改 Y 轴标题为纯黑
    ax.set_ylabel('5D3S-QSA Score', fontsize=16, fontweight='bold', labelpad=10)
    ax.yaxis.label.set_color('black')

    # 强制设置坐标轴刻度线为纯黑
    ax.tick_params(axis='both', which='major', colors='black', width=1.5, length=6)
    
    ax.set_xlim(-0.8, len(x_labels) - 0.2)
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=12)

    # X轴标签高亮：使用极高对比度的深黑与亮黄
    xtick_labels = ax.get_xticklabels()
    for i, label in enumerate(xtick_labels):
        if i in global_highlight_indices:
            label.set_color('#000000')
            label.set_fontweight('bold')
            # 强化背景框，确保在矢量图中也极度清晰
            label.set_bbox(dict(facecolor=COLOR_HIGHLIGHT_GOLD, 
                                edgecolor='#000000', # 改为黑边框，强调感更强
                                boxstyle='round,pad=0.3', 
                                linewidth=1))
        else:
            label.set_color("#131313") # 即使是普通标签也调深，拒绝浅灰

    # ==================== 边框与辅助线 ====================
    # 组间分割线加深
    dividers = [3.5, 6.5, 9.5]
    for x in dividers:
        ax.axvline(x=x, color="#C1BEBE", linestyle=':', linewidth=1.5, zorder=0)

    # 背景水平网格
    ax.grid(axis='y', linestyle='--', alpha=0.3, color="#ACACAC")

    # 顶部组名标签
    group_centers = [1.5, 5.0, 8.0, 11.0] 
    group_names = ['Population', 'Meta-Lr', 'Learning Rate', 'LoRA Rank']
    for x, name in zip(group_centers, group_names):
        ax.text(x, 0.53, name, ha='center', va='center', fontsize=13, fontweight='bold',
                color='black',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=COLOR_LABEL_BG, edgecolor='#000000', linewidth=1.0),
                transform=ax.transData, clip_on=False) 

    # 强化四个边框为纯黑
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)
        spine.set_alpha(1.0)

    plt.subplots_adjust(top=0.82, bottom=0.25)

    # ==================== 保存输出 ====================
    svg_file = "Parameter_Sensitivity_DeepBlack.svg"
    plt.savefig(svg_file, format='svg', bbox_inches='tight', facecolor=fig.get_facecolor())
    
    print(f"✅ 核心更新：Y轴标签已强制设为 #000000 纯黑。\n文件已生成: {svg_file}")
    plt.show()

if __name__ == '__main__':
    plot_parameter_search()