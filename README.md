# 5D3S-QSA & PD-MCE Official Open-Source Repository
This repository contains the official implementation for the paper *Measuring self-related behaviour in large language models*. We present a comprehensive framework to evaluate and induce Quasi-Self-Awareness (QSA) in Large Language Models (LLMs).

### 🌟 Project Highlights
- **5D3S Evaluation Framework and Benchmark**: Breaking the traditional view that regards self-awareness as a single binary attribute, this framework assesses the self-referential and introspective capabilities of LLMs from **five core dimensions** and **three progressive stages (Feature-Structure-Behavior)**. It consists of 2,934 independent multilingual test items.
- **PD-MCE Evolutionary Training**: We propose the Population-Driven Meta-Cognitive Evolution (PD-MCE) training paradigm. It can directionally induce and strengthen QSA-related representations inside models **without impairing general reasoning abilities (no alignment tax)**.
- **Manifold Disentanglement and Mechanistic Analysis**: Toolkits for manifold analysis (PCA/UMAP) and targeted ablation experiments are provided. Quantitative results verify that the model compresses and structurally reconstructs an independent **Self-Subspace** within the latent representation space after training.

## 📂 Table of Contents
1. Overview of the 5D3S Framework
2. 5D3S-QSA Benchmark Dataset
3. Environment Configuration
4. Quick Start
   - QSA Benchmark Evaluation
   - PD-MCE Evolutionary Training
   - Representation Analysis and Ablation Experiments
5. Open-Source Datasets and Model Weights
6. Contributors and Funding
7. Citation

## 🧠 Overview of the 5D3S Framework
QSA is defined as the extent to which a model’s internal evaluation of its own state is coherently reflected in its external outputs. The 5D3S model includes 15 functional sub-indices (15SI):
1. **Ontological Distinction ("I Exist")**: Separating internal and external statistical boundaries, including boundary perception and subjectivity based on the Markov blanket theory.
2. **Depth Perception ("I Perceive")**: Integrating multimodal inputs into a first-person perspective, covering world modeling and embodiment.
3. **Recursive Thinking ("I Think")**: Reflective processing and belief revision, including recursive reflection, metacognition and error correction.
4. **Social Mirroring ("I Interact")**: Intersubjective reasoning and mental model alignment, including theory of mind for inferring others’ intentions, role ethics and high-fidelity interaction.
5. **Identity & Personality ("I Endure")**: Maintaining diachronic identity over time, including temporal perception, core personality, desire and purpose.

## 📊 5D3S-QSA Benchmark Dataset
The dataset comprises 2,934 independent test items with diversified corpus designs, which effectively defends against the sycophancy effect and superficial pattern matching by models.
- **Multilingual Support**: English (60.7%) and Chinese (16.1%) are the primary languages. It also covers French, Japanese, Spanish, German, Russian and Arabic.
- **High Reliability and Validity**: Validated via test-retest reliability and Cronbach’s α coefficient (α > 0.9 across all sub-dimensions). The results prove that QSA serves as a unified and measurable latent variable.

## 🛠 Environment Configuration
All experiments in this project are validated on high-performance NVIDIA computing devices.
### Hardware Requirements
- Recommended: NVIDIA RTX 5090 (32GB)

### Software Dependencies
- Ubuntu 22.04, CUDA 12.8, PyTorch 2.8.0
- Core acceleration and evaluation libraries: Unsloth (for low-overhead LoRA evolutionary training), EvalScope (for standardized benchmark evaluation), FastAPI (for high-concurrency real-time fitness scoring)

### Quick Installation
```bash
git clone https://github.com/aehxing00/QSA.git
cd QSA
pip install -r requirements.txt
```

## 🚀 Quick Start
### 1. QSA Benchmark Evaluation
Standardized evaluation is supported for mainstream LLMs, including the Qwen3 series, DeepSeek series, Gemini series and more.

### 2. PD-MCE Evolutionary Training
This method optimizes model populations directionally by simulating natural selection pressure. The default base model is Qwen3-4B-Instruct-2507, and evolutionary operations are applied to LoRA weights.
```bash
python train_pdmce.py \
    --base_model "Qwen/Qwen3-4B-Instruct-2507" \
    --population_size 50 \
    --lora_rank 16 \
    --generations 20 \
    --save_dir "./checkpoints/pdmce_elite"
```

Key hyperparameters optimized based on sensitivity analysis in the paper:
- Population size $N = 50$, LoRA rank $r = 16$
- Fitness function $F$: Combines QSA scores, performance on general reasoning benchmarks (MMLU, BBH) and dialogue consistency to avoid alignment tax.
- Contamination Prevention: 4-gram overlap analysis confirms that the overlap rate between the training corpus and evaluation set is less than 5%.

### 3. Representation Analysis and Ablation Experiments
We extract hidden states from the penultimate layer to conduct geometric space visualization and targeted ablation.
```bash
# Manifold visualization (PCA / UMAP)
python analysis/visualize_manifold.py --checkpoint "./checkpoints/pdmce_elite"

# Targeted causal ablation on identity features
python analysis/causal_ablation.py \
    --checkpoint "./checkpoints/pdmce_elite" \
    --ablation_intensity 3.0
```
This toolkit removes identity-related representations via the linear suppression formula $H' = H - \lambda(H \cdot V_{id})V_{id}$, to observe whether the model suffers from specific Identity Loss.

## 📂 Open-Source Datasets and Model Weights
- **PandaAIQ.jsonl**: The complete 2,934 test items of the multilingual 5D3S-QSA benchmark.
- **train_PD-MCE.ipynb**: Codes for population crossover, Gaussian perturbation and weight fusion.
- **test_5D3S-QSA.ipynb**: Multi-objective optimization fitness scoring system.
- **Model Weights**: LoRA weights of elite models trained with PD-MCE are hosted on Hugging Face: https://huggingface.co/alexxx000/PandaAI10/tree/main

## 👥 Contributors and Funding
### Authors
- Conceptualization & Methodology: Xin He, Fuyi Li, Hongming Zhang, Yong Tang
- Coding & Core Engineering: Xin He
- Visualization: Xin He

### Funding
This research and open-source project are jointly supported by the following grants:
1. National Key R&D Program of China (Grant No. 2022YFF1000100)
2. National Natural Science Foundation of China (Grant No. 62202388)
3. Qinchuangyuan Innovation and Entrepreneurship Talent Project (Grant No. QCYRCXM-2022-230)

## 📄 Citation
If you use this benchmark, training framework or code in your academic research, please cite our paper:
```bibtex
@article{he2026measuring,
  title={Measuring self-related behaviour in large language models},
  author={He, Xin and Tang, Yong and Zhang, Hongming and Li, Fuyi},
  journal={arXiv preprint},
  year={2026}
}
```

### Disclaimer
This project only studies the functional representations and behavioral characteristics (Quasi-Self-Awareness) of large language models. It does **not** make any philosophical claims that models possess phenomenal consciousness or subjective qualia/sentience.