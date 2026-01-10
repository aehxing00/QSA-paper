import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ==========================================
# 1. 样式配置
# ==========================================
# 关键设置：确保导出的 SVG 文本在矢量软件中可编辑
plt.rcParams['svg.fonttype'] = 'none'

STYLE_CONFIG = {
    # 字体设置 - 确保使用 Arial
    'font_family': 'Arial',
    'font_size_tick': 24,       # 坐标轴刻度字号
    'font_size_label': 27,      # X轴标签字号
    'font_size_ylabel': 32,     # Y轴标题字号

    # 线条设置
    'axes_linewidth': 3.0,
    'tick_length': 8,
    'tick_width': 3.0,

    # 配色
    'palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#d62728'],

    # 箱体与散点
    'box_width': 0.5,
    'point_size': 7,
}

def main():
    input_file = 'panda_detailed_scores.xlsx'
    # 修改点 1: 修改输出文件名后缀为 .svg
    output_file = 'panda_pearson_correlation.svg'

    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        return

    try:
        # --- 数据处理 ---
        print("正在处理数据...")
        df = pd.read_excel(input_file)

        results = []
        for i in range(1, df.shape[1], 4):
            subset = df.iloc[:, i : i+4]
            if subset.shape[1] < 4: break

            model_name = subset.columns[0]
            try:
                corr_matrix = subset.corr(method='pearson')
                vals = [
                    corr_matrix.iloc[0, 1], corr_matrix.iloc[0, 2], corr_matrix.iloc[0, 3],
                    corr_matrix.iloc[1, 2], corr_matrix.iloc[1, 3], corr_matrix.iloc[2, 3]
                ]
                results.append([model_name] + vals)
            except Exception:
                print(f"跳过模型 {model_name}")

        if not results:
            print("没有提取到有效数据。")
            return

        cols = ['Model Name', 'Corr_1_2', 'Corr_1_3', 'Corr_1_4', 'Corr_2_3', 'Corr_2_4', 'Corr_3_4']
        df_results = pd.DataFrame(results, columns=cols)
        df_plot = df_results.melt(id_vars=['Model Name'], var_name='Pair', value_name='Correlation')

        # --- 绘图配置 ---

        # 1. 全局字体设定为 Arial
        plt.rcParams['font.family'] = STYLE_CONFIG['font_family']
        plt.rcParams['axes.labelweight'] = 'bold' 

        # 2. 创建画布
        fig, ax = plt.subplots(figsize=(10, 6))

        # 3. 绘制箱线图
        sns.boxplot(x='Model Name', y='Correlation', data=df_plot,
                    width=STYLE_CONFIG['box_width'],
                    linewidth=2.5,
                    palette=STYLE_CONFIG['palette'],
                    showfliers=False,
                    ax=ax,
                    boxprops=dict(edgecolor='black', alpha=1.0),
                    whiskerprops=dict(color='black', linewidth=2.5),
                    capprops=dict(color='black', linewidth=2.5),
                    medianprops=dict(color='black', linewidth=2.5),
                    zorder=1)

        # 4. 绘制散点图
        sns.stripplot(x='Model Name', y='Correlation', data=df_plot,
                      color='#404040',
                      s=STYLE_CONFIG['point_size'],
                      alpha=0.9,
                      jitter=0.15,
                      linewidth=1.2,
                      edgecolor='white',
                      ax=ax,
                      zorder=2)

        # --- 坐标轴定制 ---

        # 刻度设置
        ax.tick_params(axis='both', which='major',
                       direction='out',
                       length=STYLE_CONFIG['tick_length'],
                       width=STYLE_CONFIG['tick_width'],
                       colors='black',
                       pad=8,
                       labelsize=STYLE_CONFIG['font_size_tick'])

        # 边框设置
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(STYLE_CONFIG['axes_linewidth'])
        ax.spines['bottom'].set_linewidth(STYLE_CONFIG['axes_linewidth'])

        # 横向网格线 (保持极淡风格)
        ax.yaxis.grid(True, linestyle='-', which='major', color='#E0E0E0', linewidth=2, alpha=0.6, zorder=0)

        # 轴标题
        ax.set_ylabel("Pearson Correlation", fontsize=STYLE_CONFIG['font_size_ylabel'], fontweight='bold', labelpad=15)
        ax.set_xlabel("")

        # Y轴范围与刻度
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'])
        ax.set_ylim(-0.05, 1.05)

        # X轴标签
        ax.set_xticklabels(ax.get_xticklabels(),
                           rotation=45,
                           ha='right',
                           fontsize=STYLE_CONFIG['font_size_label'],
                           fontweight='normal',
                           fontfamily=STYLE_CONFIG['font_family'])

        # --- 修改点 2: 保存为 SVG ---
        print(f"正在保存为 {output_file} ...")
        plt.savefig(output_file, format='svg', bbox_inches='tight')
        print("保存成功！")

    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    main()