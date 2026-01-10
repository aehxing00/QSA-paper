import json
from collections import defaultdict
from langid import classify
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import numpy as np
import matplotlib.colors as mcolors

# --- 工具函数 ---
def adjust_brightness(color, factor):
    """
    调整颜色亮度
    """
    rgb = mcolors.to_rgb(color)
    return mcolors.to_hex(np.clip([c * factor for c in rgb], 0, 1))

# --- 1. 语言统计函数 ---

def calculate_language_counts(file_path):
    """
    统计 JSONL 文件中 "question" 字段内容的指定语言计数。

    Args:
        file_path (str): JSONL 文件的路径。

    Returns:
        dict: 包含目标语言计数的字典，键为 langid code (e.g., 'en', 'zh')。
    """
    # 定义我们关心的语言及其对应的 langid 库的识别代码，以及它们在绘图数组中的顺序。
    # 绘图代码中的顺序是: English, Chinese, French, Spanish, German, Russian, Japanese, Arabic
    TARGET_LANGS_ORDERED = {
        'en': 'English',
        'zh': 'Chinese',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ar': 'Arabic'
    }

    lang_counts = defaultdict(int)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if not line.strip():
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    # 忽略无效的 JSON 行，或记录到 'error'
                    lang_counts['error_json'] += 1
                    continue

                # 检查 "question" 字段
                if 'question' in data and isinstance(data['question'], str):
                    question_text = data['question'].strip()

                    if not question_text:
                        # 忽略空问题
                        lang_counts['empty_question'] += 1
                        continue

                    # 使用 langid 库进行语言识别
                    lang_code, _ = classify(question_text)

                    # 检查识别出的语言是否在我们的目标列表中
                    if lang_code in TARGET_LANGS_ORDERED:
                        lang_counts[lang_code] += 1
                    else:
                        # 统计非目标语言
                        lang_counts['other'] += 1
                else:
                    # 统计缺少 "question" 字段或字段内容无效的行
                    lang_counts['missing_field'] += 1

    except FileNotFoundError:
        print(f"ERROR: File not found at {file_path}. Please check the path.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during file reading: {e}")
        return None

    return lang_counts

# --- 2. 主执行和绘图部分 ---

def main():
    file_path = 'PandaAIQ.jsonl'

    print(f"--- 1. 正在读取文件并统计语言分布：{file_path} ---")

    # 获取统计结果
    raw_counts = calculate_language_counts(file_path)

    if raw_counts is None:
        print("无法继续绘图，因为文件读取或统计失败。")
        return

    # 定义目标语言及其顺序（必须与绘图代码的labels顺序一致）
    # 绘图代码中的顺序：English, Chinese, French, Spanish, German, Russian, Japanese, Arabic
    languages = ['English', 'Chinese', 'French', 'Spanish', 'German', 'Russian', 'Japanese', 'Arabic']
    lang_codes = ['en', 'zh', 'fr', 'es', 'de', 'ru', 'ja', 'ar']

    # 提取并按顺序构建绘图所需的 counts 列表
    counts = []
    for code in lang_codes:
        # 使用统计结果，如果某个语言没有数据，则计数为 0
        counts.append(raw_counts.get(code, 0))

    # 打印统计概要
    total_for_plot = sum(counts)
    total_processed_lines = sum(raw_counts.values())

    print("\n--- 统计概要 ---")
    print(f"总处理行数 (包括错误/缺失/其他): {total_processed_lines}")
    print(f"用于绘图的有效问题总数 (八种目标语言): {total_for_plot}\n")
    print("目标语言计数 (用于绘图):")
    for lang, count in zip(languages, counts):
        print(f"  {lang:<10}: {count}")

    print(f"\n非目标项统计:")
    for key, count in raw_counts.items():
        if key not in lang_codes:
            print(f"  {key:<20}: {count}")

    # 检查是否有数据可以绘图
    if total_for_plot == 0:
        print("\nWARN: 没有统计到任何目标语言的数据，无法绘制饼图。")
        return

    # --- 2. 绘图部分 (优化精美感和立体感) ---
    print("\n--- 2. 正在生成精美饼图 ---")

    # ========== 可调参数 ==========
    # 字体参数
    LEGEND_TITLE_FONT_SIZE = 15
    LEGEND_FONT_SIZE = 15

    # 图形参数
    FIG_SIZE = (12, 9)
    PIE_RADIUS = 0.7  # 增大饼图
    EXPLODE_MAX = 0.05  # 增加突出效果

    # 颜色参数
    BACKGROUND_COLOR = '#f8f9fa'
    LEGEND_BACKGROUND_COLOR = (1, 1, 1, 0.92)
    LEGEND_EDGE_COLOR = (0.7, 0.7, 0.7, 0.4)
    # =============================

    # 设置全局字体
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.linewidth'] = 0.5

    # Calculate percentages for each language
    percentages = [count / total_for_plot * 100 for count in counts]

    # 使用专业配色方案
    colors = [
        '#2E5A87',  # English - 深蓝色
        '#D46B2D',  # Chinese - 暖橙色
        '#3D8C6E',  # French - 翠绿色
        '#B3423A',  # Spanish - 酒红色
        '#6A5B8C',  # German - 紫灰色
        '#8B6B4C',  # Russian - 咖啡色
        '#C76BA3',  # Japanese - 粉紫色
        '#666666'   # Arabic - 中灰色
    ]

    # 创建图形
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # 设置精美的背景
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    # 定义立体感爆炸效果
    explode = [EXPLODE_MAX * (count / max(counts) if max(counts) > 0 else 0) ** 0.3 for count in counts]

    # 绘制具有立体感效果的饼图（取消百分比显示）
    wedges, texts = ax.pie(
        counts,
        explode=explode,
        colors=colors,
        startangle=90,
        wedgeprops={
            'edgecolor': 'white',
            'linewidth': 2.5,
            'linestyle': '-',
            'alpha': 0.9,
            'antialiased': True,
        },
        autopct=None,  # 取消百分比显示
        radius=PIE_RADIUS,
        frame=False
    )

    # 增强立体感效果
    for i, wedge in enumerate(wedges):
        # 添加内阴影和光泽效果
        wedge.set_path_effects([
            patheffects.withSimplePatchShadow(
                offset=(2, -2),
                alpha=0.15,
                rho=8
            ),
            patheffects.withStroke(linewidth=1.5, foreground='white', alpha=0.3)
        ])

    # 确保饼图是圆形
    ax.axis('equal')

    # 创建图例标签 - 使用Arial字体
    legend_labels = [f'{lang}: {perc:.1f}%' for lang, perc in zip(languages, percentages)]

    # 创建精美的图例框 - 稍微下移位置
    legend = ax.legend(
        wedges, legend_labels,
        title="Language Distribution",
        title_fontsize=LEGEND_TITLE_FONT_SIZE,
        loc="upper center",
        bbox_to_anchor=(0.5, 0),  # 稍微下移：从0.1改为0.08
        ncol=2,
        fontsize=LEGEND_FONT_SIZE,
        frameon=True,
        fancybox=True,
        shadow=True,
        framealpha=0.9,
        edgecolor=LEGEND_EDGE_COLOR,
        facecolor=LEGEND_BACKGROUND_COLOR,
        borderpad=1.2,
        labelspacing=1.1
    )

    # 美化图例标题 - 使用Arial字体
    legend_title = legend.get_title()
    legend_title.set_fontweight('bold')
    legend_title.set_color('#2c3e50')
    legend_title.set_fontsize(LEGEND_TITLE_FONT_SIZE + 1)
    legend_title.set_family('Arial')

    # 美化图例文本 - 使用Arial字体，改为粗体
    for text in legend.get_texts():
        text.set_color('#34495e')
        text.set_fontweight('bold')  # 改为粗体
        text.set_family('Arial')

    # 移除坐标轴
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 调整布局
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])

    # 添加水印效果
    ax.text(0.5, 0.5, '',
            transform=ax.transAxes,
            fontsize=40,
            alpha=0.03,
            ha='center',
            va='center',
            fontweight='bold',
            rotation=30,
            family='Arial')

    plt.show()

if __name__ == "__main__":
    main()