import json
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

def load_eval_results(jsonl_path: str) -> list:
    results = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            results.append(json.loads(line))
    return results

def get_mean_scores(results: list, selected_metrics: Optional[List[str]] = None) -> dict:
    mean_scores = {}
    if not results:
        return mean_scores
    metrics = selected_metrics if selected_metrics else results[0].keys()
    for metric in metrics:
        if metric in results[0]:
            scores = [float(r[metric]) for r in results if r.get(metric) is not None]
            mean_scores[metric] = sum(scores) / len(scores) if scores else 0.0
    return mean_scores

def normalize_scores(scores: dict) -> dict:
    norm = scores.copy()
    # BLEU: 기대 최대값 0.1로 정규화 (0.1 이상은 1.0)
    if "bleu_score" in norm and norm["bleu_score"] is not None:
        norm["bleu_score"] = min(norm["bleu_score"] / 0.1, 1.0)
    # Perplexity: 0.1/perplexity로 정규화 (최대 1.0)
    if "perplexity_score" in norm and norm["perplexity_score"] is not None and norm["perplexity_score"] > 0:
        norm["perplexity_score"] = min(0.1 / norm["perplexity_score"], 1.0)
    else:
        norm["perplexity_score"] = 0.0
    return norm

def plot_radar_chart_multi(
    scores_list: List[dict],
    model_names: List[str],
    selected_metrics: List[str],
    title: str = "Evaluation Score Radar Chart",
    metric_labels=None, 
    thresholds=None
):
    if not scores_list or not selected_metrics:
        print("시각화할 데이터가 없습니다.")
        return

    # 라벨(축 이름) 설정
    if metric_labels:
        labels = [metric_labels.get(m, m) for m in selected_metrics]
    else:
        labels = selected_metrics
        
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    # 최신 방식으로 colormap 사용
    cmap = plt.colormaps['tab10']
    colors = [cmap(i) for i in range(len(scores_list))]

    # --- Threshold 값 시각화 (사용자 지정)
    if thresholds:
        thres_values = [thresholds.get(m, 0) for m in selected_metrics]
        thres_values += thres_values[:1]
        ax.plot(angles, thres_values, color='red', linewidth=2, linestyle='dashed', label="Threshold")
        ax.fill(angles, thres_values, color='red', alpha=0.15, zorder=1)

    # 모델별 점수 시각화
    for idx, (scores, model_name) in enumerate(zip(scores_list, model_names)):
        values = [scores.get(m, 0) for m in selected_metrics]
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=model_name, color=colors[idx], zorder=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=13)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=11)
    ax.set_title(title, size=18, pad=30, fontweight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.15), fontsize=11)
    st.pyplot(fig)

def plot_score_distribution(
    eval_jsonl_bytes_list,
    file_names,
    selected_metrics,
    metric_labels=None,
    thresholds=None
):
    """
    여러 평가 결과 jsonl(bytes) 리스트, 파일명 리스트, 선택 지표 리스트를 받아
    각 지표별로 히스토그램/박스플롯을 그려 Streamlit에 출력
    """

    for metric in selected_metrics:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        metric_scores = []
        for eval_bytes, fname in zip(eval_jsonl_bytes_list, file_names):
            lines = eval_bytes.decode("utf-8").splitlines()
            values = []
            for line in lines:
                try:
                    data = json.loads(line)
                    v = data.get(metric)
                    if v is not None:
                        # --- 정규화 적용 ---
                        norm = normalize_scores({metric: float(v)})
                        values.append(norm[metric])
                except Exception:
                    continue
            if values:
                metric_scores.append((fname, values))

        # 히스토그램 (정규화 값 기준)
        for fname, values in metric_scores:
            axes[0].hist(values, bins=20, alpha=0.5, label=fname)
        if thresholds and metric in thresholds:
            axes[0].axvline(thresholds[metric], color='red', linestyle='--', label='Threshold')
        axes[0].set_title(f"{metric_labels.get(metric, metric) if metric_labels else metric} - Histogram")
        axes[0].set_xlabel("Normalized Score (0~1)")
        axes[0].set_ylabel("Count")
        axes[0].set_xlim(0, 1)
        axes[0].legend()

        # 박스플롯 (정규화 값 기준)
        axes[1].boxplot([v for _, v in metric_scores], labels=[f for f, _ in metric_scores])
        if thresholds and metric in thresholds:
            axes[1].axhline(thresholds[metric], color='red', linestyle='--', label='Threshold')
        axes[1].set_title(f"{metric_labels.get(metric, metric) if metric_labels else metric} - Boxplot")
        axes[1].set_ylabel("Normalized Score (0~1)")
        axes[1].set_ylim(0, 1)

        st.pyplot(fig)