import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import requests

load_dotenv()

# Supabase setup
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Mappings
experience_map = {"Entry Level (EN)": 0, "Executive (EX)": 1, "Mid Level (MI)": 2, "Senior (SE)": 3}
employment_map = {"Contract (CT)": 0, "Freelance (FL)": 1, "Full Time (FT)": 2, "Part Time (PT)": 3}
company_size_map = {"Large (L)": 0, "Medium (M)": 1, "Small (S)": 2}
company_location_map = {"AE": 0, "AS": 1, "AT": 2, "AU": 3, "BE": 4, "BR": 5, "CA": 6, "CH": 7, "CL": 8, "CN": 9, "CO": 10, "CZ": 11, "DE": 12, "DK": 13, "DZ": 14, "EE": 15, "ES": 16, "FR": 17, "GB": 18, "GR": 19, "HN": 20, "HR": 21, "HU": 22, "IE": 23, "IL": 24, "IN": 25, "IQ": 26, "IR": 27, "IT": 28, "JP": 29, "KE": 30, "LU": 31, "MD": 32, "MT": 33, "MX": 34, "MY": 35, "NG": 36, "NL": 37, "NZ": 38, "PK": 39, "PL": 40, "PT": 41, "RO": 42, "RU": 43, "SG": 44, "SI": 45, "TR": 46, "UA": 47, "US": 48, "VN": 49}
employee_residence_map = {"AE": 0, "AR": 1, "AT": 2, "AU": 3, "BE": 4, "BG": 5, "BO": 6, "BR": 7, "CA": 8, "CH": 9, "CL": 10, "CN": 11, "CO": 12, "CZ": 13, "DE": 14, "DK": 15, "DZ": 16, "EE": 17, "ES": 18, "FR": 19, "GB": 20, "GR": 21, "HK": 22, "HN": 23, "HR": 24, "HU": 25, "IE": 26, "IN": 27, "IQ": 28, "IR": 29, "IT": 30, "JE": 31, "JP": 32, "KE": 33, "LU": 34, "MD": 35, "MT": 36, "MX": 37, "MY": 38, "NG": 39, "NL": 40, "NZ": 41, "PH": 42, "PK": 43, "PL": 44, "PR": 45, "PT": 46, "RO": 47, "RS": 48, "RU": 49, "SG": 50, "SI": 51, "TN": 52, "TR": 53, "UA": 54, "US": 55, "VN": 56}
job_title_map = {"3D Computer Vision Researcher": 0, "AI Scientist": 1, "Analytics Engineer": 2, "Applied Data Scientist": 3, "Applied Machine Learning Scientist": 4, "BI Data Analyst": 5, "Big Data Architect": 6, "Big Data Engineer": 7, "Business Data Analyst": 8, "Cloud Data Engineer": 9, "Computer Vision Engineer": 10, "Computer Vision Software Engineer": 11, "Data Analyst": 12, "Data Analytics Engineer": 13, "Data Analytics Lead": 14, "Data Analytics Manager": 15, "Data Architect": 16, "Data Engineer": 17, "Data Engineering Manager": 18, "Data Science Consultant": 19, "Data Science Engineer": 20, "Data Science Manager": 21, "Data Scientist": 22, "Data Specialist": 23, "Director of Data Engineering": 24, "Director of Data Science": 25, "ETL Developer": 26, "Finance Data Analyst": 27, "Financial Data Analyst": 28, "Head of Data": 29, "Head of Data Science": 30, "Head of Machine Learning": 31, "Lead Data Analyst": 32, "Lead Data Engineer": 33, "Lead Data Scientist": 34, "Lead Machine Learning Engineer": 35, "ML Engineer": 36, "Machine Learning Developer": 37, "Machine Learning Engineer": 38, "Machine Learning Infrastructure Engineer": 39, "Machine Learning Manager": 40, "Machine Learning Scientist": 41, "Marketing Data Analyst": 42, "NLP Engineer": 43, "Principal Data Analyst": 44, "Principal Data Engineer": 45, "Principal Data Scientist": 46, "Product Data Analyst": 47, "Research Scientist": 48, "Staff Data Scientist": 49}

st.title("Salary Prediction Dashboard")

# --- Prediction Form ---
st.subheader("Predict a Salary")

work_year = st.selectbox("Work Year", [2020, 2021, 2022])
experience = st.selectbox("Experience Level", list(experience_map.keys()))
employment = st.selectbox("Employment Type", list(employment_map.keys()))
job_title = st.selectbox("Job Title", list(job_title_map.keys()))
employee_residence = st.selectbox("Employee Residence", list(employee_residence_map.keys()))
remote_ratio = st.selectbox("Remote Ratio", [0, 50, 100])
company_location = st.selectbox("Company Location", list(company_location_map.keys()))
company_size = st.selectbox("Company Size", list(company_size_map.keys()))

if st.button("Predict"):
    payload = {
        "work_year": work_year,
        "experience_level": experience_map[experience],
        "employment_type": employment_map[employment],
        "job_title": job_title_map[job_title],
        "employee_residence": employee_residence_map[employee_residence],
        "remote_ratio": remote_ratio,
        "company_location": company_location_map[company_location],
        "company_size": company_size_map[company_size]
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    if response.status_code == 200:
        salary = response.json()["predicted_salary_usd"]
        st.success(f"Predicted Salary: ${salary}")
    else:
        st.error("Error getting prediction.")

st.divider()

# --- Past Predictions ---
st.subheader("Past Predictions")
db_response = supabase.table("predictions").select("*").execute()
data = db_response.data

if not data:
    st.warning("No predictions found yet.")
else:
    df = pd.DataFrame(data)
    st.dataframe(df[["work_year", "experience_level", "employment_type",
                      "remote_ratio", "company_size", "predicted_salary", "created_at"]])

    st.subheader("Predicted Salaries Over Time")
    st.line_chart(df[["predicted_salary"]])

    st.subheader("LLM Analysis")
    for _, row in df.iterrows():
        st.markdown(f"**Predicted Salary:** ${row['predicted_salary']}")
        st.write(row["llm_analysis"])
        st.divider()