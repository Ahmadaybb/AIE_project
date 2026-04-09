import streamlit as st

st.set_page_config(
    page_title="Salary Benchmarker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* BASE */
  .stApp { background-color: #0A1628; color: #E8F0FE; }
  .main .block-container { padding: 2.5rem 3rem 4rem; max-width: 1100px; }

  /* SIDEBAR */
  [data-testid="stSidebar"] {
      background-color: #0D1F35 !important;
      border-right: 1px solid #1E3A5F;
  }
  section[data-testid="stSidebar"] > div:first-child { padding-top: 28px; }

  /* SIDEBAR NAV LINKS — larger, bolder */
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
  /* Sidebar toggle arrow */
  [data-testid="collapsedControl"] { color: #00D4AA !important; }

  /* HEADINGS */
  h1, h2, h3, h4, h5, h6 { color: #E8F0FE !important; }
  p { color: #B0BAC8; }
  hr { border-color: #1A2B3C !important; margin: 24px 0 !important; }

  /* PAGE LINK BUTTON */
  [data-testid="stPageLink"] a {
      background: #112240 !important;
      border: 1px solid #1E3A5F !important;
      border-radius: 10px !important;
      color: #E8F0FE !important;
      font-weight: 600 !important;
      font-size: 14px !important;
      padding: 14px 20px !important;
      text-decoration: none !important;
      display: block !important;
      text-align: center !important;
      transition: all 0.2s !important;
  }
  [data-testid="stPageLink"] a:hover {
      border-color: #00D4AA !important;
      color: #00D4AA !important;
      background: rgba(0,212,170,0.06) !important;
      transform: translateY(-1px);
  }

  /* HIDE BRANDING */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0D1F35 0%, #112240 55%, #0D1F35 100%);
    border: 1px solid #1E3A5F;
    border-radius: 16px;
    padding: 56px 52px 48px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
">
  <div style="
      position: absolute; top: -90px; right: -90px;
      width: 340px; height: 340px;
      background: radial-gradient(circle, rgba(0,212,170,0.09) 0%, transparent 68%);
      border-radius: 50%; pointer-events: none;
  "></div>
  <div style="
      position: absolute; bottom: -60px; left: 30%;
      width: 200px; height: 200px;
      background: radial-gradient(circle, rgba(74,158,255,0.06) 0%, transparent 70%);
      border-radius: 50%; pointer-events: none;
  "></div>

  <div style="
      display: inline-flex; align-items: center; gap: 7px;
      background: rgba(0,212,170,0.10); border: 1px solid rgba(0,212,170,0.28);
      color: #00D4AA; font-size: 11px; font-weight: 700; letter-spacing: 1.3px;
      text-transform: uppercase; padding: 5px 14px; border-radius: 20px; margin-bottom: 22px;
  ">✦ AI-POWERED MARKET INTELLIGENCE</div>

  <h1 style="
      font-size: 48px; font-weight: 800; color: #E8F0FE;
      line-height: 1.12; margin: 0 0 18px 0; letter-spacing: -0.8px;
  ">Data Science<br><span style="color:#00D4AA;">Salary Benchmarker</span></h1>

  <p style="
      font-size: 18px; color: #8892A4; max-width: 500px;
      line-height: 1.65; margin: 0 0 40px 0;
  ">Know exactly what the market pays. Make competitive offers backed by real data and AI-powered analysis.</p>

  <div style="display: flex; gap: 48px; padding-top: 28px; border-top: 1px solid #1E3A5F;">
      <div>
          <div style="font-size: 32px; font-weight: 800; color: #00D4AA; line-height: 1;">90%</div>
          <div style="font-size: 12px; color: #8892A4; margin-top: 5px; font-weight: 500;">Model Accuracy R²</div>
      </div>
      <div>
          <div style="font-size: 32px; font-weight: 800; color: #00D4AA; line-height: 1;">13+</div>
          <div style="font-size: 12px; color: #8892A4; margin-top: 5px; font-weight: 500;">Job Titles</div>
      </div>
      <div>
          <div style="font-size: 32px; font-weight: 800; color: #00D4AA; line-height: 1;">8</div>
          <div style="font-size: 12px; color: #8892A4; margin-top: 5px; font-weight: 500;">Countries Covered</div>
      </div>
      <div>
          <div style="font-size: 32px; font-weight: 800; color: #00D4AA; line-height: 1;">3K+</div>
          <div style="font-size: 12px; color: #8892A4; margin-top: 5px; font-weight: 500;">Training Data Points</div>
      </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
cards = [
    ("🎯", "Instant Salary Estimate",
     "Get an ML-powered salary estimate for any data science role in seconds, calibrated on real market data."),
    ("📊", "Market Insights",
     "Explore salary distributions across experience levels, locations, employment types, and company sizes."),
    ("🤖", "AI Explanation",
     "Understand the 'why' behind every estimate with contextual analysis generated by a 70B language model."),
]
c1, c2, c3 = st.columns(3)
for col, (icon, title, desc) in zip([c1, c2, c3], cards):
    with col:
        st.markdown(f"""
        <div style="
            background: #112240; border: 1px solid #1E3A5F; border-radius: 12px;
            padding: 28px 24px; height: 100%;
        ">
            <div style="font-size: 28px; margin-bottom: 14px;">{icon}</div>
            <div style="font-size: 15px; font-weight: 700; color: #E8F0FE; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 13px; color: #8892A4; line-height: 1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ── CTA links ─────────────────────────────────────────────────────────────────
st.markdown("""<div style="font-size: 19px; font-weight: 700; color: #E8F0FE; margin-bottom: 14px;">Get Started</div>""",
            unsafe_allow_html=True)
cl1, cl2, cl3 = st.columns([1, 1, 2])
with cl1:
    st.page_link("pages/try_it.py", label="Try the Salary Predictor", icon="🎯")
with cl2:
    st.page_link("pages/Insights.py", label="View Market Insights", icon="📊")

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""<div style="font-size: 19px; font-weight: 700; color: #E8F0FE; margin-bottom: 4px;">How It Works</div>""",
            unsafe_allow_html=True)

steps = [
    ("01", "Enter Role Details",
     "Select job title, experience level, location, employment type, and company size from the dropdown menus."),
    ("02", "Get an Instant Estimate",
     "Our ML model trained on 3,000+ real salaries returns a calibrated annual figure in USD within milliseconds."),
    ("03", "Read the AI Analysis",
     "A 70B language model explains the key factors — location premium, seniority uplift, remote adjustment — in plain English."),
]
for num, title, desc in steps:
    st.markdown(f"""
    <div style="
        display: flex; align-items: flex-start; gap: 20px;
        padding: 18px 0; border-bottom: 1px solid #1A2B3C;
    ">
        <div style="
            min-width: 38px; height: 38px; width: 38px;
            background: rgba(0,212,170,0.09); border: 1px solid rgba(0,212,170,0.22);
            color: #00D4AA; font-size: 12px; font-weight: 700;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        ">{num}</div>
        <div style="padding-top: 2px;">
            <div style="font-size: 15px; font-weight: 600; color: #E8F0FE; margin-bottom: 4px;">{title}</div>
            <div style="font-size: 13px; color: #8892A4; line-height: 1.5;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ── Tech stack ────────────────────────────────────────────────────────────────
tech = ["FastAPI", "Scikit-learn", "Groq · LLaMA 3.3 70B", "Supabase", "Streamlit"]
badges = "".join([
    f"""<span style="
        background: rgba(74,158,255,0.09); border: 1px solid rgba(74,158,255,0.18);
        color: #4A9EFF; font-size: 11px; font-weight: 600;
        padding: 4px 11px; border-radius: 4px; letter-spacing: 0.4px;
    ">{t}</span>""" for t in tech
])
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
    <span style="font-size: 11px; color: #3D4F62; font-weight: 600; letter-spacing: 0.8px;">BUILT WITH</span>
    {badges}
</div>
""", unsafe_allow_html=True)
