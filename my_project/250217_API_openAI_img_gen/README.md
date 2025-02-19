### 이미지 생성 by OpenAI api 
- 스케마 
    1. openAI 요청: 개인 OPENAI key입력
    2. 함수 정의: get_text, get_image, analyze_image
    3. 텍스트 생성 : 생성할 이미지에 대한 정보를 텍스트로 입력한 다음 이미지 생성을 위한 프폼프트 생성 : gpt-4o-mini 
    4. 이미지 생성 : 입력된 프롬프트를 기반으로 이미지 생성: DALL-E-3 
    5. 이미지 분석 : 생성된 이미지 url을 입력받아 해당 이미지의 정보 요약 출력 : gpt-4o-mini
    6. 이미지 저장 : url의 이미지를 불러와 로컬에 저장

![생성된 이미지 예시](https://github.com/haebo9/for_AI/blob/main/my_project/250217_API_openAI_img_gen/result/DALE_image_cat6.png)