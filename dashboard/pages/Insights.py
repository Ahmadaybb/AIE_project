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

    # --- Key metrics ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Salary", f"${df['predicted_salary'].mean():,.0f}")
    with col2:
        st.metric("Highest Salary", f"${df['predicted_salary'].max():,.0f}")
    with col3:
        st.metric("Lowest Salary", f"${df['predicted_salary'].min():,.0f}")
    with col4:
        st.metric("Model Accuracy (R²)", "90%")

    st.divider()

    # --- Charts ---
    st.markdown("**What drives salary the most?**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("*Salary by Experience Level*")
        exp_order = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}
        exp_df = df.copy()
        exp_df["experience_label"] = exp_df["experience_level"].map(exp_order)
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        exp_df.groupby("experience_label")["predicted_salary"].mean().reindex(
            ["Entry", "Mid", "Senior", "Executive"]
        ).plot(kind="bar", ax=ax1, color="#4CAF50")
        ax1.set_xlabel("")
        ax1.set_ylabel("Avg Salary (USD)")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        plt.xticks(rotation=0)
        st.pyplot(fig1)

    with col2:
        st.markdown("*Salary by Employee Location*")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        df.groupby("employee_residence")["predicted_salary"].mean().sort_values().plot(
            kind="barh", ax=ax2, color="#2196F3"
        )
        ax2.set_xlabel("Avg Salary (USD)")
        ax2.set_ylabel("")
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        st.pyplot(fig2)

    st.divider()

    # --- Comparison with real data ---
    st.markdown("**How do predictions compare to real salaries?**")
    real_data = {
        "Job Title": ["Data Scientist", "Data Analyst", "ML Engineer", "Data Engineer", "Director of Data Science"],
        "Real Avg Salary (USD)": [137000, 75000, 140000, 120000, 180000],
        "Predicted Salary (USD)": [
            df[df["job_title"] == "Data Scientist"]["predicted_salary"].mean(),
            df[df["job_title"] == "Data Analyst"]["predicted_salary"].mean(),
            df[df["job_title"] == "ML Engineer"]["predicted_salary"].mean(),
            df[df["job_title"] == "Data Engineer"]["predicted_salary"].mean(),
            df[df["job_title"] == "Director of Data Science"]["predicted_salary"].mean(),
        ]
    }
    compare_df = pd.DataFrame(real_data).dropna()
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    x = range(len(compare_df))
    width = 0.35
    ax3.barh([i - width/2 for i in x], compare_df["Real Avg Salary (USD)"], width, label="Real", color="#4CAF50")
    ax3.barh([i + width/2 for i in x], compare_df["Predicted Salary (USD)"], width, label="Predicted", color="#2196F3")
    ax3.set_yticks(list(x))
    ax3.set_yticklabels(compare_df["Job Title"])
    ax3.set_xlabel("Salary (USD)")
    ax3.legend()
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    st.pyplot(fig3)

    st.divider()

    # --- Table with clickable rows ---
    st.markdown("**All Old Predictions — click a row to see its AI analysis**")
    display_df = df[["job_title", "experience_level", "employee_residence",
                     "remote_ratio", "company_size", "predicted_salary"]].copy()
    display_df.columns = ["Job Title", "Experience", "Location", "Remote %", "Company Size", "Predicted Salary (USD)"]

    selected = st.dataframe(
        display_df,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row"
    )

    if selected and selected["selection"]["rows"]:
        row_index = selected["selection"]["rows"][0]
        selected_row = df.iloc[row_index]
        st.divider()
        st.markdown(f"#### AI Analysis — {selected_row['job_title']} ({selected_row['experience_level']}, {selected_row['employee_residence']})")
        st.info(selected_row["llm_analysis"])
    else:
        st.caption("Click a row above to see its AI salary analysis.")