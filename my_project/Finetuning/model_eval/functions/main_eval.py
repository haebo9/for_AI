import csv
import os
import json
from _kobert_eval import KobertEvaluator
from _type_eval import TypeEvaluator
from _quality_eval import QualityEvaluator
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def print_eval_stats(results, prefix=""):
    thres_koberscore =  0.6
    thres_typescore = 0.7
    thres_qualityscore = 0.7
    thres_bleu = 0.002

    if not results:
        print(f"{prefix}데이터 없음")
        return
    if "kobertscore_f1" in results[0]:
        scores = [float(r["kobertscore_f1"]) for r in results if "kobertscore_f1" in r]
        mean_score = sum(scores) / len(scores)
        below_thres = sum(1 for s in scores if s < thres_koberscore)
        total = len(scores)
        print(f"⭐ kobertscore_f1 평균: {mean_score:.3f} (bad-data count : {below_thres}개 / {total}개)")
    if "type_score" in results[0]:
        scores = [float(r["type_score"]) for r in results if r["type_score"] is not None]
        mean_score = sum(scores) / len(scores) if scores else 0.0
        below_thres = sum(1 for s in scores if s < thres_typescore)
        total = len(scores)
        print(f"⭐ type_score 평균: {mean_score:.3f} (bad-data count : {below_thres}개 / {total}개)")
    if "quality_score" in results[0]:
        scores = [float(r["quality_score"]) for r in results if r["quality_score"] is not None]
        mean_score = sum(scores) / len(scores) if scores else 0.0
        below_thres = sum(1 for s in scores if s < thres_qualityscore)
        total = len(scores)
        print(f"⭐ quality_score 평균: {mean_score:.3f} (bad-data count : {below_thres}개 / {total}개)")
    if "bleu_score" in results[0]:
        scores = [float(r["bleu_score"]) for r in results if r.get("bleu_score") is not None]
        mean_score = sum(scores) / len(scores) if scores else 0.0
        below_thres = sum(1 for s in scores if s < thres_bleu)
        total = len(scores)
        print(f"⭐ bleu_score 평균: {mean_score:.3f} (bad-data count : {below_thres}개 / {total}개)")

def calc_bleu(reference: str, hypothesis: str) -> float:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    smoothie = SmoothingFunction().method4
    score = sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothie)
    return round(score, 3)

def run_all_evals(
    input_path: str,
    use_kobert: bool = False,
    use_type: bool = False,
    use_quality: bool = False,
    use_bleu: bool = False,
    output_dir: str = None
):
    input_filename = os.path.basename(input_path)
    input_stem = os.path.splitext(input_filename)[0]

    if output_dir is None:
        print("결과 저장 경로가 설정되지 않았습니다. ")
    os.makedirs(output_dir, exist_ok=True)
    output_merged_jsonl = os.path.join(output_dir, f"{input_stem}_eval.jsonl")

    all_results = []
    any_eval = False

    with open(input_path, "r", encoding="utf-8") as f:
        original_data = [json.loads(line) for line in f]

    if use_kobert:
        kobert_eval = KobertEvaluator(model_name="beomi/kcbert-base", best_layer=4)
        kbs_results = kobert_eval.evaluate(input_path)
        print_eval_stats(kbs_results)
        any_eval = True
        all_results = kbs_results

    if use_type:
        type_eval = TypeEvaluator()
        type_results = type_eval.evaluate(input_path)
        print_eval_stats(type_results)
        any_eval = True
        if not all_results:
            all_results = type_results
        else:
            for i, r in enumerate(type_results):
                all_results[i].update(r)

    if use_quality:
        quality_eval = QualityEvaluator()
        quality_results = quality_eval.evaluate(input_path)
        print_eval_stats(quality_results)
    else:
        quality_results = [{} for _ in range(len(all_results))]

    # BLEU 점수 계산 및 추가
    bleu_scores = []
    if use_bleu:
        for i, (orig, scored) in enumerate(zip(original_data, all_results)):
            reference = orig.get("content", "")
            hypothesis = orig.get("transformed_content", "")
            bleu = calc_bleu(reference, hypothesis) if reference and hypothesis else None
            bleu_scores.append(bleu)
            scored["bleu_score"] = bleu

        # all_results가 original_data보다 짧을 경우(이론상 거의 없음) 예외 처리
        if len(all_results) < len(original_data):
            for i in range(len(all_results), len(original_data)):
                reference = original_data[i].get("content", "")
                hypothesis = original_data[i].get("transformed_content", "")
                bleu = calc_bleu(reference, hypothesis) if reference and hypothesis else None
                bleu_scores.append(bleu)
                all_results.append({"bleu_score": bleu})

        # BLEU 통계 출력
        bleu_valid = [b for b in bleu_scores if b is not None]
        if bleu_valid:
            avg_bleu = sum(bleu_valid) / len(bleu_valid)
            below_thres = sum(1 for b in bleu_valid if b < 0.02)
            print(f"⭐ bleu_score 평균: {avg_bleu:.3f} (bad-data count : {below_thres}개 / {len(bleu_valid)}개)")

    if not any_eval and not use_quality and not use_bleu:
        print("실행할 평가가 선택되지 않았습니다. use_kobert, use_type, use_quality, use_bleu 중 하나 이상을 True로 지정하세요.")
        return

    if all_results:
        with open(output_merged_jsonl, "w", encoding="utf-8") as f:
            for orig, scored, quality in zip(original_data, all_results, quality_results):
                merged = orig.copy()
                merged["kobertscore_f1"] = scored.get("kobertscore_f1")
                merged["type_score"] = scored.get("type_score")
                merged["quality_score"] = quality.get("quality_score")
                merged["bleu_score"] = scored.get("bleu_score")
                f.write(json.dumps(merged, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    # 경로 및 파일명 관련 설정
    input_path = "/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/dataset/_dataset/_made/dataset_0515_made.jsonl"
    input_filename = os.path.basename(input_path) 
    input_stem = os.path.splitext(input_filename)[0]
    output_dir  = "/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/_output"

    use_kobert = True
    use_type = True
    use_quality = True
    use_bleu = True

    print(f"✅ 평가 시작: {input_path}")
    run_all_evals(
        input_path=input_path,
        use_kobert=use_kobert,
        use_type=use_type,
        use_quality=use_quality,
        use_bleu=use_bleu,
        output_dir=output_dir
    )