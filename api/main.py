from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

# Load model and encoders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "models", "model.joblib"))
encoders = joblib.load(os.path.join(BASE_DIR, "models", "encoders.joblib"))

# Define the input schema with real names
class JobInput(BaseModel):
    work_year: int
    experience_level: str
    employment_type: str
    job_title: str
    employee_residence: str
    remote_ratio: int
    company_location: str
    company_size: str

def encode(column, value):
    known_values = list(encoders[column].classes_)
    if value not in known_values:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown value '{value}' for '{column}'. Please use known values: {known_values}"
        )
    return encoders[column].transform([value])[0]

@app.post("/predict")
def predict(input: JobInput):
    data = {
        "work_year": input.work_year,
        "experience_level": encode("experience_level", input.experience_level),
        "employment_type": encode("employment_type", input.employment_type),
        "job_title": encode("job_title", input.job_title),
        "employee_residence": encode("employee_residence", input.employee_residence),
        "remote_ratio": input.remote_ratio,
        "company_location": encode("company_location", input.company_location),
        "company_size": encode("company_size", input.company_size),
    }

    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"predicted_salary_usd": round(prediction, 2)}