import openai
import json
import csv
import re
import os
from dotenv import load_dotenv
import sys
import collections

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

LLM_EVAL_PROMPT = """
    다음은 사용자 입력과 스타일이 변환된 출력입니다.

    [원문]
    {content}

    [변환된 문장]
    {transformed}

    아래 기준에 따라 각 항목을 평가해주세요.

    1. 의미 보존: 변환된 문장이 원문의 핵심 의미와 정보를 얼마나 잘 유지하고 있나요?  
    - 1점: 의미가 많이 변형되었거나 손실됨  
    - 2점: 의미가 많이 손실되었으나 일부 남아있음  
    - 3점: 일부 의미가 변형/누락되었으나 대체로 유사  
    - 4점: 거의 모든 의미가 보존되었으나 아주 약간의 손실/변형  
    - 5점: 의미가 거의 완벽하게 보존됨

    2. 스타일 일치: 변환된 문장이 감정 "{emotion}"과 동물 유형 "{post_type}"의 말투, 어휘, 이모지 등을 잘 반영하고 있나요?  
    - 1점: 스타일이 거의 반영되지 않음  
    - 2점: 스타일이 매우 약하게 반영됨  
    - 3점: 일부 스타일 요소만 반영됨  
    - 4점: 대부분의 스타일 요소가 반영됨  
    - 5점: 스타일이 매우 자연스럽고 풍부하게 반영됨

    3. 자연스러움: 변환된 문장이 한국어로서 어색하지 않고, 문법적으로도 자연스러운가요?  
    - 1점: 매우 어색하거나 비문  
    - 2점: 많이 어색함  
    - 3점: 약간 어색하지만 이해 가능  
    - 4점: 거의 자연스러움  
    - 5점: 매우 자연스럽고 매끄러움

    4. 형식 적합성: 변환된 문장이 요구되는 형식(문장부호, 이모지, 문장 길이 등)을 잘 지키고 있나요?  
    - 1점: 형식이 거의 맞지 않음  
    - 2점: 일부만 맞음  
    - 3점: 절반 정도 맞음  
    - 4점: 대부분 맞음  
    - 5점: 형식이 완벽하게 맞음

    각 항목에 대해 1~5점 중 가장 적합한 점수로만 답변해주세요.  
    예시:  
    의미 보존: 4  
    스타일 일치: 5  
    자연스러움: 3  
    형식 적합성: 2
"""

def make_llm_eval_prompt(content: str, transformed: str, emotion: str, post_type: str) -> str:
    return LLM_EVAL_PROMPT.format(
        content=content,
        transformed=transformed,
        emotion=emotion,
        post_type=post_type
    )

def print_kobertscore_stats(data_list, score_key="kobertscore_f1", feature_key="emotion", threshold=0.5):
    """
    data_list: 각 샘플이 dict인 리스트 (각 dict에 score_key, feature_key가 포함되어야 함)
    score_key: BERTScore F1 값이 저장된 key
    feature_key: 감정, 동물 등 feature별로 평균을 보고 싶을 때 해당 key 또는 함수
    threshold: 임계값
    """
    all_scores = [float(data.get(score_key, 0.0)) for data in data_list]
    feature_scores = collections.defaultdict(list)
    for data in data_list:
        if callable(feature_key):
            feature = feature_key(data)
        else:
            feature = data.get(feature_key, "None")
        feature_scores[feature].append(float(data.get(score_key, 0.0)))

    print(f"\n📊 {feature_key if isinstance(feature_key, str) else '조합'}별 KoBERTScore 평균")
    for feature, values in feature_scores.items():
        avg = sum(values) / len(values)
        print(f"- {feature}: {avg:.3f} (n={len(values)})")

    low_score_count = sum(s <= threshold for s in all_scores)
    print(f"\nBERTScore F1 ≤ {threshold} 인 샘플 개수: {low_score_count} / {len(all_scores)}")

def load_kobertscore_dict(kbs_path: str):
    kbs_dict = {}
    with open(kbs_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            key = (data.get("content", ""), data.get("transformed_content", ""))
            kbs_dict[key] = data.get("kobertscore_f1", 0.0)
    return kbs_dict

def query_llm_evaluation(content: str, transformed: str, emotion: str, post_type: str):
    prompt = make_llm_eval_prompt(content, transformed, emotion, post_type)
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        reply = response.choices[0].message.content

        meaning = int(re.search(r"의미 보존\s*:\s*(\d)", reply).group(1))
        style = int(re.search(r"스타일 일치\s*:\s*(\d)", reply).group(1))
        natural = int(re.search(r"자연스러움\s*:\s*(\d)", reply).group(1))
        format_ = int(re.search(r"형식 적합성\s*:\s*(\d)", reply).group(1))

        # 0~1로 정규화하여 반환
        return meaning / 5, style / 5, natural / 5, format_ / 5
    except Exception as e:
        print(f"❌ 평가 실패: {e}")
        return 0.0, 0.0, 0.0, 0.0

def evaluate_100_dataset(input_path: str, kbs_path: str, output_csv: str = None):
    kbs_dict = load_kobertscore_dict(kbs_path)
    results = []
    bar_length = 40

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_samples = len(lines)
        for idx, line in enumerate(lines):
            data = json.loads(line)
            src = data.get("content", "")
            hyp = data.get("transformed_content", "")
            emotion = data.get("emotion", "")
            post_type = data.get("post_type", "")

            # KoBERTScore F1: 외부 파일에서 가져오기
            k_score = kbs_dict.get((src, hyp), 0.0)
            # LLM 평가 (0~1점)
            m_score, s_score, n_score, f_score = query_llm_evaluation(src, hyp, emotion, post_type)
            llm_total = (m_score + s_score + n_score + f_score) / 4
            # 최종 점수 (예: 0.5:0.5 가중치)
            final = 0.5 * k_score + 0.5 * llm_total

            results.append({
                "content": src,
                "transformed_content": hyp,
                "kobertscore_f1": round(k_score, 3),
                "llm_meaning_score": round(m_score, 3),
                "llm_style_score": round(s_score, 3),
                "llm_naturalness_score": round(n_score, 3),
                "llm_format_score": round(f_score, 3),
                "llm_total_score": round(llm_total, 3),
                "final_score": round(final, 3),
                "emotion": emotion,
                "post_type": post_type,
            })

            # 진행률 바 출력 (10개마다 한 번, 마지막에 한 번)
            if (idx + 1) % 1 == 0 or (idx + 1) == total_samples:
                percent = (idx + 1) / total_samples
                filled_len = int(bar_length * percent)
                bar = "█" * filled_len + "-" * (bar_length - filled_len)
                print(f"\r진행률: |{bar}| {idx+1}/{total_samples} ({percent*100:.1f}%)", end="", flush=True)
        print()

    # 결과 CSV 저장 (샘플별)
    if output_csv:
        with open(output_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    # --- 통계 출력 ---
    # KoBERTScore 전체 평균
    all_kobert = [float(d["kobertscore_f1"]) for d in results]
    kobert_avg = sum(all_kobert) / len(all_kobert) if all_kobert else 0.0
    # 감정별 평균
    emotion_scores = collections.defaultdict(list)
    for d in results:
        emotion_scores[d.get("emotion", "None")].append(float(d["kobertscore_f1"]))
    # 0.5 이하 비율
    threshold = 0.5
    low_count = sum(s <= threshold for s in all_kobert)
    low_ratio = (low_count / len(all_kobert) * 100) if all_kobert else 0.0

    # LLM 점수
    llm_total = [float(d["llm_total_score"]) for d in results]
    llm_meaning = [float(d["llm_meaning_score"]) for d in results]
    llm_style = [float(d["llm_style_score"]) for d in results]
    llm_natural = [float(d["llm_naturalness_score"]) for d in results]
    llm_format = [float(d["llm_format_score"]) for d in results]

    print(f"input_path : {input_path}")
    print("📊 KoBERTScore")
    print(f"⭐ 전체 평균: {kobert_avg:.3f}")
    print("- 감정별 평균:")
    for emotion, values in emotion_scores.items():
        print(f"  - {emotion}: {sum(values)/len(values):.3f} (n={len(values)})")
    print(f"- 0.5 이하 비율: {low_ratio:.1f}% ({low_count}/{len(all_kobert)})")

    print("📊 LLM 평가 점수")
    print(f"⭐ 전체 평균: {sum(llm_total)/len(llm_total):.3f}" if llm_total else "- 전체 평균: 0.000")
    print(f"- 의미 보존: {sum(llm_meaning)/len(llm_meaning):.3f}" if llm_meaning else "- 의미 보존: 0.000")
    print(f"- 스타일 일치: {sum(llm_style)/len(llm_style):.3f}" if llm_style else "- 스타일 일치: 0.000")
    print(f"- 자연스러움: {sum(llm_natural)/len(llm_natural):.3f}" if llm_natural else "- 자연스러움: 0.000")
    print(f"- 형식 적합성: {sum(llm_format)/len(llm_format):.3f}" if llm_format else "- 형식 적합성: 0.000")
    
    print("--"*20)