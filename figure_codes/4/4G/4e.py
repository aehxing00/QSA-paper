import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

# 全局字体样式
plt.rcParams.update({
    'font.size': 14,
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold'
})

# 创建渐变色背景函数
def create_gradient_background(ax):
    r = np.linspace(0, 1, 100)
    theta = np.linspace(0, 2*np.pi, 100)
    R, Theta = np.meshgrid(r, theta)
    cmap = LinearSegmentedColormap.from_list('custom', ['#e6f7ff', '#003366'])
    ax.pcolormesh(Theta, R, R, cmap=cmap, shading='auto', alpha=0.3)

# 定义大类映射关系
CATEGORY_MAPPING = {
    '1': 'Ontological Distinction',
    '2': 'Depth Perception', 
    '3': 'Recursive Thinking',
    '4': 'Social Mirroring',
    '5': 'Identity & Personality'
}

# 子项到大类的映射
SUBCATEGORY_MAPPING = {
    '1A': '1', '1B': '1', '1C': '1',
    '2A': '2', '2B': '2', '2C': '2', 
    '3A': '3', '3B': '3', '3C': '3',
    '4A': '4', '4B': '4', '4C': '4',
    '5A': '5', '5B': '5', '5C': '5'
}

def process_data(df):
    """处理数据，将子项合并为大类并计算平均值"""
    # 获取第一列（子项名称）
    subcategories = df.iloc[:, 0].tolist()
    
    # 创建大类数据框架
    category_data = {}
    
    # 处理每个模型的数据（从第二列开始）
    model_columns = []
    current_model = None
    model_data_cols = []
    
    # 识别模型和对应的5列数据
    for col_idx in range(1, len(df.columns)):
        col_name = df.columns[col_idx]
        
        # 如果遇到新模型名称或者到达第5列的倍数
        if len(model_data_cols) == 0 or len(model_data_cols) == 5:
            if current_model and model_data_cols:
                model_columns.append((current_model, model_data_cols))
            current_model = col_name
            model_data_cols = [col_idx]
        else:
            model_data_cols.append(col_idx)
    
    # 添加最后一个模型
    if current_model and model_data_cols:
        model_columns.append((current_model, model_data_cols))
    
    # 处理每个模型的数据
    for model_name, col_indices in model_columns:
        category_means = {}
        
        # 为每个大类初始化数据
        for category in ['1', '2', '3', '4', '5']:
            category_means[category] = []
        
        # 收集每个子项的数据并归类
        for row_idx, subcat in enumerate(subcategories):
            subcat_key = subcat.strip().split()[0]  # 获取1A, 1B等
            if subcat_key in SUBCATEGORY_MAPPING:
                category = SUBCATEGORY_MAPPING[subcat_key]
                
                # 计算该子项在5次测定中的平均值
                subcat_values = []
                for col_idx in col_indices:
                    value = df.iloc[row_idx, col_idx]
                    if pd.notna(value) and isinstance(value, (int, float)):
                        subcat_values.append(value)
                
                if subcat_values:
                    subcat_mean = np.mean(subcat_values)
                    # 不再自动转换为百分比，保持原始值
                    category_means[category].append(subcat_mean)
        
        # 计算每个大类的平均值
        final_means = []
        for category in ['1', '2', '3', '4', '5']:
            if category_means[category]:
                category_mean = np.mean(category_means[category])
                final_means.append(category_mean)
            else:
                final_means.append(0)
        
        category_data[model_name] = final_means
    
    return category_data

def generate_radar_chart():
    while True:
        input_filename = "a3.xlsx"  # 固定文件名
        
        try:
            df = pd.read_excel(input_filename)

            if df.empty:
                print(f"警告: 文件 '{input_filename}' 为空或无法正确读取。")
                continue

            base_filename = os.path.splitext(input_filename)[0]
            output_image_name = base_filename + ".png"

            # 处理数据
            category_data = process_data(df)
            
            # 只取前2个模型进行比较
            models_to_plot = list(category_data.keys())[:2]
            
            if len(models_to_plot) < 2:
                print("错误: 需要至少2个模型的数据进行比较。")
                continue

            # 雷达图类别（5个大类）
            categories = [CATEGORY_MAPPING[str(i)] for i in range(1, 6)]
            N = len(categories)
            angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
            angles += angles[:1]

            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(111, polar=True)

            create_gradient_background(ax)

            ax.set_theta_offset(np.pi/2)
            ax.set_theta_direction(-1)
            ax.set_rlabel_position(0)
            
            # 修改雷达图范围为0-0.15
            ax.set_ylim(0, 0.6)
            ax.set_yticks([0, 0.2, 0.4, 0.6])
            ax.set_yticklabels(["0", "0.2", "0.4", "0.6"],
                               fontsize=12,
                               weight='bold',
                               color='#333333')

            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            line_styles = ['-', '--', '-.', ':']

            # 绘制每个模型的数据
            for idx, model_name in enumerate(models_to_plot):
                values = category_data[model_name]
                values += values[:1]  # 闭合雷达图

                current_color = colors[idx % len(colors)]
                current_linestyle = line_styles[idx % len(line_styles)]

                ax.plot(angles, values, color=current_color,
                        linestyle=current_linestyle,
                        linewidth=3,
                        label=model_name)
                ax.fill(angles, values, color=current_color, alpha=0.15)

            # 设置类别标签
            ax.set_xticks(angles[:-1])
            xtick_labels = [label.replace(' ', '\n') for label in categories]
            ax.set_xticklabels(xtick_labels,
                               fontsize=13,
                               weight='bold',
                               verticalalignment='center',
                               horizontalalignment='center',
                               color='#333333')

            for tick_label in ax.get_xticklabels():
                tick_label.set_va('center')
                tick_label.set_position((tick_label.get_position()[0], tick_label.get_position()[1] - 0.05))
            ax.tick_params(axis='x', pad=25)

            # 图例
            legend = ax.legend(loc='upper right',
                               bbox_to_anchor=(1.55, 1.3),
                               frameon=True,
                               edgecolor='#2f4f4f',
                               fontsize=12,
                               title='Models',
                               title_fontsize='13')
            legend.get_frame().set_alpha(0.9)
            legend.get_frame().set_facecolor('#f9f9f9')

            plt.tight_layout(pad=3.0)

            plt.savefig(output_image_name,
                        bbox_inches='tight',
                        dpi=300,
                        transparent=True)
            print(f"雷达图已保存为: {output_image_name}")
            plt.show()
            plt.close(fig)

        except FileNotFoundError:
            print(f"错误: 文件 '{input_filename}' 未找到。请检查文件名和路径。")
        except pd.errors.EmptyDataError:
            print(f"错误: 文件 '{input_filename}' 为空。")
        except Exception as e:
            print(f"处理文件 '{input_filename}' 时发生错误: {e}")
            if 'fig' in locals() and plt.fignum_exists(fig.number): # type: ignore
                 plt.close(fig) # type: ignore

        another = input("是否要制作下一个图表? (yes/no): ").strip().lower()
        if another != 'yes':
            print("退出程序。")
            break

if __name__ == '__main__':
    generate_radar_chart()