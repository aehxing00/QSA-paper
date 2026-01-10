import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
from nltk.util import ngrams

# ============================ 1. 超参数配置区 (可自由调节) ============================
# 字体大小
AXIS_LABEL_SIZE = 20     # Y轴标题字体大小
TICK_LABEL_SIZE = 18      # 刻度数字/名称字体大小
THRESHOLD_FONT_SIZE = 18  # 阈值标注文字大小

# 阈值标注位置 (坐标基于数据刻度)
THRESHOLD_VAL = 5.0      # 红色虚线高度
THRESHOLD_TEXT_X = 4.2   # 阈值文字所在的X轴位置 (0对应第1个柱子，以此类推)
THRESHOLD_TEXT_Y = 5.1   # 阈值文字所在的Y轴高度

# 图表布局
FIG_SIZE = (3.5, 4)      # 图像尺寸 (英寸)，适合单栏排版
BAR_WIDTH = 0.55         # 柱子宽度
XTICK_ROTATION = 45      # X轴刻度倾斜角度
Y_TICKS = [0, 1, 2, 3, 4, 5]
Y_LIMIT = 6.0            # 为了给阈值文字留出顶部空间，略微调高上限

# 配色
COLOR_PALETTE = "Blues_r" # 蓝色系渐变

# 字体强制设置 (Arial)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['pdf.fonttype'] = 42  # 确保导出PDF时字体可编辑

# ============================ 2. 数据处理逻辑 ============================
def tokenize_hybrid(text):
    text = re.sub(r'([\u4e00-\u9fa5])', r' \1 ', text)
    return [t.lower() for t in text.split() if t.strip()]

def load_data(file_path, is_train=True):
    texts = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            data = json.loads(line)
            content = f"{data.get('instruction', '')} {data.get('output', '')}" if is_train else f"{data.get('question', '')} {' '.join(data.get('options', []))}"
            texts.append(content)
    return " ".join(texts)

def calculate_overlap_data(train_file, test_file, max_n=5):
    train_tokens = tokenize_hybrid(load_data(train_file, is_train=True))
    test_tokens = tokenize_hybrid(load_data(test_file, is_train=False))
    results = []
    for n in range(1, max_n + 1):
        train_ng = set(ngrams(train_tokens, n))
        test_ng = set(ngrams(test_tokens, n))
        intersection = train_ng.intersection(test_ng)
        overlap_ratio = (len(intersection) / len(test_ng)) * 100 if test_ng else 0
        results.append({"N": f"{n}-Gram", "Ratio": overlap_ratio})
    return pd.DataFrame(results)

# ============================ 3. 绘图执行 ============================
TRAIN_SET, TEST_SET = "tr_61.jsonl", "PandaAIQ.jsonl"

try:
    df = calculate_overlap_data(TRAIN_SET, TEST_SET)

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    # 绘制柱状图
    colors = sns.color_palette(COLOR_PALETTE, n_colors=len(df))
    bars = ax.bar(df['N'], df['Ratio'], color=colors, 
                  edgecolor='black', linewidth=0.75, width=BAR_WIDTH)
    
    # 阈值水平虚线
    ax.axhline(y=THRESHOLD_VAL, color='red', linestyle='--', linewidth=0.8, alpha=0.9)
    
    # 
    # 阈值文字标注 (位置由超参数 THRESHOLD_TEXT_X/Y 控制)
    ax.text(THRESHOLD_TEXT_X, THRESHOLD_TEXT_Y, f'Threshold ({int(THRESHOLD_VAL)}%)', 
            color='red', fontsize=THRESHOLD_FONT_SIZE, fontname='Arial',
            ha='right', fontweight='bold')
    
    # 坐标轴细节设置
    ax.set_ylabel('Overlap Ratio (%)', fontsize=AXIS_LABEL_SIZE, fontname='Arial')
    ax.set_xlabel('', visible=False) # 彻底取消X轴名称
    
    # X轴刻度倾斜设置
    ax.set_xticklabels(df['N'], rotation=XTICK_ROTATION, ha='right', fontsize=TICK_LABEL_SIZE)
    
    # Y轴刻度设置
    ax.set_yticks(Y_TICKS)
    ax.set_ylim(0, Y_LIMIT)
    ax.tick_params(axis='y', labelsize=TICK_LABEL_SIZE)
    
    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 导出矢量图
    plt.tight_layout()
    plt.savefig("Contamination_Final_Nature_Style.svg", format='svg', transparent=True)
    print("✅ 绘图成功！")
    print(f"配置文件: SVG格式, Arial字体, {XTICK_ROTATION}度倾斜, 阈值位置({THRESHOLD_TEXT_X}, {THRESHOLD_TEXT_Y})")
    plt.show()

except Exception as e:
    print(f"❌ 运行失败: {e}")