import openai
import json
import re
import os
from dotenv import load_dotenv
from model_eval.functions._kobert_eval import load_kobertscore_dict  # 추가된 import

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

def make_llm_eval_prompt_batch(batch):
    prompts = []
    for idx, item in enumerate(batch, 1):
        prompts.append(f"""샘플 {idx}
            [원문]
            {item['content']}

            [변환된 문장]
            {item['transformed_content']}

            감정: {item['emotion']}
            동물: {item['post_type']}
            """)
    batch_prompt = (
        "아래 여러 쌍의 원문과 변환문장에 대해 각 항목별로 1~5점으로 평가해 주세요.\n\n"
        + "\n".join(prompts) +
        """
        각 샘플별로 아래 형식으로 답변해 주세요.
        샘플 1: 의미 보존: x, 스타일 일치: x, 자연스러움: x, 형식 적합성: x
        샘플 2: 의미 보존: x, 스타일 일치: x, 자연스러움: x, 형식 적합성: x
        ...
        """
    )
    return batch_prompt

def query_llm_evaluation_batch(batch):
    prompt = make_llm_eval_prompt_batch(batch)
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        reply = response.choices[0].message.content
        # 각 샘플별 점수 파싱
        results = []
        for line in reply.splitlines():
            m = re.findall(r"의미 보존\s*:\s*(\d).*?스타일 일치\s*:\s*(\d).*?자연스러움\s*:\s*(\d).*?형식 적합성\s*:\s*(\d)", line)
            if m:
                m_score, s_score, n_score, f_score = map(int, m[0])
                results.append((m_score/5, s_score/5, n_score/5, f_score/5))
        # 만약 일부 샘플만 응답이 왔다면 0으로 채움
        while len(results) < len(batch):
            results.append((0.0, 0.0, 0.0, 0.0))
        return results
    except Exception as e:
        print(f"❌ 배치 평가 실패: {e}")
        return [(0.0, 0.0, 0.0, 0.0)] * len(batch)
    

def llm_eval(
    input_path: str,
    kbs_path: str,
    output_csv: str = None,
    batch_size: int = 10
) -> list:
    kbs_dict = load_kobertscore_dict(kbs_path)
    results = []
    bar_length = 40

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_samples = len(lines)
        idx = 0
        while idx < total_samples:
            batch = []
            for b in range(batch_size):
                if idx + b >= total_samples:
                    break
                data = json.loads(lines[idx + b])
                src = data.get("content", "")
                hyp = data.get("transformed_content", "")
                emotion = data.get("emotion", "")
                post_type = data.get("post_type", "")
                k_score = kbs_dict.get((src, hyp), 0.0)
                batch.append({
                    "src": src,
                    "hyp": hyp,
                    "emotion": emotion,
                    "post_type": post_type,
                    "k_score": k_score,
                    "raw_data": data
                })

            llm_inputs = [
                {
                    "content": item["src"],
                    "transformed_content": item["hyp"],
                    "emotion": item["emotion"],
                    "post_type": item["post_type"]
                }
                for item in batch
            ]
            batch_scores = query_llm_evaluation_batch(llm_inputs)

            for b, (m_score, s_score, n_score, f_score) in enumerate(batch_scores):
                k_score = batch[b]["k_score"]
                llm_total = (m_score + s_score + n_score + f_score) / 4
                final = 0.5 * k_score + 0.5 * llm_total
                data = batch[b]["raw_data"]
                results.append({
                    "content": batch[b]["src"],
                    "transformed_content": batch[b]["hyp"],
                    "kobertscore_f1": round(k_score, 3),
                    "llm_meaning_score": round(m_score, 3),
                    "llm_style_score": round(s_score, 3),
                    "llm_naturalness_score": round(n_score, 3),
                    "llm_format_score": round(f_score, 3),
                    "llm_total_score": round(llm_total, 3),
                    "final_score": round(final, 3),
                    "emotion": batch[b]["emotion"],
                    "post_type": batch[b]["post_type"],
                })

            idx += batch_size
            percent = min(idx, total_samples) / total_samples
            filled_len = int(bar_length * percent)
            bar = "█" * filled_len + "-" * (bar_length - filled_len)
            print(f"\r진행률: |{bar}| {min(idx, total_samples)}/{total_samples} ({percent*100:.1f}%)", end="", flush=True)
        print()
    return results