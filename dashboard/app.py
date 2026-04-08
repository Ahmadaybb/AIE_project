import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import matplotlib.pyplot as plt

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("Data Science Salary Predictor")
st.markdown("Predict salaries for data science roles and explore insights.")

# --- Prediction Form ---
st.subheader("Make a Prediction")

col1, col2 = st.columns(2)

with col1:
    work_year = st.selectbox("Work Year", [2020, 2021, 2022])
    experience_level = st.selectbox("Experience Level", ["EN", "MI", "SE", "EX"])
    employment_type = st.selectbox("Employment Type", ["FT", "PT", "CT", "FL"])
    job_title = st.selectbox("Job Title", [
        "Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer",
        "Machine Learning Engineer", "Research Scientist", "Analytics Engineer",
        "Director of Data Science", "Head of Data", "AI Scientist"
    ])

with col2:
    employee_residence = st.selectbox("Employee Residence", ["US", "GB", "DE", "FR", "IN", "CA", "ES", "AU"])
    remote_ratio = st.selectbox("Remote Ratio", [0, 50, 100])
    company_location = st.selectbox("Company Location", ["US", "GB", "DE", "FR", "IN", "CA", "ES", "AU"])
    company_size = st.selectbox("Company Size", ["S", "M", "L"])

if st.button("Predict Salary"):
    payload = {
        "work_year": work_year,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "job_title": job_title,
        "employee_residence": employee_residence,
        "remote_ratio": remote_ratio,
        "company_location": company_location,
        "company_size": company_size
    }
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    if response.status_code == 200:
        salary = response.json()["predicted_salary_usd"]
        st.success(f"Predicted Salary: ${salary:,.2f}")
    else:
        st.error(f"Error: {response.text}")

st.divider()

# --- Past Predictions ---
st.subheader("Past Predictions")
db_response = supabase.table("predictions").select("*").execute()
data = db_response.data

if not data:
    st.warning("No predictions found yet.")
else:
    df = pd.DataFrame(data)

    st.dataframe(df[["job_title", "experience_level", "employee_residence",
                      "remote_ratio", "company_size", "predicted_salary", "created_at"]])

    st.subheader("Salary by Job Title")
    fig, ax = plt.subplots()
    df.groupby("job_title")["predicted_salary"].mean().sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Predicted Salary (USD)")
    st.pyplot(fig)

    st.subheader("LLM Analysis")
    latest = df.iloc[-1]
    st.write(latest["llm_analysis"])