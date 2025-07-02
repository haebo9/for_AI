import re
import json

class TypeEvaluator:
    def __init__(self):
        self.cat_endings = ['냥', '냐옹', '이냥', '이다냥', '다먀', '댜옹']
        self.dog_endings = ['왈', '멍', '~다멍', '~냐왈', '~냐멍', '~다왈', '~다개', '~요멍']
        self.cat_pattern = re.compile("|".join([re.escape(e) for e in self.cat_endings]))
        self.dog_pattern = re.compile("|".join([re.escape(e) for e in self.dog_endings]))

    def type_score(self, post_type: str, transformed: str) -> float:
        if post_type == "dog":
            has_cat = bool(self.cat_pattern.search(transformed))
            has_dog = bool(self.dog_pattern.search(transformed))
            if has_cat and not has_dog:
                return 0.250
            elif has_cat and has_dog:
                return 0.500
            elif has_dog:
                return 1.000
            else:
                return 0.000
        elif post_type == "cat":
            has_cat = bool(self.cat_pattern.search(transformed))
            has_dog = bool(self.dog_pattern.search(transformed))
            if has_dog and not has_cat:
                return 0.250
            elif has_cat and has_dog:
                return 0.500
            elif has_cat:
                return 1.000
            else:
                return 0.000
        else:
            return None

    def evaluate(self, input_path: str) -> list:
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