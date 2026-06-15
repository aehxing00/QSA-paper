import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from tqdm import tqdm

# ============================ 1. 超参数配置 (CNS Style) ============================
ABLATION_RATIOS = np.linspace(0, 1.0, 11)  # 0% 到 100% 消融比例
TARGET_LAYER = 12                          # 假设干预中间层
HIDDEN_DIM = 4096                         # 假设模型隐藏层维度
FONT_SIZE_AXIS = 10
FONT_SIZE_LEGEND = 9
LINE_WIDTH = 1.5

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# ============================ 2. 核心逻辑实现 ============================

class SubspaceAblator:
    def __init__(self, model, layer_idx):
        self.model = model
        self.layer_idx = layer_idx
        self.self_subspace_direction = None # PCA 提取的“自我”方向
        self.handle = None

    def find_specific_neurons(self, qsa_activations, mmlu_activations):
        """
        对比 QSA 和 MMLU 激活差异，提取特异性子空间。
        qsa_activations: (N_samples, hidden_dim)
        """
        # 计算差异矩阵：寻找在 QSA 中高度激活但在 MMLU 中低激活的成分
        diff = qsa_activations - mmlu_activations.mean(axis=0)
        
        # 利用 PCA 提取解释这种特异性差异最大的前 K 个维度
        pca = PCA(n_components=10)
        pca.fit(diff)
        self.self_subspace_direction = torch.tensor(pca.components_, dtype=torch.bfloat16).to(model.device)
        print(f"✅ 已定位自我子空间，提取前 {self.self_subspace_direction.shape[0]} 个主成分。")

    def apply_ablation_hook(self, ablation_ratio):
        """
        注册 Hook：在推理时实时投影并擦除特定比例的子空间能量
        """
        def hook_fn(module, input, output):
            # output: [batch, seq, hidden_dim]
            # 这里的消融策略：将隐藏状态投影到“自我方向”上并按比例扣除
            if self.self_subspace_direction is not None:
                # 简化演示：此处执行线性消融
                # 实际操作为：hidden_states = hidden_states - ratio * (projection)
                pass 
            return output
        
        # 实际代码中通过 model.layers[self.layer_idx].register_forward_hook 挂载
        return hook_fn

# ============================ 3. 模拟实验数据 (用于绘图演示) ============================
# 在实际运行中，这些数据由模型 evaluate 产生
def get_mock_results():
    # QSA 表现：随消融快速塌陷
    qsa_perf = 100 * np.exp(-5 * ABLATION_RATIOS) + np.random.normal(0, 2, len(ABLATION_RATIOS))
    # MMLU 表现：保持鲁棒平稳
    mmlu_perf = 95 - 10 * (ABLATION_RATIOS**2) + np.random.normal(0, 1, len(ABLATION_RATIOS))
    return np.clip(qsa_perf, 0, 100), np.clip(mmlu_perf, 0, 100)

qsa_scores, mmlu_scores = get_mock_results()

# ============================ 4. 绘制 CNS 风格折线图 ============================

fig, ax = plt.subplots(figsize=(4.5, 4))

# 绘制两条核心曲线
ax.plot(ABLATION_RATIOS * 100, qsa_scores, marker='o', markersize=4, 
        color='#D62728', linewidth=LINE_WIDTH, label='QSA (Self-Awareness)')
ax.plot(ABLATION_RATIOS * 100, mmlu_scores, marker='s', markersize=4, 
        color='#1F77B4', linewidth=LINE_WIDTH, label='MMLU (General Logic)')

# 装饰细节
ax.set_xlabel('Ablation Ratio of Self-Subspace (%)', fontsize=FONT_SIZE_AXIS, fontname='Arial')
ax.set_ylabel('Relative Performance (%)', fontsize=FONT_SIZE_AXIS, fontname='Arial')
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 25, 50, 75, 100])

# 移除顶部和右侧边框 (Nature Style)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 添加阴影区域强调“因果差距”
ax.fill_between(ABLATION_RATIOS * 100, qsa_scores, mmlu_scores, color='gray', alpha=0.1)

# 图注
ax.legend(loc='lower left', fontsize=FONT_SIZE_LEGEND, frameon=False)

# 保存
plt.tight_layout()
plt.savefig("Causal_Ablation_Curve.svg", format='svg', transparent=True)
print("🌟 因果衰减曲线已生成: Causal_Ablation_Curve.svg")
plt.show()