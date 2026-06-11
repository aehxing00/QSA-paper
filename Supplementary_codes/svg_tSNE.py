import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

class CNS_Figure_Generator_SVG:
    def __init__(self):
        # ==================== 1. 全局样式设置 (复刻 CNS 风格) ====================
        plt.rcParams['font.family'] = 'Arial'
        # 关键：设置 SVG 字体不转为路径，保持文字可编辑
        plt.rcParams['svg.fonttype'] = 'none'

        # 线条与刻度
        plt.rcParams['axes.linewidth'] = 1.0        # 边框粗细
        plt.rcParams['xtick.major.width'] = 1.0     # 刻度粗细
        plt.rcParams['ytick.major.width'] = 1.0
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'

        # 颜色方案
        self.colors = {
            'Self-Prompts': '#E64B35',      # 红色
            'Baseline-Prompts': '#4DBBD5',  # 蓝色
        }

        # 字体大小配置
        self.font_config = {
            'label_size': 16,
            'tick_size': 14,
            'legend_size': 14,
            'weight': 'bold'
        }

        # 布局配置
        self.fig_size = (4, 4)

        # 散点样式
        self.marker_size = 20
        self.marker_alpha = 0.85
        self.edge_width = 0.5

        # 加载数据
        self.load_or_generate_data()

    def load_or_generate_data(self):
        """加载数据，如果文件不存在则生成模拟数据"""
        try:
            # 【最小修改】UMAP → tSNE
            self.df_before_tsne = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Before_tSNE')
            self.df_after_tsne = pd.read_excel('umap_analysis_data.xlsx', sheet_name='After_tSNE')
            self.df_before_pca = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Before_PCA')
            self.df_after_pca = pd.read_excel('umap_analysis_data.xlsx', sheet_name='After_PCA')
        except Exception:
            # 文件不存在时生成模拟数据
            np.random.seed(42)
            n_points = 200
            def make_blob(center, scale, label):
                data = np.random.normal(loc=center, scale=scale, size=(n_points // 2, 2))
                return pd.DataFrame({'X': data[:,0], 'Y': data[:,1], 'Category': label})

            self.df_before_pca = pd.concat([make_blob([0, 0], 10, 'Self-Prompts'),
                                           make_blob([5, 5], 10, 'Baseline-Prompts')]).rename(columns={'X':'PCA1','Y':'PCA2'})
            self.df_after_pca = pd.concat([make_blob([-10, -5], 8, 'Self-Prompts'),
                                          make_blob([15, 10], 8, 'Baseline-Prompts')]).rename(columns={'X':'PCA1','Y':'PCA2'})
            # 【最小修改】UMAP → tSNE、列名 UMAP1/UMAP2 → tSNE1/tSNE2
            self.df_before_tsne = self.df_before_pca.rename(columns={'PCA1': 'tSNE1', 'PCA2': 'tSNE2'})
            self.df_after_tsne = self.df_after_pca.rename(columns={'PCA1': 'tSNE1', 'PCA2': 'tSNE2'})

    def plot_scatter_comparison(self, df_left, df_right, x_col, y_col, xlabel, ylabel, filename):
        """绘制双面板散点图并保存为 SVG"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.fig_size, dpi=300,
                                     sharey=True, sharex=True, facecolor='white')

        # --- 核心修复部分：统一坐标轴范围 ---
        all_x = pd.concat([df_left[x_col], df_right[x_col]])
        all_y = pd.concat([df_left[y_col], df_right[y_col]])

        # 替代 ptp() 的兼容写法
        x_range = all_x.max() - all_x.min()
        y_range = all_y.max() - all_y.min()

        # 防止数据点单一导致 range 为 0
        x_range = x_range if x_range != 0 else 1.0
        y_range = y_range if y_range != 0 else 1.0

        xlims = (all_x.min() - (x_range * 0.1), all_x.max() + (x_range * 0.1))
        ylims = (all_y.min() - (y_range * 0.1), all_y.max() + (y_range * 0.1))

        def draw_scatter(ax, df):
            # 1. 绘制 Baseline
            mask_base = df['Category'] == 'Baseline-Prompts'
            ax.scatter(df.loc[mask_base, x_col], df.loc[mask_base, y_col],
                       c=self.colors['Baseline-Prompts'], s=self.marker_size,
                       alpha=self.marker_alpha, edgecolors='white', linewidths=self.edge_width, zorder=2)

            # 2. 绘制 Self-Prompts (zorder=3 确保在上方)
            mask_self = df['Category'] == 'Self-Prompts'
            ax.scatter(df.loc[mask_self, x_col], df.loc[mask_self, y_col],
                       c=self.colors['Self-Prompts'], s=self.marker_size,
                       alpha=self.marker_alpha, edgecolors='white', linewidths=self.edge_width, zorder=3)

            ax.grid(True, linestyle='-', alpha=0.1, color='#AAAAAA', zorder=1)
            ax.set_xlim(xlims)
            ax.set_ylim(ylims)

            # 强制坐标轴与刻度为纯黑
            for spine in ax.spines.values():
                spine.set_edgecolor('#000000')
            ax.tick_params(axis='both', colors='#000000', labelsize=self.font_config['tick_size'])

        draw_scatter(ax1, df_left)
        draw_scatter(ax2, df_right)

        # 轴标签加粗 (Arial, 纯黑)
        ax1.set_ylabel(ylabel, fontsize=self.font_config['label_size'], fontweight='bold', color='#000000')
        ax1.set_xlabel(xlabel, fontsize=self.font_config['label_size'], fontweight='bold', color='#000000')
        ax2.set_xlabel(xlabel, fontsize=self.font_config['label_size'], fontweight='bold', color='#000000')

        # 手动创建图注 (Legend)
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Self-Prompts',
                   markerfacecolor=self.colors['Self-Prompts'], markersize=8,
                   markeredgecolor='white', markeredgewidth=0.5),
            Line2D([0], [0], marker='o', color='w', label='Baseline-Prompts',
                   markerfacecolor=self.colors['Baseline-Prompts'], markersize=8,
                   markeredgecolor='white', markeredgewidth=0.5)
        ]

        fig.legend(handles=legend_elements,
                   loc='lower center',
                   bbox_to_anchor=(0.55, 0.92),
                   ncol=2, frameon=False,
                   fontsize=self.font_config['legend_size'],
                   prop={'family': 'Arial', 'weight': 'bold', 'size': self.font_config['legend_size']})

        # 调整子图间距
        plt.subplots_adjust(wspace=0.1, bottom=0.2, left=0.15, right=0.95, top=0.85)

        # 保存为 SVG
        svg_filename = f"{filename}.svg"
        plt.savefig(svg_filename, format='svg', bbox_inches='tight')
        plt.savefig(f"{filename}_preview.png", dpi=300, bbox_inches='tight')
        print(f"✅ 成功! 矢量图已保存为: {svg_filename}")

    def create_all_figures(self):
        self.plot_scatter_comparison(self.df_before_pca, self.df_after_pca, 'PCA1', 'PCA2', 'PC 1', 'PC 2', 'Fig_PCA_SVG')
        # 【最小修改】UMAP → tSNE：变量、列名、轴标签、输出文件名
        self.plot_scatter_comparison(self.df_before_tsne, self.df_after_tsne, 'tSNE1', 'tSNE2', 'tSNE 1', 'tSNE 2', 'Fig_tSNE_SVG')

if __name__ == "__main__":
    generator = CNS_Figure_Generator_SVG()
    generator.create_all_figures()