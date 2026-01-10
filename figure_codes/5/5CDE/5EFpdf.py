import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import warnings

warnings.filterwarnings('ignore')

# ==================== 全局绘图配置 (复刻 sshot-1/2 风格) ====================
plt.rcParams.update({
    'font.family': 'Arial',
    'font.weight': 'bold',         # 全局字体加粗
    'axes.labelweight': 'bold',    # 坐标轴标题加粗
    'axes.titleweight': 'bold',    # 图表标题加粗
    'font.size': 14,               # 基础字号加大
    'pdf.fonttype': 42,            # 确保PDF文字可编辑
    'ps.fonttype': 42,
    'figure.autolayout': False,    # 手动控制布局
    'xtick.direction': 'out',      # 刻度向外
    'ytick.direction': 'out',
    'lines.linewidth': 2.0         # 线条基础粗细
})

# 颜色定义 (精确提取自截图)
COLOR_BEFORE = '#84C284'  # 绿色 (Before)
COLOR_AFTER = '#B584BD'   # 紫色 (After)
BASELINE_COLOR = '#CCCCCC' # 浅灰色虚线

# 视觉参数 (加粗风格)
SPINE_WIDTH = 2.5       # 坐标轴线宽 (模拟马克笔风格)
TICK_WIDTH = 2.5        # 刻度线宽
TICK_LENGTH = 8         # 刻度线长度
BAR_WIDTH = 0.35        # 柱子宽度

class SelfAwarenessStabilityVisualizer:
    def __init__(self):
        # 初始化数据 (为了演示效果，这里内置了模拟数据)
        # 实际使用时，请替换为您自己的 Excel 加载逻辑
        self.metrics_data = {
            'UMAP\nSilhouette': {'before': 1.0, 'after': 1.20},
            'UMAP\nSeparation\nRatio': {'before': 1.0, 'after': 1.11},
            'UMAP\nCalinski-Harabasz': {'before': 1.0, 'after': 1.0}, # 示例
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
        
        print("可视化系统就绪。")

    def _apply_axis_style(self, ax):
        """应用统一的粗线条坐标轴风格"""
        # 加粗左侧和底部坐标轴
        ax.spines['left'].set_linewidth(SPINE_WIDTH)
        ax.spines['bottom'].set_linewidth(SPINE_WIDTH)
        # 隐藏顶部和右侧
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # 设置刻度线样式
        ax.tick_params(width=TICK_WIDTH, length=TICK_LENGTH, labelsize=14)

    def create_stability_metrics_bar_chart(self):
        """复刻图1：纵向柱状图 (sshot-1.png)"""
        print("生成图1 (纵向)...")
        
        labels = list(self.metrics_data.keys())
        before_vals = [self.metrics_data[k]['before'] for k in labels]
        after_vals = [self.metrics_data[k]['after'] for k in labels]
        
        x = np.arange(len(labels))
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 1. 绘制基准线 (y=1.0) - 放在最底层
        ax.axhline(y=1.0, color=BASELINE_COLOR, linestyle='--', linewidth=3, zorder=0)
        
        # 2. 绘制柱状图
        ax.bar(x - BAR_WIDTH/2, before_vals, BAR_WIDTH, color=COLOR_BEFORE, label='Before', zorder=3)
        ax.bar(x + BAR_WIDTH/2, after_vals, BAR_WIDTH, color=COLOR_AFTER, label='After', zorder=3)
        
        # 3. 设置Y轴 (范围 0.9 - 1.2)
        ax.set_ylim(0.9, 1.2)
        ax.set_yticks([0.9, 1.0, 1.1, 1.2])
        # Y轴标题：巨大、加粗
        ax.set_ylabel('Relative Value (Before = 1.0)', fontsize=24, fontweight='bold', labelpad=15)
        
        # 4. 设置X轴
        ax.set_xticks(x)
        # 标签旋转45度，右对齐
        ax.set_xticklabels(labels, rotation=45, ha='right', rotation_mode='anchor', 
                           fontsize=16, fontweight='normal') # 标签保持清晰不加粗
        
        # 应用样式
        self._apply_axis_style(ax)
        
        # 添加极淡的竖向网格辅助
        ax.grid(axis='x', which='major', color='#F0F0F0', linewidth=1, zorder=0)
        
        plt.tight_layout()
        plt.savefig('Fig1_Stability_Metrics.pdf', format='pdf', bbox_inches='tight')
        return fig

    def create_dimension_separation_bar_chart(self):
        """复刻图2：横向柱状图 (sshot-2.png)"""
        print("生成图2 (横向)...")
        
        labels = list(self.dimension_data.keys())
        # 按照截图，可能需要反转顺序让Identity在最上面，取决于字典顺序
        # 这里不做反转，按字典默认顺序绘制
        
        before_vals = [self.dimension_data[k]['before'] for k in labels]
        after_vals = [self.dimension_data[k]['after'] for k in labels]
        
        y = np.arange(len(labels))
        height = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 1. 绘制基准线 (x=1.0)
        ax.axvline(x=1.0, color=BASELINE_COLOR, linestyle='--', linewidth=3, zorder=0)
        
        # 2. 绘制横向柱状图
        # 注意：横向图中，Before通常在下，After在上，或者并排
        ax.barh(y - height/2, before_vals, height, color=COLOR_BEFORE, label='Before', zorder=3)
        ax.barh(y + height/2, after_vals, height, color=COLOR_AFTER, label='After', zorder=3)
        
        # 3. 设置X轴 (范围 0.90 - 1.05)
        ax.set_xlim(0.90, 1.05)
        ax.set_xticks([0.90, 0.95, 1.00, 1.05])
        ax.set_xlabel('Relative Separation (Before = 1.0)', fontsize=24, fontweight='bold', labelpad=15)
        
        # 4. 设置Y轴
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=18, fontweight='normal')
        
        # 应用样式
        self._apply_axis_style(ax)
        
        # 添加极淡的横向网格
        ax.grid(axis='y', which='major', color='#F0F0F0', linewidth=1, zorder=0)
        
        plt.tight_layout()
        plt.savefig('Fig2_Dimension_Separation.pdf', format='pdf', bbox_inches='tight')
        return fig

    def create_all_stability_figures(self):
        fig1 = self.create_stability_metrics_bar_chart()
        fig2 = self.create_dimension_separation_bar_chart()
        plt.show()
        print("图表已生成并保存为 PDF。")

if __name__ == "__main__":
    visualizer = SelfAwarenessStabilityVisualizer()
    visualizer.create_all_stability_figures()