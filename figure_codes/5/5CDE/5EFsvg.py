import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import warnings

warnings.filterwarnings('ignore')

# ==================== 全局绘图配置 (SVG 矢量化优化) ====================
plt.rcParams.update({
    'font.family': 'Arial',
    'font.weight': 'bold',         # 全局字体加粗
    'axes.labelweight': 'bold',    # 坐标轴标题加粗
    'axes.titleweight': 'bold',    # 图表标题加粗
    'font.size': 30,               # 基础字号加大
    'svg.fonttype': 'none',        # 关键：确保SVG文字可编辑，不转为路径
    'figure.autolayout': False,    
    'xtick.direction': 'out',      # 刻度向外
    'ytick.direction': 'out',
    'lines.linewidth': 2.0         
})

# 颜色定义
COLOR_BEFORE = '#84C284'   # 绿色
COLOR_AFTER = '#B584BD'    # 紫色
BASELINE_COLOR = '#CCCCCC' # 浅灰色虚线

# 视觉参数
SPINE_WIDTH = 2.5       
TICK_WIDTH = 2.5        
TICK_LENGTH = 8        
BAR_WIDTH = 0.35        

class SelfAwarenessStabilityVisualizer:
    def __init__(self):
        # 模拟数据
        self.metrics_data = {
            'UMAP\nSilhouette': {'before': 1.0, 'after': 1.20},
            'UMAP\nSeparation\nRatio': {'before': 1.0, 'after': 1.11},
            'UMAP\nCalinski-Harabasz': {'before': 1.0, 'after': 1.0},
            'PCA\nSilhouette': {'before': 1.0, 'after': 1.20},
            'PCA\nCalinski-Harabasz': {'before': 1.0, 'after': 1.08},
            'UMAP\nDavies-Bouldin': {'before': 1.0, 'after': 1.14},
            'PCA\nSeparation\nRatio': {'before': 1.0, 'after': 1.17}
        }
        
        self.dimension_data = {
            'Identity &\nPersonality': {'before': 1.0, 'after': 0.975},
            'Social\nMirroring': {'before': 1.0, 'after': 0.968},
            'Recursive\nThinking': {'before': 1.0, 'after': 0.955},
            'Depth\nPerception': {'before': 1.0, 'after': 1.02}, 
            'Ontological\nDistinction': {'before': 1.0, 'after': 0.965}
        }
        print("可视化系统就绪（SVG 优化版）。")

    def _apply_axis_style(self, ax):
        """应用统一的粗线条坐标轴风格"""
        ax.spines['left'].set_linewidth(SPINE_WIDTH)
        ax.spines['bottom'].set_linewidth(SPINE_WIDTH)
        # 强制设为纯黑
        ax.spines['left'].set_color('#000000')
        ax.spines['bottom'].set_color('#000000')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(width=TICK_WIDTH, length=TICK_LENGTH, labelsize=14, colors='#000000')

    def create_stability_metrics_bar_chart(self):
        """生成图1：纵向柱状图 (SVG)"""
        labels = list(self.metrics_data.keys())
        before_vals = [self.metrics_data[k]['before'] for k in labels]
        after_vals = [self.metrics_data[k]['after'] for k in labels]
        
        x = np.arange(len(labels))
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
        
        # 1. 绘制基准线
        ax.axhline(y=1.0, color=BASELINE_COLOR, linestyle='--', linewidth=3, zorder=0)
        
        # 2. 绘制柱状图
        ax.bar(x - BAR_WIDTH/2, before_vals, BAR_WIDTH, color=COLOR_BEFORE, label='Before', zorder=3)
        ax.bar(x + BAR_WIDTH/2, after_vals, BAR_WIDTH, color=COLOR_AFTER, label='After', zorder=3)
        
        # 3. 设置Y轴
        ax.set_ylim(0.9, 1.2)
        ax.set_yticks([0.9, 1.0, 1.1, 1.2])
        ax.set_ylabel('Relative Value (Before = 1.0)', fontsize=15, fontweight='bold', labelpad=15, color='#000000')
        
        # 4. 设置X轴
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', rotation_mode='anchor', 
                           fontsize=20, fontweight='normal', color='#000000')
        
        self._apply_axis_style(ax)
        ax.grid(axis='x', which='major', color='#F0F0F0', linewidth=1, zorder=0)
        
        plt.tight_layout()
        plt.savefig('Fig1_Stability_Metrics.svg', format='svg', bbox_inches='tight')
        return fig

    def create_dimension_separation_bar_chart(self):
        """生成图2：横向柱状图 (SVG)"""
        labels = list(self.dimension_data.keys())
        before_vals = [self.dimension_data[k]['before'] for k in labels]
        after_vals = [self.dimension_data[k]['after'] for k in labels]
        
        y = np.arange(len(labels))
        height = 0.35
        
        fig, ax = plt.subplots(figsize=(4, 5), facecolor='white')
        
        # 1. 绘制基准线
        ax.axvline(x=1.0, color=BASELINE_COLOR, linestyle='--', linewidth=3, zorder=0)
        
        # 2. 绘制横向柱状图
        ax.barh(y - height/2, before_vals, height, color=COLOR_BEFORE, label='Before', zorder=3)
        ax.barh(y + height/2, after_vals, height, color=COLOR_AFTER, label='After', zorder=3)
        
        # 3. 设置X轴
        ax.set_xlim(0.90, 1.05)
        ax.set_xticks([0.90, 0.95, 1.00, 1.05])
        ax.set_xlabel('Relative Separation (Before = 1.0)', fontsize=12, fontweight='bold', labelpad=15, color='#000000')
        
        # 4. 设置Y轴
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=15, fontweight='normal', color='#000000')
        
        self._apply_axis_style(ax)
        ax.grid(axis='y', which='major', color='#F0F0F0', linewidth=1, zorder=0)
        
        plt.tight_layout()
        plt.savefig('Fig2_Dimension_Separation.svg', format='svg', bbox_inches='tight')
        return fig

    def create_all_stability_figures(self):
        self.create_stability_metrics_bar_chart()
        self.create_dimension_separation_bar_chart()
        plt.show()
        print("图表已生成并保存为可编辑的 SVG。")

if __name__ == "__main__":
    visualizer = SelfAwarenessStabilityVisualizer()
    visualizer.create_all_stability_figures()