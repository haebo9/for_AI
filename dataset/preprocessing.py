import json
import re
from typing import Dict, Any
from collections import Counter, defaultdict

# 이모티콘 정규표현식 패턴(상수로 선언)
EMOJI_PATTERN = (
    "[" +
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002700-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U00002600-\U000026FF"
    "]"
)

# 텍스트에 해시태그가 포함되어 있는지 확인
def contains_hashtags(text: str) -> bool:
    """해시태그가 포함되어 있는지 확인"""
    return bool(re.search(r'#\S+', text))

# 텍스트에 이모티콘이 max_emojis개 이상 포함되어 있는지 확인
def contains_many_emojis(text: str, max_emojis: int = 4) -> bool:
    """이모티콘이 max_emojis개 이상 포함되어 있는지 확인"""
    emoji_re = re.compile(EMOJI_PATTERN, flags=re.UNICODE)
    return len(re.findall(emoji_re, text)) > max_emojis

# 텍스트에 이모티콘이 연속적으로 consecutive개 이상 사용되었는지 확인
def contains_consecutive_emojis(text: str, consecutive: int = 3) -> bool:
    """이모티콘이 연속적으로 consecutive개 이상 사용되었는지 확인"""
    pattern = re.compile(EMOJI_PATTERN + "{" + str(consecutive) + ",}", flags=re.UNICODE)
    return bool(pattern.search(text))

# 텍스트가 한글 또는 영문 대소문자가 아닌 문자로 시작하는지 확인
def starts_with_non_alpha(text: str) -> bool:
    """문자가 아닌 것으로 시작하는지 확인"""
    text = text.strip()
    return not bool(re.match(r'^[A-Za-z가-힣]', text))

# transformed_content가 content의 1.5배를 초과하는지 확인
def transformed_too_long(data: Dict) -> bool:
    """transformed_content가 content의 1.5배를 초과하는지 확인"""
    content = data.get('content', '')
    transformed = data.get('transformed_content', '')
    if content and transformed:
        return len(transformed) > 1.5 * len(content)
    return False

# 텍스트에서 동일한 단어가 4번 이상 반복되는지 확인
def contains_repeated_word(text: str, repeat: int = 4) -> bool:
    """
    동일한 단어가 repeat번 이상 반복되는지 확인
    """
    words = re.findall(r'\b\w+\b', text)
    word_counts = Counter(words)
    return any(count >= repeat for count in word_counts.values())

# 데이터가 위의 문제 조건 중 하나라도 해당되면 True 반환
def is_problematic_data(data: Dict) -> bool:
    """데이터가 문제 조건에 해당하는지 확인"""
    for key in ['content', 'transformed_content']:
        if key in data:
            text = data[key]
            if (
                contains_hashtags(text)
                or contains_many_emojis(text)
                or contains_consecutive_emojis(text)
                or starts_with_non_alpha(text)
                or contains_repeated_word(text)
            ):
                return True
    if transformed_too_long(data):
        return True
    return False

# 텍스트에서 \\r\\n, \\r, \\n, \r, \n 모두 제거 (정규표현식 사용)
def remove_all_backslash_and_newline(text: str) -> str:
    """
    텍스트에서 이스케이프된 줄바꿈(\\r\\n, \\r, \\n)과 실제 줄바꿈(\r, \n) 모두 제거
    """
    return re.sub(r'(\\r\\n|\\r|\\n|\r|\n)', '', text)

# 연속된 이모티콘 그룹에서 맨 앞의 이모티콘만 남기고 나머지는 제거
def keep_only_first_emoji_in_consecutive(text: str) -> str:
    """
    연속적으로 등장하는 이모티콘 그룹에서 맨 앞의 이모티콘만 남기고 나머지는 제거
    """
    return re.sub(f"({EMOJI_PATTERN}){EMOJI_PATTERN}+", r"\1", text)

# 데이터셋을 읽고, 필터링 조건에 맞지 않는 데이터만 저장
def filter_data(input_path: str, output_path: str) -> None:
    """
    1. 각 줄을 json으로 읽음
    2. 필터 조건에 해당하는 데이터는 제외
    3. 저장 직전에 content, transformed_content에서 \\r\\n, \\r, \\n, \r, \n 모두 제거
    4. 연속된 이모티콘 그룹은 맨 앞 이모티콘만 남김
    5. 새로운 파일로 저장
    """
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                data = json.loads(line)
            except Exception as e:
                print(f"JSON 파싱 오류: {e}")
                continue
            if not is_problematic_data(data):
                for key in ['content', 'transformed_content']:
                    if key in data:
                        # 1. 백슬래시 및 줄바꿈 문자 제거
                        cleaned = remove_all_backslash_and_newline(data[key])
                        # 2. 연속 이모티콘 그룹은 맨 앞만 남김
                        cleaned = keep_only_first_emoji_in_consecutive(cleaned)
                        data[key] = cleaned
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')

# 데이터셋 통계 출력 함수
def analyze_label_counts(output_path: str) -> None:
    """
    emotion의 종류별 개수, post_type의 종류별 개수만 출력
    """
    emotion_counter = Counter()
    post_type_counter = Counter()

    with open(output_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if 'emotion' in data:
                emotion_counter[data['emotion']] += 1
            if 'post_type' in data:
                post_type_counter[data['post_type']] += 1

    print("\n--- emotion 종류별 개수 ---")
    for value, count in emotion_counter.items():
        print(f"{value}: {count}")

    print("\n--- post_type 종류별 개수 ---")
    for value, count in post_type_counter.items():
        print(f"{value}: {count}")

# 경로 설정
import os

root_path = "/Users/jaeseoksee/Documents/project/dataset/_dataset/"
input_file_path = os.path.join(root_path, 'dataset_0527_made.jsonl')
output_file_path = os.path.join(root_path, 'filtered_dataset.jsonl')

# 필터링 실행
filter_data(input_file_path, output_file_path)
print("✅ 필터링 완료 및 새로운 파일 생성 완료")

# 데이터셋 통계 출력
analyze_label_counts(output_file_path)