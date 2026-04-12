#only for testing
import requests
payload = {"work_year": 2021, "experience_level": "MI", "employment_type": "FT", "job_title": "Machine Learning Engineer", "employee_residence": "GB", "remote_ratio": 100, "company_location": "GB", "company_size": "M"}

response = requests.post("http://127.0.0.1:8000/predict", json=payload)

if response.status_code == 200:
    result = response.json()
    print(f"Predicted Salary: ${result['predicted_salary_usd']}")
else:
    print(f"Error: {response.status_code} - {response.text}")