import re
import json

class TypeEvaluator:
    """
    동물 말투(고양이/강아지) 스타일이 잘 반영되었는지 평가
    - 복합 어미/신조어/오타/줄임말 등 최대한 포괄
    - 문장 단위 혼합 평가
    """

    def __init__(self):
        # 고양이 말투 어미/추임새 패턴
        self.cat_endings = [
            # 기본 및 가장 흔한 패턴
            '냥', '냐옹', '이냥', '이다냥', '다냥', '냐용', '이냐옹', '다옹', '냐하', '먀', '먀하', '냐앙', '냐우', '냐욧', '냥냥', '냐옹이', '냐앙앙', '냐야', '냐오', '냐온', '냐홍', '냐뇽', '냐웅', '냐오옹', '먀옹', '먀먀', '냐햏',
            # 줄임/복수형/신조어/유행어
            '냔', '뇽', '뇽뇽', '먀옹', '먀옹먀옹', '냐홍이', '냐옹냥', '냐옹냥냥', '냐하하', '냐핫', '먀하하', '냐욧', '냐옹옹', '냐아앙', '냐아앙앙', '냥옹', '냔냥', '냐야옹', '냐홍', '냐앙', '냐옹냐옹',
            # 띄어쓰기·기호 결합·확장(띄어쓰기/기호 포함)
            ' 냥', ' 냐옹', ' 냐', ' 냐욧', ' 냐옹이', ' 냥냥', '~냥', '~냐옹', '~냐', '~냐하', '~냐용', '~먀', '~냐앙',
            # 말 끝/추임새형
            '먀', '냐옹~', '냐앙~', '냐하~', '냐옹!', '냐앙!', '냐하!', '냐옹.', '냐앙.', '냐하.', '먀.', '먀!', '냐야~', '냐옹냐옹~'
            # 주인 vs 집사 
            '집사'
        ]

        # 강아지 말투 어미/추임새 패턴
        self.dog_endings = [
            # 기본
            '멍', '왈', '다멍', '다개', '다왈', '요멍', '왕', '왕왕', '멍멍', '멍멍이', '컹', '컹컹', '왈왈', '멍이', '멍이멍이', '멍왕',
            # 복합·확장·반복·신조어/유행어
            '멍멍멍', '멍왈', '멍컹', '왈멍', '멍컹컹', '멍왈왈', '왕멍', '왕왕', '왕왕왕', '컹컹컹', '왈왈왈', '컹멍', '멍컹왈', '왕이', '왈이', '몽', '몽몽', '멍뭉', '왈뭉', '몽왈', '멍멍왈', '왕왈', '멍몽', '왈몽', '멍몽왈', '왕몽', '컹컹왕', '왕컹', '왕컹컹',
            # 오타·특수문자·띄어쓰기 포함
            ' 멍', ' 왈', '~멍', '~왈', '~왕', '~멍멍', '~왕왕', '~다멍', '~다개', '~다왈', '~컹', '~멍이', '~멍멍이',
            # 복합 고양이+강아지(혼합)
            '냐멍', '냐왈', '냥왈', '냥멍', '냐멍멍', '냐왕', '냥왕', '냥멍멍'
            # 주인 vs 집사 
            '주인'
        ]

        # 고양이 명사성 지칭어
        self.cat_nouns = [
            '고양이', '냥이', '야옹이', '캣', '냥냥이', '묘', '묘님', '캣초딩', '캣맘', '냥스타그램', '묘생', '캣타워'
        ]
        # 강아지 명사성 지칭어
        self.dog_nouns = [
            '강아지', '댕댕이', '멍멍이', '개', '견', '댕댕', '견생', '개스타그램', '멍스타그램', '견주', '멍뭉이'
        ]


        # 말투 패턴(문장 끝, 단어 끝, 공백 또는 문장부호 뒤)
        self.cat_pattern = re.compile(r"(" + "|".join([re.escape(e) for e in self.cat_endings]) + r")([\W\s]|$)", re.IGNORECASE)
        self.dog_pattern = re.compile(r"(" + "|".join([re.escape(e) for e in self.dog_endings]) + r")([\W\s]|$)", re.IGNORECASE)

        # 명사성 지칭어 패턴
        self.cat_noun_pattern = re.compile(r"|".join([re.escape(n) for n in self.cat_nouns]), re.IGNORECASE)
        self.dog_noun_pattern = re.compile(r"|".join([re.escape(n) for n in self.dog_nouns]), re.IGNORECASE)

    def remove_nouns(self, text: str) -> str:
        """
        고양이/강아지 명사성 지칭어를 모두 공백으로 치환
        """
        text = self.cat_noun_pattern.sub(' ', text)
        text = self.dog_noun_pattern.sub(' ', text)
        return text

    def type_score(self, post_type: str, transformed: str) -> float:
        """
        명사성 지칭어 제외 후, 말투 패턴만으로 점수 계산
        """
        text_wo_noun = self.remove_nouns(transformed)
        has_cat = bool(self.cat_pattern.search(text_wo_noun))
        has_dog = bool(self.dog_pattern.search(text_wo_noun))
        if post_type == "dog":
            if has_cat and not has_dog:
                return 0.1
            elif has_cat and has_dog:
                return 0.2
            elif has_dog:
                return 1.0
            else:
                return 0.0
        elif post_type == "cat":
            if has_dog and not has_cat:
                return 0.1
            elif has_cat and has_dog:
                return 0.2
            elif has_cat:
                return 1.0
            else:
                return 0.0
        else:
            return None

    def evaluate(self, input_path: str) -> list:
        """
        JSONL 데이터셋 평가, type_score만 포함된 리스트 반환
        """
        results = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                post_type = data.get("post_type", "")
                transformed = data.get("transformed_content", "")
                score = self.type_score(post_type, transformed)
                results.append({
                    "post_type": post_type,
                    "transformed_content": transformed,
                    "type_score": score
                })
        return results

# 사용 예시
if __name__ == "__main__":
    evaluator = TypeEvaluator()
    result = evaluator.evaluate("/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/dataset/_dataset/_made/dataset_0527_made.jsonl")
    print(json.dumps(result, ensure_ascii=False, indent=2))