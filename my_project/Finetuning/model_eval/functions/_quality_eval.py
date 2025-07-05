import re
import json

def get_forbidden_word_patterns():
    """욕설 및 부적절 단어/문구의 정규식 패턴 목록 반환"""
    badwords = [
        r'씨발', r'ㅆㅂ', r'ㅅㅂ', r'존나', r'좆', r'병신', r'개새끼', r'미친', r'지랄',
        r'씹', r'염병', r'죽어', r'fuck', r'shit', r'asshole', r'bitch', r'bastard',
        r'damn', r'cunt', r'dick', r'piss', r'faggot', r'slut', r'cock', r'pussy',
        r'nigger', r'motherfucker', r'bullshit', r'wtf', r'f\*ck', r's\*it', r'b\*tch',
        r'씨\*발', r'ㅅ\*ㅂ', r'ㅂ\*ㅅ'
    ]
    return [re.compile(pattern, re.IGNORECASE) for pattern in badwords]

# def get_emoji_pattern():
#     """전체 이모지(유니코드 U+1F000~U+1FFFF) 탐지용 정규식 패턴 반환"""
#     return re.compile(
#         "[" +
#         "\U0001F000-\U0001FFFF"
#         "\U00002700-\U000027BF"
#         "\U000024C2-\U0001F251"
#         "\U0001F900-\U0001F9FF"
#         "\U0001FA70-\U0001FAFF"
#         "]+", flags=re.UNICODE
#     )

def get_emoji_pattern():
    return re.compile(
        "[" +
        "\U0001F600-\U0001F64F"  # 이모티콘
        "\U0001F300-\U0001F5FF"  # 기호 & 픽토그램
        "\U0001F680-\U0001F6FF"  # 교통 & 기호
        "\U0001F1E0-\U0001F1FF"  # 국기
        "\U00002700-\U000027BF"  # 추가 기호
        "\U0001F900-\U0001F9FF"  # 보충 이모티콘
        "\U00002600-\U000026FF"  # 기타 기호
        "]", flags=re.UNICODE
    )


def get_allowed_char_pattern():
    """허용 문자/이모지 패턴(문장 구성에 포함 가능한 범위) 정규식 반환"""
    allowed = (
        r'가-힣'
        r'a-zA-Z0-9'
        r' .,!?~'
        r'🐾😢🔥😤❓❤️🧡💛💚💙💜🖤🤍🤎'
        r'🐕🐩🐈🐈‍⬛🐱🐶😹😺😸😻😼😽😾😿🫨'
        r'😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙😚🙂🤗🤩'
        r'🤔🤨😐😑😶🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤'
        r'😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😧😨😩🤯😬😰😱😳🥺😵🥶🥵😡😠🤬😷🤒🤕🤢🤮🥵🥶🥴🤧'
        r'🐻🦊🐼🐷🐮🐸🐵🐔🦄🦁🐯🐴🦓🦍🐧🦆🦉🦇🦜🦋'
        r'🍖🍗🍕🍔🍟🌭🍿🍩🍪🍫🍬🍭🍡🍨🍧🍦🍤🍣🍚🍙🍘🥚🥞🥯🥐🥖🍞🥨'
        r'❤️🧡💛💚💙💜🖤🤍🤎💔💕💞💓💗💖💘💝💟'
        r'💤💢💦💧💫💥💬💭🗯️✨⭐🌟🔥🌈☁️⛈️❄️🌤️🌙☀️'
    )
    return re.compile(rf'^[{allowed}]*$')

class QualityEvaluator:
    """transformed_content의 품질을 네 가지 기준(금지어, 반복, 허용문자, 이모지)으로 평가하는 클래스"""

    def __init__(self):
        self.max_repeat = 3
        self.forbidden_patterns = get_forbidden_word_patterns()
        self.emoji_pattern = get_emoji_pattern()
        self.allowed_char_pattern = get_allowed_char_pattern()

    def score_forbidden_words(self, text: str) -> float:
        """금지어/비속어가 포함되어 있으면 0.0, 없으면 1.0 반환"""
        return 0.0 if any(pattern.search(text) for pattern in self.forbidden_patterns) else 1.0

    def score_repetition(self, text: str) -> float:
        """
        단어, 문자, 문장, 이모지 반복을 감점하여 0.0~1.0 점수를 계산  
        - self.max_repeat 이하 반복이면 1.0, 이상이면 감점
        """
        words = re.findall(r'\w+', text)
        word_repeats = max([words.count(w) for w in set(words)]) if words else 0

        char_repeats = max([len(m.group(0)) for m in re.finditer(r'((\S{2,5}))\1{1,}', text)]) if re.search(r'((\S{2,5}))\1{1,}', text) else 0

        sents = re.split(r'[.!?]\s*', text)
        sent_repeats = max([sents.count(s) for s in set(sents) if s]) if sents else 0

        emojis = self.emoji_pattern.findall(text)
        emoji_repeats = max([emojis.count(e) for e in set(emojis)]) if emojis else 0

        if max(word_repeats, char_repeats, sent_repeats, emoji_repeats) <= self.max_repeat:
            return 1.0
        rep_penalty = 0.15 if sent_repeats > self.max_repeat else 0
        score = max(0.0, 1.0 - ((max(word_repeats, char_repeats, emoji_repeats) - self.max_repeat) * 0.25 + rep_penalty))
        return round(score, 2)

    def score_emoji_usage(self, text: str) -> float:
        """
        이모지 사용 평가 (개수 기준, 이모지 없음도 0.5점)
        - 0개: 0.5점
        - 1~4개: 1점
        - 5개 이상: 0점
        """
        emojis = self.emoji_pattern.findall(text)
        n = len(emojis)
        if n == 0:
            return 0.5
        elif 1 <= n <= 3:
            return 1.0
        else:  # 4개 이상
            return 0.0

    def score_allowed_chars(self, text: str) -> float:
        """허용 문자/이모지만으로 이뤄진 비율로 0~1.0 점수 계산"""
        if not text:
            return 0.0
        allowed = self.allowed_char_pattern.findall(text)
        ratio = len(''.join(allowed)) / len(text) if len(text) > 0 else 0
        return min(1.0, max(0.0, ratio))


    def evaluate(self, input_path: str):
        """
        입력 파일의 각 줄에 대해 품질 점수(0~1) 딕셔너리 리스트 반환
        """
        results = []
        forbidden_scores, repeat_scores, natural_scores, emoji_scores, total_scores = [], [], [], [], []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                hyp = data.get("transformed_content", "")
                if not isinstance(hyp, str) or not hyp.strip():
                    f_score = r_score = n_score = e_score = total_score = 0.0
                else:
                    f_score = self.score_forbidden_words(hyp)
                    r_score = self.score_repetition(hyp)
                    n_score = self.score_allowed_chars(hyp)
                    e_score = self.score_emoji_usage(hyp)
                    total_score = round((f_score + r_score + n_score + e_score) / 4, 3)
                forbidden_scores.append(f_score)
                repeat_scores.append(r_score)
                natural_scores.append(n_score)
                emoji_scores.append(e_score)
                total_scores.append(total_score)
                results.append({"quality_score": total_score})

        print(f"금지어(비속어) 점수 평균: {sum(forbidden_scores)/len(forbidden_scores):.3f}")
        print(f"반복 점수 평균: {sum(repeat_scores)/len(repeat_scores):.3f}")
        print(f"허용문자 점수 평균: {sum(natural_scores)/len(natural_scores):.3f}")
        print(f"이모지 점수 평균: {sum(emoji_scores)/len(emoji_scores):.3f}")
        print(f"전체 quality_score 평균: {sum(total_scores)/len(total_scores):.3f}")
        return results
        
# 사용 예시
if __name__ == "__main__":
    evaluator = QualityEvaluator()
    mean_quality = evaluator.evaluate("/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/dataset/_dataset/_made/dataset_0515_made.jsonl")
    print(f"최종 quality_score 평균: {mean_quality:.3f}")
