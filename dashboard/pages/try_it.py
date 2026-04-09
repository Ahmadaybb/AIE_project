import streamlit as st
import requests
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Try the Predictor", page_icon="🎯")

API_URL = os.getenv("API_URL", "https://aie-project.onrender.com")

@st.cache_resource
def get_groq():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

client = get_groq()

st.title("🎯 Salary Predictor")
st.markdown("Fill in the role details to get an instant market salary estimate.")

EXPERIENCE_MAP = {
    "Entry Level": "EN",
    "Mid Level": "MI",
    "Senior": "SE",
    "Executive": "EX"
}

EMPLOYMENT_MAP = {
    "Full Time": "FT",
    "Part Time": "PT",
    "Contract": "CT",
    "Freelance": "FL"
}

COMPANY_SIZE_MAP = {
    "Small (< 50 employees)": "S",
    "Medium (50-250 employees)": "M",
    "Large (> 250 employees)": "L"
}

REMOTE_MAP = {
    "On-site": 0,
    "Hybrid": 50,
    "Fully Remote": 100
}

JOB_TITLES = [
    "Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer",
    "Machine Learning Engineer", "Research Scientist", "Analytics Engineer",
    "Director of Data Science", "Head of Data", "AI Scientist",
    "Business Data Analyst", "Data Science Manager", "Lead Data Scientist"
]

LOCATIONS = {
    "United States": "US",
    "United Kingdom": "GB",
    "Germany": "DE",
    "France": "FR",
    "India": "IN",
    "Canada": "CA",
    "Spain": "ES",
    "Australia": "AU"
}

st.divider()

col1, col2 = st.columns(2)

with col1:
    job_title = st.selectbox("Job Title", JOB_TITLES)
    experience = st.selectbox("Experience Level", list(EXPERIENCE_MAP.keys()))
    employment = st.selectbox("Employment Type", list(EMPLOYMENT_MAP.keys()))

with col2:
    residence = st.selectbox("Employee Location", list(LOCATIONS.keys()))
    company_location = st.selectbox("Company Location", list(LOCATIONS.keys()))
    company_size = st.selectbox("Company Size", list(COMPANY_SIZE_MAP.keys()))
    remote = st.selectbox("Work Arrangement", list(REMOTE_MAP.keys()))

st.divider()
st.caption("ℹ️ Salary estimates are based on data science job market data from 2020–2022. Results reflect market trends from that period.")

if st.button("Get Salary Estimate", type="primary"):
    payload = {
        "work_year": 2022,
        "experience_level": EXPERIENCE_MAP[experience],
        "employment_type": EMPLOYMENT_MAP[employment],
        "job_title": job_title,
        "employee_residence": LOCATIONS[residence],
        "remote_ratio": REMOTE_MAP[remote],
        "company_location": LOCATIONS[company_location],
        "company_size": COMPANY_SIZE_MAP[company_size]
    }

    response = requests.post(f"{API_URL}/predict", json=payload)

    if response.status_code == 200:
        salary = response.json()["predicted_salary_usd"]
        st.success(f"Estimated Market Salary: **${salary:,.2f} USD/year**")
        st.caption(f"For a {experience} {job_title} based in {residence}, working {remote.lower()} at a {company_size.split('(')[0].strip().lower()} company.")

        with st.spinner("Generating AI explanation..."):
            prompt = f"""
You are a salary analyst. Explain in 2-3 short paragraphs why a {experience} {job_title} 
based in {residence}, working {remote.lower()} at a {company_size.split('(')[0].strip().lower()} company
would earn ${salary:,.2f} USD per year.

Be specific about how location, experience, and role affect the salary.
Keep it friendly and easy to understand for an HR manager.
"""
            st.markdown("#### Why this salary?")
            placeholder = st.empty()
            full_text = ""

            stream = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    placeholder.markdown(full_text)
    else:
        st.error(f"Could not get prediction. Error: {response.text}")