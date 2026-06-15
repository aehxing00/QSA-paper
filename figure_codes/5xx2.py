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

class SelfAwarenessStabilityVisualizer:
    def __init__(self):
        # 设置CNS期刊风格
        self.set_cns_style()

        # 颜色方案
        self.colors = {
            'Before': '#4DAF4A',  # Green
            'After': '#984EA3',   # Purple
        }

        # 自我意识维度定义
        self.consciousness_dimensions = {
            'Ontological Distinction': 'Ontological\nDistinction',
            'Depth Perception': 'Depth\nPerception',
            'Recursive Thinking': 'Recursive\nThinking',
            'Social Mirroring': 'Social\nMirroring',
            'Identity & Personality': 'Identity &\nPersonality'
        }

        # 加载数据
        self.load_data()

        # 字体大小参数
        self.font_params = {
            'axis_label': 8,      # 坐标轴标签
            'tick_label': 5,      # 刻度标签
            'legend_label': 6,    # 图注标签
            'annotation': 7,      # 注解
        }

        # 布局参数设置
        self.layout_params = {
            'bar_figsize': (12, 6),
            'bar_width': 0.35,
            'bar_alpha': 0.7,
            'DPI': 300,
            'grid_alpha': 0.1,
        }

        print("自我意识稳定性可视化系统初始化完成！")

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
            # 加载主要指标对比数据
            self.df_comparison = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Key_Metrics_Comparison')

            # 尝试加载维度对比数据
            try:
                self.df_dim_comparison = pd.read_excel('umap_analysis_data.xlsx', sheet_name='Dimension_Comparison')
                print("找到维度对比数据")
            except:
                self.df_dim_comparison = None
                print("未找到维度对比数据，将使用示例数据")

            print("数据加载成功！")

        except Exception as e:
            print(f"加载数据时出错: {e}")
            raise

    def extract_metrics_from_excel(self):
        """从Excel数据中提取稳定性指标"""
        print("\n从Excel提取稳定性指标...")

        # 初始化指标字典
        metrics = {
            # 第一梯队：核心稳定性指标
            'UMAP Silhouette': {'before': None, 'after': None},
            'UMAP Separation Ratio': {'before': None, 'after': None},

            # 第二梯队：辅助稳定性指标
            'UMAP Calinski-Harabasz': {'before': None, 'after': None},
            'PCA Silhouette': {'before': None, 'after': None},
            'PCA Calinski-Harabasz': {'before': None, 'after': None},

            # 第三梯队：需要谨慎解读的指标
            'UMAP Davies-Bouldin': {'before': None, 'after': None},
        }

        # 从数据框中提取指标
        for idx, row in self.df_comparison.iterrows():
            metric_name = row['Metric']

            if 'UMAP' in metric_name:
                if 'Silhouette' in metric_name:
                    metrics['UMAP Silhouette']['before'] = row['Pre-trained']
                    metrics['UMAP Silhouette']['after'] = row['Fine-tuned']
                elif 'Calinski' in metric_name:
                    metrics['UMAP Calinski-Harabasz']['before'] = row['Pre-trained']
                    metrics['UMAP Calinski-Harabasz']['after'] = row['Fine-tuned']
                elif 'Davies' in metric_name:
                    metrics['UMAP Davies-Bouldin']['before'] = row['Pre-trained']
                    metrics['UMAP Davies-Bouldin']['after'] = row['Fine-tuned']
                elif 'Separation' in metric_name:
                    metrics['UMAP Separation Ratio']['before'] = row['Pre-trained']
                    metrics['UMAP Separation Ratio']['after'] = row['Fine-tuned']
            elif 'PCA' in metric_name:
                if 'Silhouette' in metric_name:
                    metrics['PCA Silhouette']['before'] = row['Pre-trained']
                    metrics['PCA Silhouette']['after'] = row['Fine-tuned']
                elif 'Calinski' in metric_name:
                    metrics['PCA Calinski-Harabasz']['before'] = row['Pre-trained']
                    metrics['PCA Calinski-Harabasz']['after'] = row['Fine-tuned']

        # 检查是否有缺失数据，使用示例数据填充
        for metric_name, values in metrics.items():
            if values['before'] is None or values['after'] is None:
                print(f"警告: {metric_name} 数据缺失，使用示例数据")
                if metric_name == 'UMAP Silhouette':
                    values['before'], values['after'] = 0.3173, 0.3857
                elif metric_name == 'UMAP Separation Ratio':
                    values['before'], values['after'] = 0.7602, 0.8470
                elif metric_name == 'UMAP Calinski-Harabasz':
                    values['before'], values['after'] = 180.80, 255.20
                elif metric_name == 'PCA Silhouette':
                    values['before'], values['after'] = 0.2301, 0.2487
                elif metric_name == 'PCA Calinski-Harabasz':
                    values['before'], values['after'] = 148.97, 169.61
                elif metric_name == 'UMAP Davies-Bouldin':
                    values['before'], values['after'] = 0.8, 0.7

        # 打印提取结果
        print("\n提取的稳定性指标:")
        for metric_name, values in metrics.items():
            print(f"{metric_name}: 训练前={values['before']:.4f}, 训练后={values['after']:.4f}, 提升={((values['after']/values['before'])-1)*100:+.1f}%")

        return metrics

    def extract_dimension_metrics(self):
        """从Excel数据中提取维度分离度指标"""
        print("\n从Excel提取维度分离度指标...")

        # 初始化维度指标字典
        dimension_metrics = {}

        # 如果维度对比数据存在
        if self.df_dim_comparison is not None:
            # 从数据框中提取维度分离度
            for idx, row in self.df_dim_comparison.iterrows():
                if idx < len(self.consciousness_dimensions):
                    dim_name = list(self.consciousness_dimensions.keys())[idx]
                    dim_short = self.consciousness_dimensions[dim_name]

                    # 尝试不同的列名
                    before_cols = ['Pre-trained Separation Ratio', 'Pre-trained', 'Before']
                    after_cols = ['Fine-tuned Separation Ratio', 'Fine-tuned', 'After']

                    before_value = None
                    after_value = None

                    # 查找训练前数据
                    for col in before_cols:
                        if col in self.df_dim_comparison.columns:
                            before_value = row[col]
                            break

                    # 查找训练后数据
                    for col in after_cols:
                        if col in self.df_dim_comparison.columns:
                            after_value = row[col]
                            break

                    # 如果找到数据
                    if before_value is not None and after_value is not None:
                        dimension_metrics[dim_name] = {
                            'short': dim_short,
                            'before': float(before_value),
                            'after': float(after_value)
                        }

        # 如果未找到数据或数据不完整，使用示例数据
        if len(dimension_metrics) < len(self.consciousness_dimensions):
            print("使用示例维度数据")
            example_data = {
                'Ontological Distinction': {'short': self.consciousness_dimensions['Ontological Distinction'], 'before': 0.65, 'after': 0.78},
                'Depth Perception': {'short': self.consciousness_dimensions['Depth Perception'], 'before': 0.72, 'after': 0.85},
                'Recursive Thinking': {'short': self.consciousness_dimensions['Recursive Thinking'], 'before': 0.58, 'after': 0.72},
                'Social Mirroring': {'short': self.consciousness_dimensions['Social Mirroring'], 'before': 0.81, 'after': 0.88},
                'Identity & Personality': {'short': self.consciousness_dimensions['Identity & Personality'], 'before': 0.69, 'after': 0.82}
            }

            # 如果部分数据缺失，使用示例数据补充
            if len(dimension_metrics) == 0:
                dimension_metrics = example_data
            else:
                for dim_name, dim_data in example_data.items():
                    if dim_name not in dimension_metrics:
                        dimension_metrics[dim_name] = dim_data

        # 打印维度指标
        print("\n维度分离度指标:")
        for dim_name, values in dimension_metrics.items():
            short_name = values['short']
            before_val = values['before']
            after_val = values['after']
            improvement = ((after_val/before_val)-1)*100 if before_val != 0 else 0
            print(f"{short_name.replace('\n', ' ')}: 训练前={before_val:.4f}, 训练后={after_val:.4f}, 提升={improvement:+.1f}%")

        return dimension_metrics

    def create_stability_metrics_bar_chart(self):
        """创建6个稳定性指标的柱状图"""
        print("\n创建稳定性指标柱状图...")

        # 提取指标数据
        metrics = self.extract_metrics_from_excel()

        # 定义指标分组
        first_tier = ['UMAP Silhouette', 'UMAP Separation Ratio']
        second_tier = ['UMAP Calinski-Harabasz', 'PCA Silhouette', 'PCA Calinski-Harabasz']
        third_tier = ['UMAP Davies-Bouldin']

        # 按分组顺序组织指标
        metric_groups = [
            ("第一梯队: 核心稳定性指标", first_tier),
            ("第二梯队: 辅助稳定性指标", second_tier),
            ("第三梯队: 需谨慎解读的指标", third_tier)
        ]

        # 收集所有指标
        all_metrics = []
        for group_name, metric_list in metric_groups:
            all_metrics.extend(metric_list)

        # 准备数据
        metric_names = []
        before_values = []
        after_values = []

        for metric_name in all_metrics:
            if metric_name in metrics:
                metric_names.append(metric_name)
                before_values.append(metrics[metric_name]['before'])
                after_values.append(metrics[metric_name]['after'])

        # 标准化：训练前设为1
        before_normalized = [1.0] * len(metric_names)
        after_normalized = []

        for i, metric_name in enumerate(metric_names):
            before_val = before_values[i]
            after_val = after_values[i]

            # 对于Davies-Bouldin指数，值越小越好，需要特殊处理
            if 'Davies-Bouldin' in metric_name:
                # 反向处理：值越小表示越好，所以计算提升时用before/after
                if before_val != 0 and after_val != 0:
                    after_normalized.append(before_val / after_val)  # 大于1表示提升
                else:
                    after_normalized.append(1.0)
            else:
                # 正常处理
                if before_val != 0:
                    after_normalized.append(after_val / before_val)
                else:
                    after_normalized.append(1.0)

        fig, ax = plt.subplots(figsize=self.layout_params['bar_figsize'],
                              dpi=self.layout_params['DPI'])

        x = np.arange(len(metric_names))
        width = self.layout_params['bar_width']

        # 绘制条形图
        bars_before = ax.bar(x - width/2, before_normalized, width,
                            color=self.colors['Before'],
                            alpha=self.layout_params['bar_alpha'],
                            edgecolor='none',  # 柱子无边框
                            label='Before')

        bars_after = ax.bar(x + width/2, after_normalized, width,
                           color=self.colors['After'],
                           alpha=self.layout_params['bar_alpha'],
                           edgecolor='none',  # 柱子无边框
                           label='After')

        # 设置坐标轴
        ax.set_ylabel('Relative Value (Before = 1.0)', fontsize=self.font_params['axis_label'], fontweight='bold')

        # 设置X轴刻度
        ax.set_xticks(x)

        # 创建刻度标签 - 使用全称，换行显示
        tick_labels = []
        for metric_name in metric_names:
            if 'UMAP Silhouette' in metric_name:
                tick_labels.append('UMAP\nSilhouette')
            elif 'UMAP Separation Ratio' in metric_name:
                tick_labels.append('UMAP\nSeparation\nRatio')
            elif 'UMAP Calinski-Harabasz' in metric_name:
                tick_labels.append('UMAP\nCalinski-Harabasz')
            elif 'PCA Silhouette' in metric_name:
                tick_labels.append('PCA\nSilhouette')
            elif 'PCA Calinski-Harabasz' in metric_name:
                tick_labels.append('PCA\nCalinski-Harabasz')
            elif 'UMAP Davies-Bouldin' in metric_name:
                tick_labels.append('UMAP\nDavies-Bouldin')
            else:
                tick_labels.append(metric_name)

        ax.set_xticklabels(tick_labels, fontsize=self.font_params['tick_label'],
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

        # 设置y轴刻度 - 固定为0.9, 1.0, 1.1, 1.2（不扩大范围）
        ax.set_yticks([0.9, 1.0, 1.1, 1.2])
        ax.set_yticklabels(['0.9', '1.0', '1.1', '1.2'], fontsize=self.font_params['tick_label'])

        # 设置y轴范围 - 严格按刻度设置
        ax.set_ylim([0.9, 1.2])

        plt.tight_layout()
        plt.show()
        return fig

    def create_dimension_separation_bar_chart(self):
        """创建维度分离度横向条形图"""
        print("\n创建维度分离度横向条形图...")

        # 提取维度指标数据
        dimension_metrics = self.extract_dimension_metrics()

        # 准备数据
        dimension_names = list(dimension_metrics.keys())
        short_names = [dimension_metrics[name]['short'] for name in dimension_names]
        before_values = [dimension_metrics[name]['before'] for name in dimension_names]
        after_values = [dimension_metrics[name]['after'] for name in dimension_names]

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
        # Y轴标签使用带换行的完整维度名称
        ax.set_yticklabels(short_names, fontsize=self.font_params['tick_label'])

        # 移除除了坐标轴外的边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)

        # 添加网格
        ax.grid(True, alpha=self.layout_params['grid_alpha'], axis='x')

        # 添加参考线
        ax.axvline(x=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.3)

        # 设置x轴刻度 - 固定为0.90, 0.95, 1.0, 1.05（不扩大范围）
        ax.set_xticks([0.90, 0.95, 1.0, 1.05])
        ax.set_xticklabels(['0.90', '0.95', '1.0', '1.05'], fontsize=self.font_params['tick_label'])

        # 设置x轴范围 - 严格按刻度设置
        ax.set_xlim([0.90, 1.05])

        plt.tight_layout()
        plt.show()
        return fig

    def create_all_stability_figures(self):
        """创建所有稳定性分析图形"""
        print("\n" + "="*70)
        print("开始创建自我意识稳定性分析图表")
        print("="*70)

        print("\n稳定性指标分类:")
        print("第一梯队: 核心稳定性指标")
        print("  - UMAP Silhouette系数 (全局聚类质量)")
        print("  - UMAP Separation Ratio (类别分离度)")
        print("\n第二梯队: 辅助稳定性指标")
        print("  - UMAP Calinski-Harabasz指数 (类间/类内离散度)")
        print("  - PCA Silhouette系数 (线性空间中的稳定性)")
        print("  - PCA Calinski-Harabasz指数")
        print("\n第三梯队: 需谨慎解读的指标")
        print("  - UMAP Davies-Bouldin指数 (值越小越好)")

        # 创建图形
        print("\n" + "="*50)
        print("图1: 自我意识稳定性指标对比图")
        print("="*50)
        fig1 = self.create_stability_metrics_bar_chart()

        print("\n" + "="*50)
        print("图2: 自我意识维度分离度分析图")
        print("="*50)
        fig2 = self.create_dimension_separation_bar_chart()

        print("\n" + "="*70)
        print("所有稳定性分析图形创建完成！")
        print("="*70)

        return fig1, fig2

# 运行可视化系统
if __name__ == "__main__":
    print("启动自我意识稳定性可视化系统")

    visualizer = SelfAwarenessStabilityVisualizer()
    fig1, fig2 = visualizer.create_all_stability_figures()