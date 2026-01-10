import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

# 全局字体样式 (保持不变)
plt.rcParams.update({
    'font.size': 14,
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold'
})

# 创建渐变色背景函数 (保持不变)
def create_gradient_background(ax):
    r = np.linspace(0, 1, 100)
    theta = np.linspace(0, 2*np.pi, 100)
    R, Theta = np.meshgrid(r, theta)
    cmap = LinearSegmentedColormap.from_list('custom', ['#e6f7ff', '#003366'])
    ax.pcolormesh(Theta, R, R, cmap=cmap, shading='auto', alpha=0.3)

def generate_radar_chart():
    while True:
        input_filename = input("请输入Excel文件名称 (例如: model_data.xlsx): ")
        if not input_filename.lower().endswith(".xlsx"):
            print("错误：文件必须是 .xlsx 格式。请重新输入。")
            continue

        try:
            df = pd.read_excel(input_filename)

            if df.empty:
                print(f"警告: 文件 '{input_filename}' 为空或无法正确读取。")
                continue

            base_filename = os.path.splitext(input_filename)[0]
            output_image_name = base_filename + ".png"

            if df.shape[1] < 2:
                print(f"错误: 文件 '{input_filename}' 需要至少两列 (一列模型名称，至少一列指标数据)。")
                continue

            categories = df.columns[1:].tolist()
            N = len(categories)
            angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
            angles += angles[:1]

            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(111, polar=True)

            create_gradient_background(ax)

            ax.set_theta_offset(np.pi/2)
            ax.set_theta_direction(-1)
            ax.set_rlabel_position(0)
            ax.set_ylim(0, 100)
            ax.set_yticks([0, 25, 50, 75, 100])
            ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"],
                               fontsize=12,
                               weight='bold',
                               color='#333333')

            numeric_cols = df.iloc[:, 1:].select_dtypes(include=np.number).columns
            if not numeric_cols.empty:
                for col in numeric_cols:
                    if df[col].max() <= 1 and df[col].max() > 0:
                         df[col] = df[col] * 100
            else:
                print(f"警告: 在文件 '{input_filename}' 中未找到用于缩放的数值型数据列。")

            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            line_styles = ['-', '--', '-.', ':']

            for idx, row_data in df.iterrows():
                model_name = str(row_data.iloc[0])
                values_series = pd.to_numeric(row_data.iloc[1:], errors='coerce').fillna(0)
                values = values_series.tolist()

                if len(values) < N:
                    values.extend([0] * (N - len(values)))
                elif len(values) > N:
                    values = values[:N]

                values += values[:1]

                current_color = colors[idx % len(colors)]
                current_linestyle = line_styles[idx % len(line_styles)]

                ax.plot(angles, values, color=current_color,
                        linestyle=current_linestyle,
                        linewidth=3,
                        label=model_name)
                ax.fill(angles, values, color=current_color, alpha=0.15)

            ax.set_xticks(angles[:-1])
            xtick_labels = [str(label).replace(' ', '\n') for label in categories]
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

            # --- 图片标题已被取消 ---
            # plt.title(f"Model Performance: {base_filename}",
            #           pad=60,
            #           fontsize=20,
            #           fontweight='black',
            #           color='#1a1a1a')

            legend = ax.legend(loc='upper right',
                               bbox_to_anchor=(1.55, 1.3),
                               frameon=True,
                               edgecolor='#2f4f4f',
                               fontsize=12,
                               title='Models', # 您也可以通过设置 title='' 来移除图例标题
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