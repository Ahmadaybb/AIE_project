import requests

# Example input
payload = {
    "work_year": 2022,
    "experience_level": 2,
    "employment_type": 1,
    "job_title": 3,
    "employee_residence": 2,
    "remote_ratio": 100,
    "company_location": 2,
    "company_size": 1
}

response = requests.post("http://127.0.0.1:8000/predict", json=payload)

if response.status_code == 200:
    result = response.json()
    print(f"Predicted Salary: ${result['predicted_salary_usd']}")
else:
    print(f"Error: {response.status_code} - {response.text}")