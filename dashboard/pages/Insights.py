import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

st.set_page_config(page_title="Market Insights", page_icon="📊")

@st.cache_resource
def get_supabase():
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

supabase = get_supabase()

st.title("📊 Market Insights")
st.markdown("Explore salary trends and AI-generated analysis.")

db_response = supabase.table("predictions").select("*").execute()
data = db_response.data

if not data:
    st.warning("No predictions found yet. Run the analysis script first.")
else:
    df = pd.DataFrame(data)

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Salary", f"${df['predicted_salary'].mean():,.0f}")
    with col2:
        st.metric("Highest Salary", f"${df['predicted_salary'].max():,.0f}")
    with col3:
        st.metric("Lowest Salary", f"${df['predicted_salary'].min():,.0f}")

    st.divider()

    # Chart
    st.markdown("**Average Salary by Job Title**")
    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby("job_title")["predicted_salary"].mean().sort_values().plot(
        kind="barh", ax=ax, color="#4CAF50"
    )
    ax.set_xlabel("Predicted Salary (USD)")
    ax.set_ylabel("")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)

    st.divider()

    # Table
    st.markdown("**All Predictions**")
    display_df = df[["job_title", "experience_level", "employee_residence",
                     "remote_ratio", "company_size", "predicted_salary"]].copy()
    display_df.columns = ["Job Title", "Experience", "Location", "Remote %", "Company Size", "Predicted Salary (USD)"]
    st.dataframe(display_df, use_container_width=True)

    st.divider()

    # LLM Analysis
    st.markdown("**AI Market Analysis**")
    st.info(df.iloc[-1]["llm_analysis"])