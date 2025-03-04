import torch
import torch.nn as nn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import model
import json

app = FastAPI()
router = APIRouter()


# JSON 파일 로드
with open("Pytorch/data.json", "r") as f:
    data = json.load(f)

# 모델 생성 및 학습

models = {} 
@router.get("/model/{model_name}") 
def model_select(model_name): # JSON 파일의 키 값으로 모델 생성
    input_dim = len(data[model_name]["data"][0]) # 입력 데이터의 차원 확인
    models[model_name] = model.create_model(input_dim) # 모델 생성

# 모델 학습 함수 정의
def train_model(model, data, labels, epochs=10000, lr=0.1):
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        outputs = model(data)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 1000 == 0:
            print(f'Epoch: {epoch}, Loss: {loss.item()}')

# 모델 학습
for model_name, model_instance in models.items():
    data_tensor = torch.tensor(data[model_name]["data"], dtype=torch.float32)
    labels_tensor = torch.tensor(data[model_name]["labels"], dtype=torch.float32)
    train_model(model_instance, data_tensor, labels_tensor)

# FastAPI 라우터 설정
router = APIRouter()

class InputData(BaseModel):
    x1: int
    x2: int = 0  # NOT 연산의 경우 x2는 사용되지 않음

@router.post("/{operation}")
def predict(operation: str, data: InputData):
    model_instance = models.get(operation)
    if not model_instance:
        return {"error": "Invalid operation"}
    
    input_data = [data.x1]
    if operation != "not":
        input_data.append(data.x2)
    input_tensor = torch.tensor([input_data], dtype=torch.float32)

    output = model_instance(input_tensor)
    prediction = (output > 0.5).int().item()
    return {"prediction": prediction}

# FastAPI 앱 생성 및 라우터 등록
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}