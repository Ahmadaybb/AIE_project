import requests
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

# Supabase setup
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_prediction(payload):
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    if response.status_code == 200:
        return response.json()["predicted_salary_usd"]
    else:
        raise Exception(f"API error: {response.status_code}")

def get_llm_analysis(salary, payload):
    prompt = f"""
    You are a data analyst. A data science job has been analyzed with the following details:
    - Work Year: {payload['work_year']}
    - Experience Level: {payload['experience_level']}
    - Employment Type: {payload['employment_type']}
    - Remote Ratio: {payload['remote_ratio']}
    - Company Size: {payload['company_size']}
    
    The predicted salary is ${salary}.
    
    Write a short narrative insight about this salary prediction.
    What does it tell us about the data science job market?
    """

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]

def save_to_supabase(payload, salary, analysis):
    data = {
        "work_year": payload["work_year"],
        "experience_level": payload["experience_level"],
        "employment_type": payload["employment_type"],
        "job_title": payload["job_title"],
        "employee_residence": payload["employee_residence"],
        "remote_ratio": payload["remote_ratio"],
        "company_location": payload["company_location"],
        "company_size": payload["company_size"],
        "predicted_salary": salary,
        "llm_analysis": analysis
    }
    supabase.table("predictions").insert(data).execute()
    print("Saved to Supabase.")

# Example input
payload = {
    "work_year": 2019,
    "experience_level": 4,
    "employment_type": 2,
    "job_title": 4,
    "employee_residence": 4,
    "remote_ratio": 100,
    "company_location": 3,
    "company_size": 1
}

salary = get_prediction(payload)
print(f"Predicted Salary: ${salary}")

analysis = get_llm_analysis(salary, payload)
print(f"\nLLM Analysis:\n{analysis}")

save_to_supabase(payload, salary, analysis)