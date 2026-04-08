import streamlit as st

st.set_page_config(page_title="Salary Benchmarker", page_icon="💼", layout="centered")

st.title("💼 Data Science Salary Benchmarker")
st.markdown("### Know the market. Make the right offer.")

st.markdown("""
Are you an HR manager hiring data science talent?  
Do you know if your salary offer is competitive?

**This tool helps you:**
- Instantly estimate the market salary for any data science role
- Compare salaries across experience levels, locations, and job titles
- Make data-driven hiring decisions backed by real market data
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/try_It.py", label="Try the Salary Predictor", icon="🎯")

with col2:
    st.page_link("pages/Insights.py", label="View Market Insights", icon="📊")

st.divider()

st.markdown("#### How it works")
st.markdown("""
1. **Enter the role details** — job title, experience, location, company size
2. **Get an instant salary estimate** — powered by a machine learning model trained on real data
3. **Explore insights** — see salary trends and AI-generated market analysis
""")

st.caption("Built with FastAPI · Scikit-learn · Ollama · Supabase · Streamlit")