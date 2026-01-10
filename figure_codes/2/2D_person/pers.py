import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# 1. 样式配置 (保持 2A.jpg 的全框、粗线条风格)
# ==========================================
STYLE_CONFIG = {
    # 字体设置
    'font_family': 'Arial',
    'font_weight': 'bold',
    'font_size_tick': 14,        # 刻度数字大小
    'font_size_ylabel': 18,      # Y轴标题大小
    
    # 线条设置 (粗犷风格，仿马克笔质感)
    'axes_linewidth': 2.5,       # 边框粗细
    'tick_length': 8,            # 刻度线长度
    'tick_width': 2.5,           # 刻度线粗细
    
    # 配色 (高饱和度对比色)
    'palette': ['#4C8CDE', '#F59D56', '#67BF5C', '#AF8CD3', '#EE94AC'],
    
    # 箱体与散点
    'box_width': 0.6,
    'point_size': 6,
}

def main():
    input_file = 'panda_detailed_scores.xlsx'
    
    try:
        # --- 数据处理 (逻辑不变) ---
        print("正在处理数据...")
        df = pd.read_excel(input_file)
        
        results = []
        for i in range(1, df.shape[1], 4):
            subset = df.iloc[:, i : i+4]
            if subset.shape[1] < 4: break
            model_name = subset.columns[0]
            corr_matrix = subset.corr(method='pearson')
            vals = [
                corr_matrix.iloc[0, 1], corr_matrix.iloc[0, 2], corr_matrix.iloc[0, 3],
                corr_matrix.iloc[1, 2], corr_matrix.iloc[1, 3], corr_matrix.iloc[2, 3]
            ]
            results.append([model_name] + vals)
        
        cols = ['Model Name', 'Corr_1_2', 'Corr_1_3', 'Corr_1_4', 'Corr_2_3', 'Corr_2_4', 'Corr_3_4']
        df_results = pd.DataFrame(results, columns=cols)
        df_plot = df_results.melt(id_vars=['Model Name'], var_name='Pair', value_name='Correlation')

        # --- 绘图部分 ---
        
        # 全局字体与线宽设定
        plt.rcParams['font.family'] = STYLE_CONFIG['font_family']
        plt.rcParams['font.weight'] = STYLE_CONFIG['font_weight']
        plt.rcParams['axes.linewidth'] = STYLE_CONFIG['axes_linewidth']
        
        fig, ax = plt.subplots(figsize=(10, 6.5)) # 稍微增加高度给倾斜的标签

        # 1. 绘制箱线图
        sns.boxplot(x='Model Name', y='Correlation', data=df_plot,
                    width=STYLE_CONFIG['box_width'],
                    linewidth=STYLE_CONFIG['axes_linewidth'], 
                    palette=STYLE_CONFIG['palette'],
                    showfliers=False,
                    ax=ax,
                    boxprops=dict(edgecolor='black', alpha=1.0), 
                    whiskerprops=dict(color='black'),
                    capprops=dict(color='black'),
                    medianprops=dict(color='black', linewidth=2.5),
                    zorder=1)

        # 2. 绘制散点图
        sns.stripplot(x='Model Name', y='Correlation', data=df_plot,
                      color='#404040',
                      s=STYLE_CONFIG['point_size'],
                      alpha=0.8,
                      jitter=0.2,
                      linewidth=1.0, 
                      edgecolor='white',
                      ax=ax,
                      zorder=2)

        # 3. 坐标轴深度定制
        
        # 刻度设置：朝外，加粗
        ax.tick_params(axis='both', which='major', 
                       direction='out', 
                       length=STYLE_CONFIG['tick_length'], 
                       width=STYLE_CONFIG['tick_width'], 
                       colors='black',
                       pad=6,
                       labelsize=STYLE_CONFIG['font_size_tick'])
        
        # 强制显示四周边框 (全框风格)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(STYLE_CONFIG['axes_linewidth'])

        # 横向网格线
        ax.yaxis.grid(True, linestyle='-', which='major', color='#E0E0E0', linewidth=1.5, alpha=0.6, zorder=0)

        # 轴标题
        ax.set_ylabel("Pearson Correlation", fontsize=STYLE_CONFIG['font_size_ylabel'], fontweight='bold', labelpad=12)
        ax.set_xlabel("") # 移除底部标题

        # Y轴范围与刻度
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_ylim(-0.02, 1.05)

        # --- 关键修改：X轴标签旋转 45度 ---
        # ha='right' (Horizontal Alignment) 保证文字尾部对齐刻度，防止文字悬空
        plt.xticks(rotation=45, ha='right', fontweight='bold')

        # 自动调整布局，防止标签被切掉
        plt.tight_layout()
        
        print("绘图完成，正在弹出窗口...")
        plt.show()

    except FileNotFoundError:
        print("错误：未找到 panda_detailed_scores.xlsx 文件")
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    main()