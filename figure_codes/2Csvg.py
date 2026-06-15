import os
import re
import jieba
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import font_manager
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors
from matplotlib.patches import Circle

# ==========================================
# 1. 样式与矢量配置
# ==========================================
plt.rcParams['svg.fonttype'] = 'none'  # 关键：确保 SVG 文字可编辑
plt.rcParams['font.family'] = 'Arial'

CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 1500
FIG_WIDTH_INCH = 8
FIG_HEIGHT_INCH = 6

# 精确换算因子
CALCULATED_DPI = CANVAS_WIDTH / FIG_WIDTH_INCH  
FONT_SCALE_FACTOR = 72 / CALCULATED_DPI  

def get_arial_font_path():
    candidates = [
        "C:/Windows/Fonts/arialuni.ttf", 
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/Library/Fonts/Arial.ttf"
    ]
    for f in candidates:
        if os.path.exists(f): return f
    return None

def create_academic_colormap():
    colors = ['#0D47A1', '#1565C0', '#00695C', '#B71C1C', '#4A148C', '#0277BD']
    return mcolors.LinearSegmentedColormap.from_list('cns_academic', colors, N=256)

def get_panda_geometry():
    """回归最初 PDF 的完美比例"""
    w, h = CANVAS_WIDTH, CANVAS_HEIGHT
    cx, cy = w // 2, int(h * 0.55)
    head_r = int(h * 0.42)
    ear_r = int(head_r * 0.42)
    ear_off_x = int(head_r * 0.75)
    ear_off_y = int(head_r * 0.70)
    return {
        'head': (cx, cy, head_r),
        'left_ear': (cx - ear_off_x, cy - ear_off_y, ear_r),
        'right_ear': (cx + ear_off_x, cy - ear_off_y, ear_r)
    }

def create_mask(geo):
    mask = np.ones((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=np.uint8) * 255
    y, x = np.ogrid[:CANVAS_HEIGHT, :CANVAS_WIDTH]
    def add_circle_mask(cx, cy, r):
        mask[(x - cx)**2 + (y - cy)**2 <= r**2] = 0
    add_circle_mask(*geo['head'])
    add_circle_mask(*geo['left_ear'])
    add_circle_mask(*geo['right_ear'])
    return mask

def draw_vector_background(ax, geo):
    """最初 PDF 的分层背景绘图"""
    C_SHADOW = '#F5F5F5' 
    C_STROKE = '#CFD8DC' 
    C_FILL = '#FFFFFF'
    def plot_part(cx, cy, r, z_shadow, z_body):
        ax.add_patch(Circle((cx + 12, cy + 12), r, facecolor=C_SHADOW, edgecolor=None, zorder=z_shadow))
        ax.add_patch(Circle((cx, cy), r, facecolor=C_FILL, edgecolor=C_STROKE, linewidth=1.5, zorder=z_body))
    plot_part(*geo['left_ear'], 5, 6)
    plot_part(*geo['right_ear'], 5, 6)
    plot_part(*geo['head'], 10, 11)

def process_data(filename):
    if not os.path.exists(filename): return None, None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [json.loads(line)['question'] for line in f if line.strip()]
            text = " ".join(lines)
    except: return None, None
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', text)
    words = jieba.cut(text)
    stopwords = set(STOPWORDS) | {'的', '了', '在', '是', '我', '有', '和', '就', '不'}
    return " ".join(words), stopwords

# 修复后的颜色转换函数
def format_color(color):
    """安全地将各种格式的颜色转换为十六进制字符串"""
    try:
        if isinstance(color, str) and color.startswith('rgb'):
            # 处理 'rgb(r, g, b)' 格式
            vals = [int(x) for x in re.findall(r'\d+', color)]
            return '#{:02x}{:02x}{:02x}'.format(*vals)
        elif isinstance(color, (tuple, list, np.ndarray)):
            # 处理 (r, g, b) 元组
            if any(val > 1.0 for val in color):
                color = [val/255.0 for val in color]
            return mcolors.to_hex(color)
        return color # 如果已经是 hex 字符串则直接返回
    except:
        return '#000000'

def main():
    filename = "PandaAIQ.jsonl"
    text, stopwords = process_data(filename)
    if not text:
        text = "Arial Vector SVG Layout Perfect " * 100
        stopwords = set()

    font_path = get_arial_font_path()
    geo = get_panda_geometry()
    mask = create_mask(geo)

    wc = WordCloud(
        font_path=font_path,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        mask=mask,
        max_words=150,
        stopwords=stopwords,
        colormap=create_academic_colormap(),
        background_color=None,
        mode="RGBA",
        random_state=42,
        margin=2,
        relative_scaling=0.5
    )
    wc.generate(text)

    fig, ax = plt.subplots(figsize=(FIG_WIDTH_INCH, FIG_HEIGHT_INCH), dpi=CALCULATED_DPI)
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(CANVAS_HEIGHT, 0) 
    ax.set_aspect('equal')
    ax.axis('off')

    draw_vector_background(ax, geo)

    arial_prop = font_manager.FontProperties(fname=font_path) if font_path else None
    
    print("正在进行 SVG 兼容性文字排版...")
    for item in wc.layout_:
        (word, count), font_size_px, position, orientation, color = item
        y_pos, x_pos = position 
        
        font_size_pt = font_size_px * FONT_SCALE_FACTOR
        angle = 90 if orientation is not None and orientation != 0 else 0
        
        ax.text(
            x_pos, y_pos, 
            word,
            fontsize=font_size_pt,
            rotation=angle,
            color=format_color(color), # 使用修复后的颜色函数
            ha='left', va='top',
            fontproperties=arial_prop,
            zorder=20,
            clip_on=False 
        )

    output_file = "Fig2c_Panda_Perfect.svg"
    plt.tight_layout(pad=0)
    plt.savefig(output_file, format='svg', bbox_inches='tight', pad_inches=0.05)
    print(f"✅ 修复成功! SVG 已保存至: {output_file}")
    plt.show()

if __name__ == "__main__":
    jieba.initialize()
    main()