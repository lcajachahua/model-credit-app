from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import uvicorn
import os
from src.make_dataset import data_preparation

# call the app
app = FastAPI(title="API")

# Load the model and scaler
def load_model():
    with open("models/best_model.pkl", "rb") as f1:
        return pickle.load(f1)

model = load_model()

def predict_def(df, endpoint="simple"):
    # Prediction
    prediction = model.predict_proba(df)
    highest_proba = prediction.max(axis=1)
    predicted_labels = ["No es Default" if i == 0 else f"Es Default" for i in highest_proba]
    print(f"Predicted labels: {predicted_labels}")
    print(highest_proba)
    response = []
    for label, proba in zip(predicted_labels, highest_proba):
        output = {
            "prediction": label,
            "probability of prediction": str(round(proba * 100)) + '%'
        }
        response.append(output)
    return response


class Customer(BaseModel):
    LIMIT_BAL: int
    SEX: int
    MARRIAGE: int
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
@app.post("/predict", response_model=Output)
def predict_default(subject: Customer):
    # Make prediction
    data = pd.DataFrame(subject.dict(), index=[0])
    datan = data_preparation(data)
    parsed = predict_def(df=datan)
    return {"Output": parsed}


# App Health
@app.get('/health')
async def service_health():
    """Return service health"""
    return {"ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
