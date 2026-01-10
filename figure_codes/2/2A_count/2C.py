import os
import re
import jieba
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import font_manager
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors
from matplotlib.patches import Circle, Ellipse
import random

# ==========================================
# 1. 配置与几何定义
# ==========================================

# 画布尺寸 (高分辨率)
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1200

# 显示词汇量限制
MAX_SHOW_WORDS = 80

def create_premium_blue_colormap():
    """
    【修改点1】创建以“高级蓝”为主的配色方案。
    强调质感，辅以少量的绿/紫/红作为点缀。
    """
    colors = [
        '#0D47A1', # 皇室深蓝 (主色，稳重)
        '#1565C0', # 经典蓝 (主色)
        '#006064', # 深青色 (辅助，增加深邃感)
        '#00B0FF', # 亮天蓝 (提亮)
        '#2E7D32', # 森林绿 (点缀，自然感)
        '#7B1FA2', # 深紫色 (极少点缀，高级感)
        '#C62828'  # 深红色 (极少点缀，活力)
    ]
    # 使用 LinearSegmentedColormap 并在位置上让蓝色占据主导
    return mcolors.LinearSegmentedColormap.from_list('premium_blue_luxury', colors, N=256)

def get_panda_geometry(width, height):
    """定义熊猫几何参数"""
    center_x = width // 2
    center_y = int(height * 0.55) 
    
    head_radius = int(min(width, height) * 0.35) 
    ear_radius = int(head_radius * 0.45)
    
    # 耳朵位置微调
    ear_offset_x = int(head_radius * 0.72)
    ear_offset_y = int(head_radius * 0.68)
    
    left_ear_center = (center_x - ear_offset_x, center_y - ear_offset_y)
    right_ear_center = (center_x + ear_offset_x, center_y - ear_offset_y)
    
    return {
        'width': width,
        'height': height,
        'head': {'center': (center_x, center_y), 'radius': head_radius},
        'left_ear': {'center': left_ear_center, 'radius': ear_radius},
        'right_ear': {'center': right_ear_center, 'radius': ear_radius}
    }

CUSTOM_SKIP_WORDS = [
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', 
    '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', 
    '着', '没有', '看', '好', '自己', '这', '那', '我们', '以及', '或者', 
    '因为', '所以', '什么', '怎么', '为什么', '此处', '选择', '内容', '格式',
    '应用', '发展', '技术', '领域', '问题', '挑战', '前景', '现状',
    'the', 'and', 'is', 'of', 'to', 'in', 'it', 'that'
]

# ==========================================
# 2. 视觉效果函数 (核心修改区域)
# ==========================================

def create_subtle_light_background(width, height):
    """创建极柔和的浅色背景"""
    Y = np.linspace(0, 1, height)
    # 极淡的灰蓝色渐变
    r = np.interp(Y, [0, 1], [1.0, 0.95])
    g = np.interp(Y, [0, 1], [1.0, 0.96])
    b = np.interp(Y, [0, 1], [1.0, 0.98])
    a = np.ones(height)
    gradient = np.dstack((r, g, b, a))
    gradient = np.tile(gradient, (width, 1, 1)).transpose(1, 0, 2)
    return gradient

def create_mask_from_geometry(geo):
    """生成词云形状掩码"""
    w, h = geo['width'], geo['height']
    mask = np.ones((h, w), dtype=np.uint8) * 255
    y, x = np.ogrid[:h, :w]
    
    hx, hy = geo['head']['center']
    hr = geo['head']['radius']
    head_mask = ((x - hx)**2 + (y - hy)**2) <= hr**2
    
    lx, ly = geo['left_ear']['center']
    lr = geo['left_ear']['radius']
    l_ear_mask = ((x - lx)**2 + (y - ly)**2) <= lr**2
    
    rx, ry = geo['right_ear']['center']
    rr = geo['right_ear']['radius']
    r_ear_mask = ((x - rx)**2 + (y - ry)**2) <= rr**2
    
    full_shape = head_mask | l_ear_mask | r_ear_mask
    mask[full_shape] = 0
    return mask

def draw_circle_layer(ax, center, radius, color, alpha, zorder, offset=(0,0), blur_add=0, linewidth=0, edgecolor=None):
    """辅助绘图函数"""
    cx, cy = center
    ox, oy = offset
    r_final = radius + blur_add
    if edgecolor is None:
        edgecolor = color 
    ax.add_patch(Circle((cx+ox, cy+oy), r_final, facecolor=color, alpha=alpha, zorder=zorder, linewidth=linewidth, edgecolor=edgecolor))

def draw_refined_luxury_3d_effects(ax, geo):
    """
    【修改点2】重构立体光影。
    减少外部投影的脏感，增强内部体积感，打造“悬浮陶瓷”效果。
    """
    # --- 配色定义 (极简、干净) ---
    # 本体颜色：极淡的冷白，几乎看不出颜色，只在阴影处显现体积
    COLOR_BODY_BASE = '#FFFFFF'      # 纯白底
    COLOR_BODY_SHADE = '#E3F2FD'     # 极淡蓝 (用于体积暗部)
    
    # 阴影颜色：收敛、通透
    COLOR_SHADOW_CONTACT = '#B0BEC5' # 接触阴影 (蓝灰，不黑)
    COLOR_SHADOW_AMBIENT = '#CFD8DC' # 环境阴影 (更淡)
    
    # 轮廓与高光
    COLOR_OUTLINE = '#CFD8DC'        # 极淡的轮廓线
    COLOR_RIM_LIGHT = '#FFFFFF'      # 边缘光
    COLOR_SPECULAR = '#FFFFFF'       # 镜面高光

    h = geo['head']
    ears = [geo['left_ear'], geo['right_ear']]

    # ==============================================================================
    # 阶段 1: 绘制耳朵 (Z = 5 ~ 15)
    # ==============================================================================
    Z_EAR = 5
    for ear in ears:
        r = ear['radius']
        c = ear['center']
        
        # 1.1 环境阴影 (Ambient Shadow) - 范围大但极淡，解决“喧宾夺主”
        draw_circle_layer(ax, c, r, COLOR_SHADOW_AMBIENT, alpha=0.3, zorder=Z_EAR, offset=(5, 5), blur_add=2)
        
        # 1.2 接触阴影 (Contact Shadow) - 范围小，靠近物体，锚定位置
        draw_circle_layer(ax, c, r, COLOR_SHADOW_CONTACT, alpha=0.2, zorder=Z_EAR, offset=(2, 2))

        # 1.3 本体填充 (渐变模拟)
        # 底层偏暗
        draw_circle_layer(ax, c, r, COLOR_BODY_SHADE, alpha=1.0, zorder=Z_EAR+1)
        # 上层亮白 (偏移量大，露出右下角的暗部)
        draw_circle_layer(ax, c, r*0.92, COLOR_BODY_BASE, alpha=1.0, zorder=Z_EAR+2, offset=(-r*0.04, -r*0.04))
        
        # 1.4 极细轮廓线
        ax.add_patch(Circle(c, r, fill=False, edgecolor=COLOR_OUTLINE, linewidth=1.5, alpha=0.5, zorder=Z_EAR+3))

    # ==============================================================================
    # 阶段 2: 绘制连接处阴影 (Z = 18)
    # ==============================================================================
    for ear in ears:
        vec_x = h['center'][0] - ear['center'][0]
        vec_y = h['center'][1] - ear['center'][1]
        dist = np.sqrt(vec_x**2 + vec_y**2)
        ao_offset_x = (vec_x / dist) * ear['radius'] * 0.3
        ao_offset_y = (vec_y / dist) * ear['radius'] * 0.3
        # 减淡AO阴影
        draw_circle_layer(ax, ear['center'], ear['radius']*0.5, '#90A4AE', alpha=0.1, zorder=18, offset=(ao_offset_x, ao_offset_y))

    # ==============================================================================
    # 阶段 3: 绘制头部 (Z = 20 ~ 30)
    # ==============================================================================
    Z_HEAD = 20
    hr = h['radius']
    hc = h['center']

    # 3.1 头部环境阴影 (淡且柔和)
    draw_circle_layer(ax, hc, hr, COLOR_SHADOW_AMBIENT, alpha=0.3, zorder=Z_HEAD, offset=(8, 8), blur_add=5)
    
    # 3.2 头部接触阴影 (贴近物体)
    draw_circle_layer(ax, hc, hr, COLOR_SHADOW_CONTACT, alpha=0.2, zorder=Z_HEAD, offset=(3, 3))
    
    # 3.3 头部本体 - 打造温润的陶瓷感
    # 暗部底色
    draw_circle_layer(ax, hc, hr, COLOR_BODY_SHADE, alpha=1.0, zorder=Z_HEAD+1)
    # 亮部主体 (占据大部分面积，只在右下留一点阴影)
    draw_circle_layer(ax, hc, hr*0.96, COLOR_BODY_BASE, alpha=1.0, zorder=Z_HEAD+2, offset=(-hr*0.02, -hr*0.02))
    
    # 3.4 边缘光 (Rim Light) - 在左上角增加一道亮边，增加立体清晰度
    ax.add_patch(Circle((hc[0]-1, hc[1]-1), hr-1, fill=False, edgecolor=COLOR_RIM_LIGHT, linewidth=2, alpha=0.8, zorder=Z_HEAD+3))

    # 3.5 极细轮廓线
    ax.add_patch(Circle(hc, hr, fill=False, edgecolor=COLOR_OUTLINE, linewidth=1.5, alpha=0.6, zorder=Z_HEAD+4))

    # 3.6 镜面高光 - 更加锐利但透明度降低，不抢眼
    spec_pos_x = hc[0] - hr * 0.3
    spec_pos_y = hc[1] - hr * 0.3
    ax.add_patch(Ellipse((spec_pos_x, spec_pos_y), width=hr*0.25, height=hr*0.18, angle=135, color=COLOR_SPECULAR, alpha=0.6, zorder=Z_HEAD+5, linewidth=0))


# ==========================================
# 3. 数据处理与主逻辑
# ==========================================

def get_font_path():
    font_candidates = [
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arialuni.ttf"
    ]
    for font in font_candidates:
        if os.path.exists(font):
            return font
    return None

def process_text_data(filename):
    if not os.path.exists(filename): return None, None, 0
    try:
        with open(filename, 'r', encoding='utf-8') as f: lines = f.readlines()
        questions = []
        for line in lines:
            try: questions.append(json.loads(line.strip())['question'])
            except: continue
    except: return None, None, 0
    
    if not questions: return None, None, 0

    all_text = " ".join(questions)
    # 清洗文本
    all_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', all_text)
    
    cut_text = jieba.cut(all_text, cut_all=False)
    processed_text = " ".join(cut_text)
    final_stopwords = set(STOPWORDS) | set(CUSTOM_SKIP_WORDS)
    return processed_text, final_stopwords, len(questions)

def generate_luxury_panda_wordcloud(filename):
    if not os.path.exists(filename):
        print(f"❌ 错误: 找不到文件 {filename}")
        return

    print(f"正在处理 {filename}...")
    processed_text, stopwords, count = process_text_data(filename)
    if not processed_text:
        print("数据为空。")
        return

    font_path = get_font_path()
    geo = get_panda_geometry(CANVAS_WIDTH, CANVAS_HEIGHT)
    mask = create_mask_from_geometry(geo)

    print(f"正在生成词云 (高级蓝配色)...")
    wc = WordCloud(
        font_path=font_path,
        background_color=None, # 透明背景
        mode='RGBA',
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        mask=mask,
        max_words=MAX_SHOW_WORDS,
        stopwords=stopwords,
        colormap=create_premium_blue_colormap(), # 【应用修改1】
        random_state=42,
        margin=6, 
        relative_scaling=0.5,
        scale=1,
        min_font_size=16,
        max_font_size=240
    )
    wc.generate(processed_text)

    # 绘图设置
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='white')
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(CANVAS_HEIGHT, 0)
    ax.axis('off')

    print("正在渲染背景与优化后的立体效果...")
    bg_gradient = create_subtle_light_background(CANVAS_WIDTH, CANVAS_HEIGHT)
    ax.imshow(bg_gradient, aspect='auto', extent=[0, CANVAS_WIDTH, CANVAS_HEIGHT, 0], zorder=0)

    # 【应用修改2】
    draw_refined_luxury_3d_effects(ax, geo)

    print("正在合成最终图像...")
    ax.imshow(wc, interpolation='bilinear', alpha=0.98, zorder=40)
    
    output_filename = 'luxury_blue_panda.png'
    plt.tight_layout(pad=0)
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor='white', pad_inches=0)
    print(f"✅ 成功! 图像已保存至: {output_filename}")
    plt.show()

if __name__ == "__main__":
    jieba.initialize()
    generate_luxury_panda_wordcloud("PandaAIQ.jsonl")