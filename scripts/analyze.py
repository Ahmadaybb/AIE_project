import requests
from supabase import create_client
from dotenv import load_dotenv
import os
import json

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Multiple input combinations to predict
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

def get_llm_analysis(predictions_summary):
    prompt = f"""
You are a data analyst writing a report about data science salaries around the world.

Here are salary predictions for different data science roles:
{predictions_summary}

Write a compelling narrative (3-4 paragraphs) that:
1. Highlights the key differences in salaries across roles, experience levels, and locations
2. Tells a story about what drives salary in data science
3. Points out the most surprising finding

Be specific, use the numbers, and make it interesting to read.
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

# Run predictions
results = []
for combo in job_combinations:
    salary = get_prediction(combo)
    print(f"{combo['job_title']} ({combo['experience_level']}, {combo['employee_residence']}): ${salary:,.2f}")
    results.append({**combo, "salary": salary})

# Build summary for LLM
summary = "\n".join([
    f"- {r['job_title']} | {r['experience_level']} | {r['employee_residence']} | ${r['salary']:,.2f}"
    for r in results
])

# Get one narrative for all predictions
print("\nGenerating LLM analysis...")
analysis = get_llm_analysis(summary)
print(f"\nLLM Analysis:\n{analysis}")

# Save each prediction with the shared analysis
for r in results:
    save_to_supabase(r, r["salary"], analysis)

print("\nAll saved to Supabase.")