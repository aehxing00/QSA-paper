import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D  # 需要导入 Line2D 来手动构建图注
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

class CNS_Figure_Generator_V2:
    def __init__(self):
        # ==================== 1. 全局样式设置 (复刻 Nature/Science 风格) ====================
        # 字体设置：Arial
        plt.rcParams['font.family'] = 'Arial'
        # 关键：设置 PDF 字体类型为 42 (TrueType)，确保导出后文字可编辑
        plt.rcParams['pdf.fonttype'] = 42
        plt.rcParams['ps.fonttype'] = 42
        
        # 线条与刻度
        plt.rcParams['axes.linewidth'] = 0.8        # 边框粗细
        plt.rcParams['xtick.major.width'] = 0.8     # 刻度粗细
        plt.rcParams['ytick.major.width'] = 0.8
        plt.rcParams['xtick.direction'] = 'out'     # 刻度朝外
        plt.rcParams['ytick.direction'] = 'out'
        
        # 颜色方案 (从图片提取的近似色)
        self.colors = {
            'Self-Prompts': '#E64B35',      # 红色
            'Baseline-Prompts': '#4DBBD5',  # 蓝色
        }
        
        # 字体大小配置 (精确参考图片)
        self.font_config = {
            'label_size': 16,       # 坐标轴标题 (如 PC 1) - 粗体
            'tick_size': 14,        # 刻度数字
            'legend_size': 14,      # 【新增】图注字体大小
            'weight': 'bold'       # 字体加粗
        }
        
        # 布局配置
        # 【修改点1】图片变得更窄，适应排版
        self.fig_size = (4, 4) # 宽 x 高 (英寸)，更窄的比例
        
        # 散点样式
        self.marker_size = 15      # 散点大小
        self.marker_alpha = 0.75   # 透明度
        self.edge_width = 0.3      # 散点白色描边宽度

        # 加载或生成数据
        self.load_or_generate_data()

    def load_or_generate_data(self):
        """加载数据，如果文件不存在则生成模拟数据以供演示"""
        try:
            # 请确保您的目录下有这个文件，否则会生成模拟数据
            self.df_before_umap = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Before_UMAP')
            self.df_after_umap = pd.read_excel('umap_analysis_data.xlsx', sheet_name='After_UMAP')
            try:
                self.df_before_pca = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Before_PCA')
                self.df_after_pca = pd.read_excel('umap_analysis_data.xlsx', sheet_name='After_PCA')
            except:
                self._generate_dummy_pca()
            print("数据加载成功")
        except FileNotFoundError:
            print("未找到数据文件，生成模拟数据用于演示图表效果...")
            self._generate_dummy_data()

    def _generate_dummy_data(self):
        """生成模拟数据结构"""
        np.random.seed(42)
        n_points = 200
        
        # 生成 PCA 模拟数据 (两个类别的分布)
        def make_blob(center, scale, label):
            data = np.random.normal(loc=center, scale=scale, size=(n_points // 2, 2))
            return pd.DataFrame({'PCA1': data[:,0], 'PCA2': data[:,1], 'Category': label})

        # Before: 混合较多
        pca_b1 = make_blob([0, 0], 10, 'Self-Prompts')
        pca_b2 = make_blob([5, 5], 10, 'Baseline-Prompts')
        self.df_before_pca = pd.concat([pca_b1, pca_b2])
        
        # After: 分离较好
        pca_a1 = make_blob([-10, -5], 8, 'Self-Prompts')
        pca_a2 = make_blob([15, 10], 8, 'Baseline-Prompts')
        self.df_after_pca = pd.concat([pca_a1, pca_a2])

        # UMAP 模拟数据
        self.df_before_umap = self.df_before_pca.rename(columns={'PCA1': 'UMAP1', 'PCA2': 'UMAP2'})
        self.df_after_umap = self.df_after_pca.rename(columns={'PCA1': 'UMAP1', 'PCA2': 'UMAP2'})

    def _generate_dummy_pca(self):
        self.df_before_pca = self.df_before_umap.rename(columns={'UMAP1': 'PCA1', 'UMAP2': 'PCA2'})
        self.df_after_pca = self.df_after_umap.rename(columns={'UMAP1': 'PCA1', 'UMAP2': 'PCA2'})

    def plot_scatter_comparison(self, df_left, df_right, x_col, y_col, xlabel, ylabel, filename):
        """绘制双面板散点图 (复刻图c和d，带图注，更窄)"""
        
        # 创建画布，共享 Y 轴和 X 轴
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.fig_size, dpi=300, 
                                     sharey=True, sharex=True)
        
        # 统一坐标轴范围
        all_x = pd.concat([df_left[x_col], df_right[x_col]])
        all_y = pd.concat([df_left[y_col], df_right[y_col]])
        x_padding = (all_x.max() - all_x.min()) * 0.1
        y_padding = (all_y.max() - all_y.min()) * 0.1
        xlims = (all_x.min() - x_padding, all_x.max() + x_padding)
        ylims = (all_y.min() - y_padding, all_y.max() + y_padding)

        # 辅助绘图函数
        def draw_scatter(ax, df):
            # 绘制 Baseline (蓝色)
            mask_base = df['Category'] == 'Baseline-Prompts'
            ax.scatter(df.loc[mask_base, x_col], df.loc[mask_base, y_col],
                       c=self.colors['Baseline-Prompts'],
                       s=self.marker_size, alpha=self.marker_alpha,
                       edgecolors='white', linewidths=self.edge_width)
            
            # 绘制 Self-Prompts (红色) - 放在上层
            mask_self = df['Category'] == 'Self-Prompts'
            ax.scatter(df.loc[mask_self, x_col], df.loc[mask_self, y_col],
                       c=self.colors['Self-Prompts'],
                       s=self.marker_size, alpha=self.marker_alpha,
                       edgecolors='white', linewidths=self.edge_width)

            # 设置网格 (极淡)
            ax.grid(True, linestyle='-', alpha=0.1, color='gray')
            
            # 设置坐标轴范围
            ax.set_xlim(xlims)
            ax.set_ylim(ylims)
            
            # 设置刻度字体
            ax.tick_params(axis='both', which='major', labelsize=self.font_config['tick_size'])

        # 绘制左右子图
        draw_scatter(ax1, df_left)
        draw_scatter(ax2, df_right)

        # 设置坐标轴标签 (加粗 Arial 8pt)
        # 只在左图显示 Y 轴标签， labelpad 减小以适应窄图
        ax1.set_ylabel(ylabel, fontsize=self.font_config['label_size'], fontweight='bold', labelpad=1)
        # 两个图都显示 X 轴标签
        ax1.set_xlabel(xlabel, fontsize=self.font_config['label_size'], fontweight='bold', labelpad=1)
        ax2.set_xlabel(xlabel, fontsize=self.font_config['label_size'], fontweight='bold', labelpad=1)

        # 【修改点2】添加图注 (Legend)
        # 手动创建图注元素，以确保样式与散点完全一致（包括透明度和描边）
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Self-Prompts',
                   markerfacecolor=self.colors['Self-Prompts'], markersize=5,
                   markeredgecolor='white', markeredgewidth=self.edge_width, alpha=self.marker_alpha),
            Line2D([0], [0], marker='o', color='w', label='Baseline-Prompts',
                   markerfacecolor=self.colors['Baseline-Prompts'], markersize=5,
                   markeredgecolor='white', markeredgewidth=self.edge_width, alpha=self.marker_alpha)
        ]
        
        # 将图注放置在图像正上方，无边框，水平排列
        fig.legend(handles=legend_elements, 
                   loc='lower center', 
                   bbox_to_anchor=(0.55, 0.92), # 调整位置到顶部居中略偏上
                   ncol=2,                      # 水平排列
                   frameon=False,               # 无边框
                   fontsize=self.font_config['legend_size'],
                   handletextpad=0.1, columnspacing=1.0)

        # 调整布局间距 (紧凑版)
        # top 留出空间给图注，bottom 留出空间给 X 轴标签
        plt.subplots_adjust(wspace=0.05, bottom=0.22, left=0.16, right=0.98, top=0.88)
        
        # 保存
        plt.savefig(f"{filename}.pdf", format='pdf', bbox_inches='tight')
        plt.savefig(f"{filename}.png", format='png', dpi=300, bbox_inches='tight')
        print(f"图表已保存: {filename}.pdf (矢量图, 窄版带图注)")

    def create_all_figures(self):
        print("\n=== 开始生成 CNS 风格矢量图 (窄版带图注) ===")
        
        # 1. 生成图 c (PCA Analysis)
        self.plot_scatter_comparison(
            self.df_before_pca, 
            self.df_after_pca, 
            x_col='PCA1', y_col='PCA2', 
            xlabel='PC 1', ylabel='PC 2', 
            filename='Fig_c_PCA_Analysis_Narrow'
        )

        # 2. 生成图 d (UMAP Analysis)
        self.plot_scatter_comparison(
            self.df_before_umap, 
            self.df_after_umap, 
            x_col='UMAP1', y_col='UMAP2', 
            xlabel='UMAP 1', ylabel='UMAP 2', 
            filename='Fig_d_UMAP_Analysis_Narrow'
        )

if __name__ == "__main__":
    generator = CNS_Figure_Generator_V2()
    generator.create_all_figures()