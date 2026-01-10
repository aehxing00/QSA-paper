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
# 1. 物理尺寸严格定义 (Pixel vs Point)
# ==========================================

# 1. 设定画布分辨率 (像素) - 4:3 比例
# 提高分辨率以保证词云计算的精度
CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 1500

# 2. 设定输出图片物理尺寸 (英寸)
FIG_WIDTH_INCH = 8
FIG_HEIGHT_INCH = 6

# 3. 计算 DPI (每英寸像素数)
# 公式: 像素 / 英寸
CALCULATED_DPI = CANVAS_WIDTH / FIG_WIDTH_INCH  # 2000 / 8 = 250 DPI

# 4. 【核心修复】字号换算因子
# Matplotlib fontsize 单位是 Point (pt)
# 1 inch = 72 pt
# 转换公式: Points = Pixels * (72 / DPI)
# 这能保证矢量字的大小与像素图完全一致！
FONT_SCALE_FACTOR = 72 / CALCULATED_DPI 

def get_arial_font_path():
    """强制使用 Arial 字体"""
    candidates = [
        "C:/Windows/Fonts/arialuni.ttf", 
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "C:/Windows/Fonts/msyh.ttc", 
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for f in candidates:
        if os.path.exists(f): return f
    return "C:/Windows/Fonts/arial.ttf"

def create_academic_colormap():
    """学术配色：深蓝主导"""
    colors = [
        '#0D47A1', '#1565C0', '#00695C', '#B71C1C', '#4A148C', '#0277BD'
    ]
    return mcolors.LinearSegmentedColormap.from_list('cns_academic', colors, N=256)

def get_panda_geometry():
    """定义熊猫几何"""
    w, h = CANVAS_WIDTH, CANVAS_HEIGHT
    cx, cy = w // 2, int(h * 0.55)
    
    # 头部半径
    head_r = int(h * 0.42)
    
    # 耳朵
    ear_r = int(head_r * 0.42)
    ear_off_x = int(head_r * 0.75)
    ear_off_y = int(head_r * 0.70)
    
    return {
        'head': (cx, cy, head_r),
        'left_ear': (cx - ear_off_x, cy - ear_off_y, ear_r),
        'right_ear': (cx + ear_off_x, cy - ear_off_y, ear_r)
    }

# ==========================================
# 2. 矢量底图 (浅色轮廓)
# ==========================================

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
    """
    【修改点】使用极浅的颜色描边
    """
    C_SHADOW = '#F5F5F5' 
    C_STROKE = '#CFD8DC' # 浅蓝灰 (Light Blue Grey) - 极淡的轮廓
    C_FILL = '#FFFFFF'
    LW = 1.5             # 细线，更精致
    
    def plot_part(cx, cy, r, z_shadow, z_body):
        # 阴影
        ax.add_patch(Circle((cx + 15, cy + 15), r, facecolor=C_SHADOW, edgecolor=None, zorder=z_shadow))
        # 本体
        ax.add_patch(Circle((cx, cy), r, facecolor=C_FILL, edgecolor=C_STROKE, linewidth=LW, zorder=z_body))

    plot_part(*geo['left_ear'], 5, 6)
    plot_part(*geo['right_ear'], 5, 6)
    plot_part(*geo['head'], 10, 11)

# ==========================================
# 3. 主逻辑
# ==========================================

def process_data(filename):
    if not os.path.exists(filename): return None, None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = " ".join([json.loads(line)['question'] for line in f if line.strip()])
    except: return None, None
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', text)
    words = jieba.cut(text)
    stopwords = set(STOPWORDS) | {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
        '自己', '这', '那', '我们', '以及', '或者', '因为', '所以', '什么', '怎么',
        '为什么', '此处', '选择', '内容', '格式', 'the', 'and', 'is', 'of', 'to'
    }
    return " ".join(words), stopwords

def rgb2hex(c):
    if isinstance(c, str) and c.startswith('rgb'):
        vals = [int(x) for x in re.findall(r'\d+', c)]
        return '#{:02x}{:02x}{:02x}'.format(*vals)
    return c

def main():
    filename = "PandaAIQ.jsonl"
    text, stopwords = process_data(filename)
    if not text:
        text = "Arial Academic Figure Vector PDF Analysis Clear Layout " * 50
        stopwords = set()

    font_path = get_arial_font_path()
    geo = get_panda_geometry()
    mask = create_mask(geo)

    print(f"1. 画布: {CANVAS_WIDTH}x{CANVAS_HEIGHT}, DPI: {CALCULATED_DPI}")
    print(f"2. 字号换算因子 (Px -> Pt): {FONT_SCALE_FACTOR:.3f}")

    # 生成词云 (使用原始标准的参数，不需要hack了)
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
        margin=2,              # 恢复正常间距
        relative_scaling=0.5,  # 恢复标准比例
        min_font_size=10
    )
    wc.generate(text)

    # 初始化绘图
    # 【关键】设置 DPI 与计算值一致
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_INCH, FIG_HEIGHT_INCH), dpi=CALCULATED_DPI)
    
    # 锁定坐标系
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(CANVAS_HEIGHT, 0) # 翻转Y轴
    ax.set_aspect('equal')
    ax.axis('off')

    # 绘制背景
    draw_vector_background(ax, geo)

    print("3. 正在绘制矢量文字 (应用精确换算)...")
    arial_prop = font_manager.FontProperties(fname=font_path)
    
    # 【核心循环】
    for item in wc.layout_:
        # item结构: ((word, count), font_size, position, orientation, color)
        (word, count), font_size_px, position, orientation, color = item
        
        # 【BUG 修复点 1】：坐标解包
        # WordCloud 的 position 是 (row, col) 即 (y, x)
        # Matplotlib 需要 (x, y)
        y_pos, x_pos = position 
        
        # 【BUG 修复点 2】：单位换算
        # 将 像素(px) 转换为 点(pt)
        # 之前这里没有乘系数，导致字号大了3-4倍
        font_size_pt = font_size_px * FONT_SCALE_FACTOR
        
        angle = 90 if orientation is not None and orientation != 0 else 0
        
        ax.text(
            x_pos, y_pos, 
            word,
            fontsize=font_size_pt, # 使用换算后的点数
            rotation=angle,
            color=rgb2hex(color),
            ha='left', va='top',   # WordCloud 默认对齐方式
            fontproperties=arial_prop,
            zorder=20
        )

    output_file = "Fig2c_Perfect_Vector.pdf"
    plt.tight_layout(pad=0)
    plt.savefig(output_file, format='pdf', dpi=300, facecolor='white')
    print(f"✅ 完美修复！矢量 PDF 已保存至: {output_file}")
    plt.show()

if __name__ == "__main__":
    jieba.initialize()
    main()