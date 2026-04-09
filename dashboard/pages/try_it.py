import streamlit as st
import requests
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Try the Predictor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = os.getenv("API_URL", "https://aie-project.onrender.com")

@st.cache_resource
def get_groq():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_groq()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* BASE — matches config.toml so there is no flash */
  .stApp { background-color: #0A1628 !important; color: #E8F0FE; }
  .main .block-container { padding: 2.5rem 3rem 4rem; max-width: 1100px; }

  /* ── SIDEBAR ── */
  [data-testid="stSidebar"] {
      background-color: #0D1F35 !important;
      border-right: 1px solid #1E3A5F;
  }
  section[data-testid="stSidebar"] > div:first-child { padding-top: 28px; }

  /* Sidebar nav links — bigger, clearer */
  [data-testid="stSidebarNavLink"] {
      color: #8892A4 !important;
      border-radius: 8px !important;
      padding: 10px 16px !important;
      font-size: 15px !important;
      font-weight: 500 !important;
      transition: all 0.15s !important;
      margin-bottom: 2px !important;
  }
  [data-testid="stSidebarNavLink"]:hover {
      background: rgba(0,212,170,0.08) !important;
      color: #00D4AA !important;
  }
  [data-testid="stSidebarNavLink"][aria-selected="true"] {
      background: rgba(0,212,170,0.13) !important;
      color: #00D4AA !important;
      font-weight: 700 !important;
  }
  /* Sidebar toggle button (the ›/‹ arrow) */
  [data-testid="collapsedControl"] {
      color: #00D4AA !important;
  }

  /* ── TYPOGRAPHY ── */
  h1, h2, h3, h4 { color: #E8F0FE !important; }
  p { color: #B0BAC8; }
  hr { border-color: #1A2B3C !important; margin: 20px 0 !important; }

  /* ── SELECTBOX LABEL ── */
  [data-testid="stSelectbox"] label {
      color: #8892A4 !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.8px !important;
  }
  /* Selectbox control */
  [data-testid="stSelectbox"] > div > div {
      background-color: #112240 !important;
      border: 1px solid #1E3A5F !important;
      color: #E8F0FE !important;
      border-radius: 8px !important;
      font-size: 14px !important;
      transition: border-color 0.15s !important;
  }
  [data-testid="stSelectbox"] > div > div:focus-within {
      border-color: #00D4AA !important;
      box-shadow: 0 0 0 3px rgba(0,212,170,0.12) !important;
  }

  /* ── PRIMARY BUTTON ── */
  .stButton > button[kind="primary"] {
      background: #112240 !important;
      color: #0A1628 !important;
      border: none !important;
      font-weight: 800 !important;
      font-size: 16px !important;
      padding: 14px 32px !important;
      border-radius: 8px !important;
      width: 100% !important;
      letter-spacing: 0.4px !important;
      transition: all 0.2s !important;
  }
  .stButton > button[kind="primary"]:hover {
      background: #04d4aa !important;
      box-shadow: 0 4px 28px rgba(0,212,170,0.35) !important;
      transform: translateY(-1px);
  }
  .stButton > button[kind="primary"]:active {
      transform: translateY(0px);
  }

  /* ── SPINNER ── */
  .stSpinner > div { border-top-color: #00D4AA !important; }

  /* ── HIDE BRANDING ── */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 36px;">
    <div style="
        display: inline-flex; align-items: center; gap: 7px;
        background: rgba(0,212,170,0.09); border: 1px solid rgba(0,212,170,0.25);
        color: #00D4AA; font-size: 11px; font-weight: 700; letter-spacing: 1.3px;
        text-transform: uppercase; padding: 5px 14px; border-radius: 20px; margin-bottom: 18px;
    ">🎯 Salary Predictor</div>
    <h1 style="
        font-size: 38px; font-weight: 800; margin: 0 0 12px 0;
        color: #E8F0FE; letter-spacing: -0.5px; line-height: 1.15;
    ">Get Your <span style="color:#00D4AA;">Salary Estimate</span></h1>
    <p style="font-size: 16px; color: #8892A4; margin: 0; line-height: 1.6; max-width: 520px;">
        Configure the role below and get an instant market salary estimate powered by machine learning.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Data maps ─────────────────────────────────────────────────────────────────
EXPERIENCE_MAP   = {"Entry Level": "EN", "Mid Level": "MI", "Senior": "SE", "Executive": "EX"}
EMPLOYMENT_MAP   = {"Full Time": "FT", "Part Time": "PT", "Contract": "CT", "Freelance": "FL"}
COMPANY_SIZE_MAP = {"Small (< 50 employees)": "S", "Medium (50-250 employees)": "M", "Large (> 250 employees)": "L"}
REMOTE_MAP       = {"On-site": 0, "Hybrid": 50, "Fully Remote": 100}
JOB_TITLES = [
    "Data Scientist", "Data Analyst", "Data Engineer", "ML Engineer",
    "Machine Learning Engineer", "Research Scientist", "Analytics Engineer",
    "Director of Data Science", "Head of Data", "AI Scientist",
    "Business Data Analyst", "Data Science Manager", "Lead Data Scientist",
]
LOCATIONS = {
    "United States": "US", "United Kingdom": "GB", "Germany": "DE",
    "France": "FR", "India": "IN", "Canada": "CA", "Spain": "ES", "Australia": "AU",
}

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    font-size: 11px; font-weight: 700; color: #00D4AA;
    text-transform: uppercase; letter-spacing: 1.3px; margin-bottom: 16px;
">Role Details</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    job_title  = st.selectbox("Job Title", JOB_TITLES)
    experience = st.selectbox("Experience Level", list(EXPERIENCE_MAP.keys()))
    employment = st.selectbox("Employment Type", list(EMPLOYMENT_MAP.keys()))

with col2:
    residence        = st.selectbox("Employee Location", list(LOCATIONS.keys()))
    company_location = st.selectbox("Company Location", list(LOCATIONS.keys()))
    company_size     = st.selectbox("Company Size", list(COMPANY_SIZE_MAP.keys()))
    remote           = st.selectbox("Work Arrangement", list(REMOTE_MAP.keys()))

st.markdown("""
<p style="font-size: 12px; color: #3D4F62; margin: 14px 0 22px; line-height: 1.5;">
    ℹ️ Salary estimates are based on data science job market data from 2020–2022.
    Results reflect market trends from that period.
</p>
""", unsafe_allow_html=True)

# ── Submit ────────────────────────────────────────────────────────────────────
if st.button("Get Salary Estimate", type="primary"):
    payload = {
        "work_year": 2022,
        "experience_level": EXPERIENCE_MAP[experience],
        "employment_type": EMPLOYMENT_MAP[employment],
        "job_title": job_title,
        "employee_residence": LOCATIONS[residence],
        "remote_ratio": REMOTE_MAP[remote],
        "company_location": LOCATIONS[company_location],
        "company_size": COMPANY_SIZE_MAP[company_size],
    }

    response = requests.post(f"{API_URL}/predict", json=payload)

    if response.status_code == 200:
        salary = response.json()["predicted_salary_usd"]

        # Salary result card
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(0,212,170,0.10) 0%, rgba(0,212,170,0.04) 100%);
            border: 1px solid rgba(0,212,170,0.28); border-radius: 14px;
            padding: 40px 36px; margin: 28px 0; text-align: center;
        ">
            <div style="
                font-size: 11px; font-weight: 700; color: #00D4AA;
                text-transform: uppercase; letter-spacing: 1.3px; margin-bottom: 12px;
            ">Estimated Market Salary</div>
            <div style="
                font-size: 62px; font-weight: 800; color: #E8F0FE;
                letter-spacing: -2px; line-height: 1; margin-bottom: 8px;
            ">${salary:,.0f}</div>
            <div style="font-size: 16px; color: #8892A4; margin-bottom: 24px;">USD per year</div>
            <div style="
                padding-top: 18px; border-top: 1px solid rgba(0,212,170,0.15);
                font-size: 13px; color: #8892A4; line-height: 1.7;
            ">
                <strong style="color:#E8F0FE;">{experience}</strong> {job_title}
                &nbsp;&middot;&nbsp; {residence}
                &nbsp;&middot;&nbsp; {remote}
                &nbsp;&middot;&nbsp; {company_size.split("(")[0].strip()} company
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI explanation
        with st.spinner("Generating AI explanation…"):
            prompt = f"""
You are a salary analyst. Explain in 2-3 short paragraphs why a {experience} {job_title}
based in {residence}, working {remote.lower()} at a {company_size.split("(")[0].strip().lower()} company
would earn ${salary:,.2f} USD per year.

Be specific about how location, experience, and role affect the salary.
Keep it friendly and easy to understand for an HR manager.
"""
            st.markdown("""
            <div style="
                background: #112240; border: 1px solid #1E3A5F;
                border-radius: 12px; padding: 28px 32px; margin-top: 4px;
            ">
                <div style="
                    font-size: 11px; font-weight: 700; color: #4A9EFF;
                    text-transform: uppercase; letter-spacing: 1.3px; margin-bottom: 18px;
                ">🤖 AI Analysis</div>
            """, unsafe_allow_html=True)

            placeholder = st.empty()
            full_text = ""

            stream = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    placeholder.markdown(
                        f"<p style='color:#B0BAC8; line-height:1.75; margin:0; font-size:15px;'>{full_text}</p>",
                        unsafe_allow_html=True,
                    )

            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error(f"Could not get prediction. API returned: {response.text}")
