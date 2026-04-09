import requests
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

job_combinations = [
    {"work_year": 2022, "experience_level": "SE", "employment_type": "FT", "job_title": "Data Scientist", "employee_residence": "US", "remote_ratio": 100, "company_location": "US", "company_size": "L"},
    {"work_year": 2022, "experience_level": "EN", "employment_type": "FT", "job_title": "Data Analyst", "employee_residence": "US", "remote_ratio": 0, "company_location": "US", "company_size": "S"},
    {"work_year": 2022, "experience_level": "MI", "employment_type": "FT", "job_title": "ML Engineer", "employee_residence": "GB", "remote_ratio": 50, "company_location": "GB", "company_size": "M"},
    {"work_year": 2022, "experience_level": "SE", "employment_type": "FT", "job_title": "Data Engineer", "employee_residence": "DE", "remote_ratio": 100, "company_location": "DE", "company_size": "L"},
    {"work_year": 2022, "experience_level": "EX", "employment_type": "FT", "job_title": "Director of Data Science", "employee_residence": "US", "remote_ratio": 100, "company_location": "US", "company_size": "L"},
]

def get_prediction(payload):
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    if response.status_code == 200:
        return response.json()["predicted_salary_usd"]
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")

def get_llm_analysis(salary, payload):
    prompt = f"""
You are a salary analyst. Explain in 2-3 short paragraphs why a {payload['experience_level']} {payload['job_title']} 
based in {payload['employee_residence']}, working with {payload['remote_ratio']}% remote at a {payload['company_size']} company
would earn ${salary:,.2f} USD per year.

Be specific about how location, experience, and role affect the salary.
Keep it friendly and easy to understand for an HR manager.
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

# Run each prediction individually
for combo in job_combinations:
    salary = get_prediction(combo)
    print(f"{combo['job_title']} ({combo['experience_level']}, {combo['employee_residence']}): ${salary:,.2f}")

    analysis = get_llm_analysis(salary, combo)
    print(f"Analysis: {analysis[:100]}...")

    save_to_supabase(combo, salary, analysis)
    print("Saved.\n")

print("All done.")