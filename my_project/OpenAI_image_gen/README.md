> 이미지 생성 by OpenAI api 스케마
- openAI 요청: 개인 OPENAI key입력
- 함수 정의: get_text, get_image, analyze_image
- 텍스트 생성 : 생성할 이미지에 대한 정보를 텍스트로 입력한 다음 이미지 생성을 위한 프폼프트 생성 : gpt-4o-mini 
- 이미지 생성 : 입력된 프롬프트를 기반으로 이미지 생성: DALL-E-3 
- 이미지 분석 : 생성된 이미지 url을 입력받아 해당 이미지의 정보 요약 출력 : gpt-4o-mini
- 이미지 저장 : url의 이미지를 불러와 로컬에 저장
    
<img src="https://github.com/haebo9/for_AI/blob/main/my_project/250217_openai-img-generation/result/DALE_image_cat5.png" width="300" height="auto" alt="생성된 이미지">

> 이미지 분석 결과
- 이 이미지는 교실 장면을 보여줍니다.  
- 하얀 고양이가 수업을 하고 있으며, 칠판 앞에 서 있습니다.  
- 칠판에는 수학 방정식과 기하학적 도형이 가득 적혀 있습니다.  
- 고양이는 포인터를 들고, 보드의 내용을 설명하는 듯 보입니다.  
- 고양이 앞에는 갈색 고양이가 책상에 앉아 있으며, 주의 깊게 듣고 있는 모습입니다.  
- 책상 위에는 열려 있는 책들과 메모, 수학 공식들이 있습니다.  
- 전체적인 분위기는 기발하고 유머러스하며, 전형적인 교실 환경과 의인화된 고양이들이 결합되어 있습니다.
