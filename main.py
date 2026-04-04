from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import uvicorn
import os
from mangum import Mangum
from src.make_dataset import data_preparation


model_features = [
    "SEX",
    "PAY_1",
    "AGE",
    "LIMIT_BAL",
    "CV_LPAY_TOT",
    "CV_LBILL_TOT",
    "CANT_PAY_MAY0",
    "BILL_AMT1",
    "LOG_BILL_AMT1",
    "AVG_LPAY_TOT",
    "STD_PAY_TOT",
    "AVG_EXP_1",
]


# call the app
app = FastAPI(title="API")
handler=Mangum(app)


# Load the model and scaler
with open("models/best_model.pkl", "rb") as f1:
    model = pickle.load(f1)


class Customer(BaseModel):
    LIMIT_BAL: int
    SEX: int
    AGE: int
    PAY_1: int
    PAY_2: int
    PAY_3: int
    PAY_4: int
    PAY_5: int
    PAY_6: int
    BILL_AMT1: int
    BILL_AMT2: int
    BILL_AMT3: int
    BILL_AMT4: int
    BILL_AMT5: int
    BILL_AMT6: int
    PAY_AMT1: int
    PAY_AMT2: int
    PAY_AMT3: int
    PAY_AMT4: int
    PAY_AMT5: int
    PAY_AMT6: int


# Ouput for data validation
class Output(BaseModel):
    label: str
    prediction: int
    

# Endpoints
# Root Endpoint
@app.get("/")
def root():
    return {"API": "Este es un modelo para predecir Default."}


# Prediction endpoint
@app.post("/predict")
def predict_default(subject: Customer):
    # Make prediction
    
    data = pd.DataFrame(subject.dict(), index=[0])
    datan = data_preparation(data)
    prediction = model.predict(datan[model_features])
    result = "No es Default" if prediction[0] == 1 else "Es Default"
    return JSONResponse({"Predicción": result})
    

# App Health
@app.get('/health')
async def service_health():
    """Return service health"""
    return {"ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
