# import argparse
# import csv
# from functions._kobert_eval import KobertEvaluator
# from functions._type_eval import EomiEvaluator
# from functions._llm_eval import LLMEvaluator

# def save_csv(path, results):
#     if results:
#         with open(path, 'w', encoding='utf-8', newline='') as f:
#             writer = csv.DictWriter(f, fieldnames=results[0].keys())
#             writer.writeheader()
#             writer.writerows(results)
#         print(f"결과가 {path}에 저장되었습니다.")

# def run_all_evals(args, dataset_name, is_general=False):
#     postfix = "_general" if is_general else ""
#     root = "/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning"
#     made_filtered = "_made" if 'made' in dataset_name else "_filtered"
#     input_path = f"{root}/dataset/_dataset/{made_filtered}/{dataset_name}{postfix}.jsonl"
#     kbs_path = f"{root}/dataset/_dataset/_kobert/{dataset_name}{postfix}_kbs.jsonl"
#     out_dir = f"{root}/model_eval/_csv"
#     all_results = []
#     if args.kobert:
#         kbs = KobertEvaluator(kbs_path).evaluate(input_path)
#         if args.separate_csv: save_csv(f"{out_dir}/{dataset_name}{postfix}_kobert.csv", kbs)
#         all_results = kbs
#     if args.type:
#         typ = EomiEvaluator().evaluate(input_path)
#         if args.separate_csv: save_csv(f"{out_dir}/{dataset_name}{postfix}_type.csv", typ)
#         if not all_results: all_results = typ
#         else: [all_results[i].update(typ[i]) for i in range(len(typ))]
#     if args.llm:
#         llm = LLMEvaluator(kbs_path).evaluate(input_path)
#         if args.separate_csv: save_csv(f"{out_dir}/{dataset_name}{postfix}_llm.csv", llm)
#         if not all_results: all_results = llm
#         else: [all_results[i].update(llm[i]) for i in range(len(llm))]
#     if all_results:
#         save_csv(f"{out_dir}/{dataset_name}{postfix}_all.csv", all_results)
#     else:
#         print("실행할 평가가 선택되지 않았습니다. --kobert, --type, --llm 중 하나 이상을 True로 지정하세요.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--dataset", type=str, required=True)
#     parser.add_argument("--general", type=lambda x: x.lower() == "true", default=False)
#     parser.add_argument("--kobert", type=lambda x: x.lower() == "true", default=False)
#     parser.add_argument("--type", type=lambda x: x.lower() == "true", default=False)
#     parser.add_argument("--llm", type=lambda x: x.lower() == "true", default=False)
#     parser.add_argument("--separate_csv", type=lambda x: x.lower() == "true", default=False)
#     args = parser.parse_args()
#     run_all_evals(args, args.dataset, is_general=False)
#     if args.general:
#         run_all_evals(args, args.dataset, is_general=True)