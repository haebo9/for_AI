from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import Pytorch.model as model

app = FastAPI()

# 모델 인스턴스 생성 및 학습 (서버 시작 시 한 번만 실행)
and_perceptron = model.AndPerceptron()
not_perceptron = model.NotPerceptron()
xor_perceptron = model.XorPerceptron()

and_perceptron.train(np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([[0], [0], [0], [1]]))
not_perceptron.train(np.array([[0], [1]]), np.array([[1], [0]]))
xor_perceptron.train(np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([[0], [1], [1], [0]]))

# 입력 데이터 모델 정의 (Pydantic 사용)
class InputData(BaseModel):
    input: list

@app.post("/and")
async def and_route(data: InputData):
    if len(data.input) != 2:
        raise HTTPException(status_code=400, detail="Invalid input. Input should be a list of two numbers.")
    try:
        prediction = and_perceptron.predict(data.input)
        return {"result": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/not")
async def not_route(data: InputData):
    if len(data.input) != 1:
        raise HTTPException(status_code=400, detail="Invalid input. Input should be a list of one number.")
    try:
        prediction = not_perceptron.predict([data.input[0]])  # NOT 연산은 입력값이 하나이므로 리스트의 첫 번째 요소만 사용
        return {"result": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/xor")
async def xor_route(data: InputData):
    if len(data.input) != 2:
        raise HTTPException(status_code=400, detail="Invalid input. Input should be a list of two numbers.")
    try:
        prediction = xor_perceptron.predict(data.input)
        return {"result": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))