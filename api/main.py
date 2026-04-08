from fastapi import FastAPI
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

@app.post("/predict")
def predict(input: JobInput):
    data = {
        "work_year": input.work_year,
        "experience_level": encoders["experience_level"].transform([input.experience_level])[0],
        "employment_type": encoders["employment_type"].transform([input.employment_type])[0],
        "job_title": encoders["job_title"].transform([input.job_title])[0],
        "employee_residence": encoders["employee_residence"].transform([input.employee_residence])[0],
        "remote_ratio": input.remote_ratio,
        "company_location": encoders["company_location"].transform([input.company_location])[0],
        "company_size": encoders["company_size"].transform([input.company_size])[0],
    }

    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"predicted_salary_usd": round(prediction, 2)}