import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

class FinalVisualizerV2:
    def __init__(self):
        # 设置CNS期刊风格
        self.set_cns_style()
        
        # 颜色方案
        self.colors = {
            'Self-Prompts': '#E41A1C',  # Red
            'Baseline-Prompts': '#377EB8',  # Blue
            'Before': '#4DAF4A',  # Green
            'After': '#984EA3',   # Purple
        }
        
        # 自我意识维度定义
        self.consciousness_dimensions = {
            'Ontological Distinction': {
                'short': 'Ontological',
                'subdimensions': ['Boundary Sense', 'Self-Awareness', 'Subjectivity']
            },
            'Depth Perception': {
                'short': 'Depth',
                'subdimensions': ['Multimodal Integration', 'World Model', 'Embodiment']
            },
            'Recursive Thinking': {
                'short': 'Recursive',
                'subdimensions': ['Recursive Reflection', 'Metacognition', 'Error Correction']
            },
            'Social Mirroring': {
                'short': 'Social',
                'subdimensions': ['Mirroring Others', 'Role Understanding', 'Interactional Synchrony']
            },
            'Identity & Personality': {
                'short': 'Identity',
                'subdimensions': ['Time Perception', 'Desire & Purpose', 'Core Personality']
            }
        }
        
        # 加载数据
        self.load_data()
        
        # 字体大小参数（比原来减少2-4个字号）
        self.font_params = {
            'axis_label': 8,      # 坐标轴标签：10->8（减少2）
            'tick_label': 5,      # 刻度标签：8->5（减少3）
            'legend_label': 6,    # 图注标签：10->6（减少4）
            'annotation': 7,      # 注解：9->7（减少2）
        }
        
        # 布局参数设置
        self.layout_params = {
            # 点状图参数
            'scatter_figsize': (10, 6),
            'scatter_marker_size': 30,
            'scatter_alpha': 0.6,
            'scatter_edge_width': 0.5,
            
            # 条形图参数
            'bar_figsize': (12, 6),
            'bar_width': 0.35,
            'bar_alpha': 0.7,
            
            # 通用参数
            'DPI': 300,
            'grid_alpha': 0.1,
        }
        
        print("最终版可视化系统V2初始化完成！")
    
    def set_cns_style(self):
        """设置CNS期刊风格"""
        plt.rcParams.update({
            'font.family': 'Arial',
            'font.size': 8,
            'figure.dpi': 300,
            'axes.linewidth': 0.8,
            'axes.grid': True,
            'grid.linewidth': 0.2,
            'grid.alpha': 0.1,
            'xtick.major.width': 0.6,
            'ytick.major.width': 0.6,
        })
    
    def load_data(self):
        """从Excel文件加载数据"""
        print("正在加载数据...")
        
        try:
            self.df_before_umap = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Before_UMAP')
            self.df_after_umap = pd.read_excel('umap_analysis_data.xlsx', sheet_name='After_UMAP')
            self.df_comparison = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Key_Metrics_Comparison')
            
            # 尝试加载PCA数据
            try:
                self.df_before_pca = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Before_PCA')
                self.df_after_pca = pd.read_excel('umap_analysis_data.xlsx', sheet_name='After_PCA')
                print("找到PCA数据")
            except:
                print("未找到PCA数据，将计算PCA")
                self.df_before_pca = None
                self.df_after_pca = None
                
            try:
                self.df_dim_comparison = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Dimension_Comparison')
                print("找到维度对比数据")
            except:
                self.df_dim_comparison = None
                print("未找到维度对比数据")
                
            print("数据加载成功！")
            
        except Exception as e:
            print(f"加载数据时出错: {e}")
            raise
    
    def create_umap_scatter_separate(self):
        """创建独立的UMAP点状分布图（有完整边框）"""
        print("\n创建独立的UMAP点状分布图...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.layout_params['scatter_figsize'], 
                                      dpi=self.layout_params['DPI'])
        
        # ========== 训练前UMAP ==========
        self_prompts_mask_before = self.df_before_umap['Category'] == 'Self-Prompts'
        baseline_prompts_mask_before = self.df_before_umap['Category'] == 'Baseline-Prompts'
        
        ax1.scatter(self.df_before_umap.loc[self_prompts_mask_before, 'UMAP1'],
                   self.df_before_umap.loc[self_prompts_mask_before, 'UMAP2'],
                   c=self.colors['Self-Prompts'], 
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        ax1.scatter(self.df_before_umap.loc[baseline_prompts_mask_before, 'UMAP1'],
                   self.df_before_umap.loc[baseline_prompts_mask_before, 'UMAP2'],
                   c=self.colors['Baseline-Prompts'],
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        # ========== 训练后UMAP ==========
        self_prompts_mask_after = self.df_after_umap['Category'] == 'Self-Prompts'
        baseline_prompts_mask_after = self.df_after_umap['Category'] == 'Baseline-Prompts'
        
        ax2.scatter(self.df_after_umap.loc[self_prompts_mask_after, 'UMAP1'],
                   self.df_after_umap.loc[self_prompts_mask_after, 'UMAP2'],
                   c=self.colors['Self-Prompts'], 
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        ax2.scatter(self.df_after_umap.loc[baseline_prompts_mask_after, 'UMAP1'],
                   self.df_after_umap.loc[baseline_prompts_mask_after, 'UMAP2'],
                   c=self.colors['Baseline-Prompts'],
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        # ========== 设置UMAP图 ==========
        # 统一两个子图的坐标轴范围，确保大小一致
        all_umap1 = pd.concat([self.df_before_umap['UMAP1'], self.df_after_umap['UMAP1']])
        all_umap2 = pd.concat([self.df_before_umap['UMAP2'], self.df_after_umap['UMAP2']])
        
        x_min, x_max = all_umap1.min(), all_umap1.max()
        y_min, y_max = all_umap2.min(), all_umap2.max()
        
        # 添加5%的边距
        x_margin = (x_max - x_min) * 0.05
        y_margin = (y_max - y_min) * 0.05
        
        for ax in [ax1, ax2]:
            ax.set_xlabel('UMAP 1', fontsize=self.font_params['axis_label'], fontweight='bold')
            ax.set_ylabel('UMAP 2', fontsize=self.font_params['axis_label'], fontweight='bold')
            ax.grid(True, alpha=self.layout_params['grid_alpha'])
            ax.set_aspect('equal', adjustable='box')
            # 统一坐标轴范围
            ax.set_xlim([x_min - x_margin, x_max + x_margin])
            ax.set_ylim([y_min - y_margin, y_max + y_margin])
        
        # 隐藏第二张图的Y轴刻度数字
        ax2.set_ylabel('')
        ax2.set_yticklabels([])
        
        plt.tight_layout()
        plt.show()
        return fig
    
    def create_pca_scatter_separate(self):
        """创建独立的PCA点状分布图（有完整边框）"""
        print("\n创建独立的PCA点状分布图...")
        
        # 如果没有PCA数据，计算PCA
        if self.df_before_pca is None or self.df_after_pca is None:
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler
            
            scaler = StandardScaler()
            
            # 训练前PCA
            X_before = self.df_before_umap[['UMAP1', 'UMAP2']].values
            X_before_scaled = scaler.fit_transform(X_before)
            pca_before = PCA(n_components=2, random_state=42)
            pca_result_before = pca_before.fit_transform(X_before_scaled)
            
            # 训练后PCA
            X_after = self.df_after_umap[['UMAP1', 'UMAP2']].values
            X_after_scaled = scaler.fit_transform(X_after)
            pca_after = PCA(n_components=2, random_state=42)
            pca_result_after = pca_after.fit_transform(X_after_scaled)
        else:
            pca_result_before = self.df_before_pca[['PCA1', 'PCA2']].values
            pca_result_after = self.df_after_pca[['PCA1', 'PCA2']].values
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.layout_params['scatter_figsize'], 
                                      dpi=self.layout_params['DPI'])
        
        # 获取类别掩码
        self_prompts_mask_before = self.df_before_umap['Category'] == 'Self-Prompts'
        baseline_prompts_mask_before = self.df_before_umap['Category'] == 'Baseline-Prompts'
        self_prompts_mask_after = self.df_after_umap['Category'] == 'Self-Prompts'
        baseline_prompts_mask_after = self.df_after_umap['Category'] == 'Baseline-Prompts'
        
        # ========== 训练前PCA ==========
        ax1.scatter(pca_result_before[self_prompts_mask_before, 0],
                   pca_result_before[self_prompts_mask_before, 1],
                   c=self.colors['Self-Prompts'], 
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        ax1.scatter(pca_result_before[baseline_prompts_mask_before, 0],
                   pca_result_before[baseline_prompts_mask_before, 1],
                   c=self.colors['Baseline-Prompts'],
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        # ========== 训练后PCA ==========
        ax2.scatter(pca_result_after[self_prompts_mask_after, 0],
                   pca_result_after[self_prompts_mask_after, 1],
                   c=self.colors['Self-Prompts'], 
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        ax2.scatter(pca_result_after[baseline_prompts_mask_after, 0],
                   pca_result_after[baseline_prompts_mask_after, 1],
                   c=self.colors['Baseline-Prompts'],
                   s=self.layout_params['scatter_marker_size'],
                   alpha=self.layout_params['scatter_alpha'],
                   edgecolors='white',
                   linewidth=self.layout_params['scatter_edge_width'])
        
        # ========== 设置PCA图 ==========
        # 统一两个子图的坐标轴范围，确保大小一致
        all_pca1 = np.concatenate([pca_result_before[:, 0], pca_result_after[:, 0]])
        all_pca2 = np.concatenate([pca_result_before[:, 1], pca_result_after[:, 1]])
        
        x_min, x_max = all_pca1.min(), all_pca1.max()
        y_min, y_max = all_pca2.min(), all_pca2.max()
        
        # 添加5%的边距
        x_margin = (x_max - x_min) * 0.05
        y_margin = (y_max - y_min) * 0.05
        
        for ax in [ax1, ax2]:
            ax.set_xlabel('PC 1', fontsize=self.font_params['axis_label'], fontweight='bold')
            ax.set_ylabel('PC 2', fontsize=self.font_params['axis_label'], fontweight='bold')
            ax.grid(True, alpha=self.layout_params['grid_alpha'])
            # 统一坐标轴范围
            ax.set_xlim([x_min - x_margin, x_max + x_margin])
            ax.set_ylim([y_min - y_margin, y_max + y_margin])
        
        # 隐藏第二张图的Y轴刻度数字
        ax2.set_ylabel('')
        ax2.set_yticklabels([])
        
        plt.tight_layout()
        plt.show()
        return fig
    
    def create_umap_bar_chart_simple(self):
        """创建简化的UMAP指标条形图"""
        print("\n创建UMAP指标条形图...")
        
        # 提取UMAP指标
        umap_metrics = []
        umap_before = []
        umap_after = []
        
        for idx, row in self.df_comparison.iterrows():
            metric_name = row['Metric']
            if 'UMAP' in metric_name:
                if 'Silhouette' in metric_name:
                    umap_metrics.append('Silhouette')
                    umap_before.append(row['Pre-trained'])
                    umap_after.append(row['Fine-tuned'])
                elif 'Calinski' in metric_name:
                    umap_metrics.append('Calinski-Harabasz')
                    umap_before.append(row['Pre-trained'])
                    umap_after.append(row['Fine-tuned'])
                elif 'Davies' in metric_name:
                    umap_metrics.append('Davies-Bouldin')
                    umap_before.append(row['Pre-trained'])
                    umap_after.append(row['Fine-tuned'])
                elif 'Separation' in metric_name:
                    umap_metrics.append('Separation Ratio')
                    umap_before.append(row['Pre-trained'])
                    umap_after.append(row['Fine-tuned'])
        
        if not umap_metrics:
            print("使用示例UMAP数据")
            umap_metrics = ['Silhouette', 'Calinski-Harabasz', 'Davies-Bouldin', 'Separation Ratio']
            umap_before = [0.3173, 180.80, 0.8, 0.7602]
            umap_after = [0.3857, 255.20, 0.7, 0.8470]
        
        # 标准化：训练前设为1
        umap_before_normalized = [1.0] * len(umap_metrics)
        umap_after_normalized = [after/before if before != 0 else 0 
                                for after, before in zip(umap_after, umap_before)]
        
        fig, ax = plt.subplots(figsize=self.layout_params['bar_figsize'], 
                              dpi=self.layout_params['DPI'])
        
        x = np.arange(len(umap_metrics))
        width = self.layout_params['bar_width']
        
        # 绘制条形图
        bars_before = ax.bar(x - width/2, umap_before_normalized, width,
                            color=self.colors['Before'],
                            alpha=self.layout_params['bar_alpha'],
                            edgecolor='none',  # 柱子无边框
                            label='Before')
        
        bars_after = ax.bar(x + width/2, umap_after_normalized, width,
                           color=self.colors['After'],
                           alpha=self.layout_params['bar_alpha'],
                           edgecolor='none',  # 柱子无边框
                           label='After')
        
        # 设置坐标轴
        # 取消X轴标题（根据要求）
        # ax.set_xlabel('UMAP Metrics', fontsize=self.font_params['axis_label'], fontweight='bold')
        
        # Y轴标题减小2个字号
        ax.set_ylabel('Relative Value (Before = 1.0)', fontsize=self.font_params['axis_label'] - 2, fontweight='bold')
        
        # 柱子名称45度倾斜
        ax.set_xticks(x)
        ax.set_xticklabels(umap_metrics, fontsize=self.font_params['tick_label'], 
                          rotation=45, ha='right')
        
        # 移除除了坐标轴外的边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        
        # 添加网格
        ax.grid(True, alpha=self.layout_params['grid_alpha'], axis='y')
        
        # 添加参考线
        ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.3)
        
        # 设置y轴范围
        max_value = max(max(umap_after_normalized), 1.0) * 1.3
        ax.set_ylim([0, max_value])
        
        plt.tight_layout()
        plt.show()
        return fig
    
    def create_pca_bar_chart_simple(self):
        """创建简化的PCA指标条形图"""
        print("\n创建PCA指标条形图...")
        
        # 提取PCA指标
        pca_metrics = []
        pca_before = []
        pca_after = []
        
        for idx, row in self.df_comparison.iterrows():
            metric_name = row['Metric']
            if 'PCA' in metric_name:
                if 'Silhouette' in metric_name:
                    pca_metrics.append('Silhouette')
                    pca_before.append(row['Pre-trained'])
                    pca_after.append(row['Fine-tuned'])
                elif 'Calinski' in metric_name:
                    pca_metrics.append('Calinski-Harabasz')
                    pca_before.append(row['Pre-trained'])
                    pca_after.append(row['Fine-tuned'])
        
        if not pca_metrics:
            print("使用示例PCA数据")
            pca_metrics = ['Silhouette', 'Calinski-Harabasz']
            pca_before = [0.2301, 148.97]
            pca_after = [0.2487, 169.61]
        
        # 标准化：训练前设为1
        pca_before_normalized = [1.0] * len(pca_metrics)
        pca_after_normalized = [after/before if before != 0 else 0 
                               for after, before in zip(pca_after, pca_before)]
        
        fig, ax = plt.subplots(figsize=self.layout_params['bar_figsize'], 
                              dpi=self.layout_params['DPI'])
        
        x = np.arange(len(pca_metrics))
        width = self.layout_params['bar_width']
        
        # 绘制条形图
        bars_before = ax.bar(x - width/2, pca_before_normalized, width,
                            color=self.colors['Before'],
                            alpha=self.layout_params['bar_alpha'],
                            edgecolor='none',  # 柱子无边框
                            label='Before')
        
        bars_after = ax.bar(x + width/2, pca_after_normalized, width,
                           color=self.colors['After'],
                           alpha=self.layout_params['bar_alpha'],
                           edgecolor='none',  # 柱子无边框
                           label='After')
        
        # 设置坐标轴
        # 取消X轴标题（根据要求）
        # ax.set_xlabel('PCA Metrics', fontsize=self.font_params['axis_label'], fontweight='bold')
        
        # Y轴标题减小2个字号
        ax.set_ylabel('Relative Value (Before = 1.0)', fontsize=self.font_params['axis_label'] - 2, fontweight='bold')
        
        # 柱子名称45度倾斜
        ax.set_xticks(x)
        ax.set_xticklabels(pca_metrics, fontsize=self.font_params['tick_label'], 
                          rotation=45, ha='right')
        
        # 移除除了坐标轴外的边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        
        # 添加网格
        ax.grid(True, alpha=self.layout_params['grid_alpha'], axis='y')
        
        # 添加参考线
        ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.3)
        
        # 设置y轴范围
        max_value = max(max(pca_after_normalized), 1.0) * 1.3
        ax.set_ylim([0, max_value])
        
        plt.tight_layout()
        plt.show()
        return fig
    
    def create_combined_horizontal_bar_simple(self):
        """创建简化的合并横向条形图"""
        print("\n创建合并横向条形图...")
        
        # 定义要显示的指标
        metrics_data = [
            {'name': 'UMAP Silhouette', 'before': 0.3173, 'after': 0.3857},
            {'name': 'UMAP Calinski-Harabasz', 'before': 180.80, 'after': 255.20},
            {'name': 'UMAP Separation Ratio', 'before': 0.7602, 'after': 0.8470},
            {'name': 'PCA Silhouette', 'before': 0.2301, 'after': 0.2487},
            {'name': 'PCA Calinski-Harabasz', 'before': 148.97, 'after': 169.61},
        ]
        
        # 从数据中更新（如果存在）
        for metric in metrics_data:
            for idx, row in self.df_comparison.iterrows():
                if metric['name'] in row['Metric']:
                    metric['before'] = row['Pre-trained']
                    metric['after'] = row['Fine-tuned']
                    break
        
        # 标准化：训练前设为1
        metric_names = [m['name'] for m in metrics_data]
        before_values = [1.0] * len(metrics_data)
        after_values = [m['after']/m['before'] if m['before'] != 0 else 0 for m in metrics_data]
        
        fig, ax = plt.subplots(figsize=(14, 8), dpi=self.layout_params['DPI'])
        
        y = np.arange(len(metric_names))
        height = 0.35
        
        # 绘制横向条形图
        bars_before = ax.barh(y - height/2, before_values, height,
                             color=self.colors['Before'],
                             alpha=self.layout_params['bar_alpha'],
                             edgecolor='none',  # 柱子无边框
                             label='Before')
        
        bars_after = ax.barh(y + height/2, after_values, height,
                            color=self.colors['After'],
                            alpha=self.layout_params['bar_alpha'],
                            edgecolor='none',  # 柱子无边框
                            label='After')
        
        # 设置坐标轴
        ax.set_xlabel('Relative Performance (Before = 1.0)', fontsize=self.font_params['axis_label'] - 2, fontweight='bold')
        
        ax.set_yticks(y)
        # Y轴标签字号减少3个号
        ax.set_yticklabels(metric_names, fontsize=self.font_params['tick_label'])
        
        # 移除除了坐标轴外的边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        
        # 添加网格
        ax.grid(True, alpha=self.layout_params['grid_alpha'], axis='x')
        
        # 添加参考线
        ax.axvline(x=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.3)
        
        # 设置x轴范围
        max_x = max(max(after_values), 1.0) * 1.2
        ax.set_xlim([0, max_x])
        
        plt.tight_layout()
        plt.show()
        return fig
    
    def create_dimension_horizontal_bar_simple(self):
        """创建简化的维度分析横向条形图"""
        print("\n创建维度分析横向条形图...")
        
        # 创建示例数据（如果没有实际数据）
        if self.df_dim_comparison is None:
            print("使用示例维度数据")
            dimension_names = list(self.consciousness_dimensions.keys())
            short_names = [self.consciousness_dimensions[name]['short'] for name in dimension_names]
            before_values = [0.65, 0.72, 0.58, 0.81, 0.69]
            after_values = [0.78, 0.85, 0.72, 0.88, 0.82]
        else:
            # 使用实际数据
            dimension_names = list(self.consciousness_dimensions.keys())[:len(self.df_dim_comparison)]
            short_names = [self.consciousness_dimensions[name]['short'] for name in dimension_names]
            before_values = self.df_dim_comparison['Pre-trained Separation Ratio'].values[:5]
            after_values = self.df_dim_comparison['Fine-tuned Separation Ratio'].values[:5]
        
        # 标准化：训练前设为1
        before_normalized = [1.0] * len(dimension_names)
        after_normalized = [after/before if before != 0 else 0 
                           for after, before in zip(after_values, before_values)]
        
        fig, ax = plt.subplots(figsize=(14, 8), dpi=self.layout_params['DPI'])
        
        y = np.arange(len(dimension_names))
        height = 0.35
        
        # 绘制横向条形图
        bars_before = ax.barh(y - height/2, before_normalized, height,
                             color=self.colors['Before'],
                             alpha=self.layout_params['bar_alpha'],
                             edgecolor='none',  # 柱子无边框
                             label='Before')
        
        bars_after = ax.barh(y + height/2, after_normalized, height,
                            color=self.colors['After'],
                            alpha=self.layout_params['bar_alpha'],
                            edgecolor='none',  # 柱子无边框
                            label='After')
        
        # 设置坐标轴
        ax.set_xlabel('Relative Separation (Before = 1.0)', fontsize=self.font_params['axis_label'] - 2, fontweight='bold')
        
        ax.set_yticks(y)
        # Y轴标签字号减少3个号
        ax.set_yticklabels(short_names, fontsize=self.font_params['tick_label'])
        
        # 在下方的位置显示完整名称
        for i, dim_name in enumerate(dimension_names):
            ax.text(-0.05, i, dim_name, 
                   ha='right', va='center',
                   fontsize=self.font_params['annotation'], fontstyle='italic', alpha=0.7,
                   transform=ax.get_yaxis_transform())
        
        # 移除除了坐标轴外的边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        
        # 添加网格
        ax.grid(True, alpha=self.layout_params['grid_alpha'], axis='x')
        
        # 添加参考线
        ax.axvline(x=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.3)
        
        # 设置x轴范围
        max_x = max(max(after_normalized), 1.0) * 1.3
        ax.set_xlim([0, max_x])
        
        plt.tight_layout()
        plt.show()
        return fig
    
    def print_font_settings(self):
        """打印字体设置"""
        print("\n" + "="*60)
        print("字体大小设置（比原来减少2-4个字号）")
        print("="*60)
        print(f"坐标轴标签: {self.font_params['axis_label']}pt (原10)")
        print(f"刻度标签: {self.font_params['tick_label']}pt (原8)")
        print(f"图注标签: {self.font_params['legend_label']}pt (原10，减少4)")
        print(f"注解文字: {self.font_params['annotation']}pt (原9)")
        print("="*60)
    
    def create_all_figures_v2(self):
        """创建所有V2版图形"""
        print("\n" + "="*70)
        print("开始创建V2版专业图表")
        print("="*70)
        
        # 打印字体设置
        self.print_font_settings()
        
        print("\n特点总结:")
        print("✓ UMAP和PCA分别独立弹出")
        print("✓ 点状图有完整边框")
        print("✓ 条形图除了坐标轴没有边框")
        print("✓ 柱子名称45度倾斜")
        print("✓ 字体大小统一减小")
        print("✓ 取消所有图注（用户手动添加）")
        
        # 创建各个图形
        print("\n" + "="*50)
        print("图1: 独立的UMAP点状分布图（有完整边框）")
        print("="*50)
        fig1 = self.create_umap_scatter_separate()
        
        print("\n" + "="*50)
        print("图2: 独立的PCA点状分布图（有完整边框）")
        print("="*50)
        fig2 = self.create_pca_scatter_separate()
        
        print("\n" + "="*50)
        print("图3: UMAP指标条形图（无边框）")
        print("="*50)
        fig3 = self.create_umap_bar_chart_simple()
        
        print("\n" + "="*50)
        print("图4: PCA指标条形图（无边框）")
        print("="*50)
        fig4 = self.create_pca_bar_chart_simple()
        
        print("\n" + "="*50)
        print("图5: 合并指标横向条形图（无边框）")
        print("="*50)
        fig5 = self.create_combined_horizontal_bar_simple()
        
        print("\n" + "="*50)
        print("图6: 维度分析横向条形图（无边框）")
        print("="*50)
        fig6 = self.create_dimension_horizontal_bar_simple()
        
        print("\n" + "="*70)
        print("所有图形创建完成！")
        print("="*70)
        print("\n图形列表:")
        print("1. UMAP Scatter Plot (with full frame)")
        print("2. PCA Scatter Plot (with full frame)")
        print("3. UMAP Metrics Bar Chart")
        print("4. PCA Metrics Bar Chart")
        print("5. Combined Metrics Horizontal Bar Chart")
        print("6. Dimension Analysis Horizontal Bar Chart")
        print("="*70)

# 运行最终版可视化
if __name__ == "__main__":
    print("启动V2版CNS风格可视化系统")
    
    visualizer = FinalVisualizerV2()
    visualizer.create_all_figures_v2()