from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI()

# Load the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "models", "model.pkl"), "rb") as f:
    model = pickle.load(f)

# Define the input schema
class JobInput(BaseModel):
    work_year: int
    experience_level: int
    employment_type: int
    job_title: int
    employee_residence: int
    remote_ratio: int
    company_location: int
    company_size: int

@app.post("/predict")
def predict(input: JobInput):
    data = pd.DataFrame([input.dict()])
    prediction = model.predict(data)[0]
    return {"predicted_salary_usd": round(prediction, 2)}