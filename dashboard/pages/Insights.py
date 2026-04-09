import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

load_dotenv()

st.set_page_config(
    page_title="Market Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* BASE — matches config.toml so there is no flash */
  .stApp { background-color: #0A1628 !important; color: #E8F0FE; }
  .main .block-container { padding: 2.5rem 3rem 4rem; max-width: 1200px; }

  /* SIDEBAR */
  [data-testid="stSidebar"] { background-color: #0D1F35 !important; border-right: 1px solid #1E3A5F; }
  section[data-testid="stSidebar"] > div:first-child { padding-top: 28px; }
  [data-testid="stSidebarNavLink"] {
      color: #8892A4 !important; border-radius: 8px !important;
      padding: 10px 16px !important; font-size: 15px !important;
      font-weight: 500 !important; transition: all 0.15s !important; margin-bottom: 2px !important;
  }
  [data-testid="stSidebarNavLink"]:hover { background: rgba(0,212,170,0.08) !important; color: #00D4AA !important; }
  [data-testid="stSidebarNavLink"][aria-selected="true"] { background: rgba(0,212,170,0.13) !important; color: #00D4AA !important; font-weight: 700 !important; }
  [data-testid="collapsedControl"] { color: #00D4AA !important; }

  /* HEADINGS */
  h1, h2, h3, h4 { color: #E8F0FE !important; }
  p { color: #B0BAC8; }
  hr { border-color: #1A2B3C !important; margin: 20px 0 !important; }

  /* DATAFRAME */
  [data-testid="stDataFrame"] {
      background: #112240 !important;
      border: 1px solid #1E3A5F !important;
      border-radius: 10px !important;
  }

  /* ALERT */
  .stAlert { border-radius: 10px !important; }

  /* HIDE BRANDING */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme helpers ─────────────────────────────────────────────
CHART_BG   = "#112240"
CHART_GRID = "#1A2B3C"
CHART_TEXT = "#8892A4"
PALETTE    = ["#00D4AA", "#4A9EFF", "#FF6B6B", "#FFB347", "#A78BFA"]


def style_ax(ax):
    """Vertical bar / line charts."""
    ax.set_facecolor(CHART_BG)
    ax.figure.set_facecolor(CHART_BG)
    ax.tick_params(colors=CHART_TEXT, labelsize=9)
    ax.xaxis.label.set_color(CHART_TEXT)
    ax.yaxis.label.set_color(CHART_TEXT)
    ax.xaxis.label.set_fontsize(10)
    ax.yaxis.label.set_fontsize(10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color=CHART_GRID, linewidth=0.7, linestyle="--", alpha=0.8)
    ax.set_axisbelow(True)


def style_ax_h(ax):
    """Horizontal bar charts."""
    ax.set_facecolor(CHART_BG)
    ax.figure.set_facecolor(CHART_BG)
    ax.tick_params(colors=CHART_TEXT, labelsize=9)
    ax.xaxis.label.set_color(CHART_TEXT)
    ax.yaxis.label.set_color(CHART_TEXT)
    ax.xaxis.label.set_fontsize(10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color=CHART_GRID, linewidth=0.7, linestyle="--", alpha=0.8)
    ax.set_axisbelow(True)


# ── Supabase ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

supabase = get_supabase()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 32px;">
    <div style="
        display: inline-flex; align-items: center; gap: 7px;
        background: rgba(74,158,255,0.09); border: 1px solid rgba(74,158,255,0.22);
        color: #4A9EFF; font-size: 11px; font-weight: 700; letter-spacing: 1.2px;
        text-transform: uppercase; padding: 5px 14px; border-radius: 20px; margin-bottom: 18px;
    ">📊 Market Insights</div>
    <h1 style="font-size: 38px; font-weight: 800; margin: 0 0 10px 0; color: #E8F0FE; letter-spacing: -0.4px;">
        Salary Analytics <span style="color:#4A9EFF;">Dashboard</span>
    </h1>
    <p style="font-size: 16px; color: #8892A4; margin: 0; line-height: 1.5;">
        Explore salary trends and AI-generated analysis from all predictions run through this tool.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Data fetch ────────────────────────────────────────────────────────────────
db_response = supabase.table("predictions").select("*").execute()
data = db_response.data

if not data:
    st.warning("No predictions found yet. Use the Salary Predictor to generate some first.")
else:
    df = pd.DataFrame(data)

    # ── KPI cards ─────────────────────────────────────────────────────────────
    avg_sal = df["predicted_salary"].mean()
    max_sal = df["predicted_salary"].max()
    min_sal = df["predicted_salary"].min()

    kpis = [
        ("#00D4AA", "rgba(0,212,170,0.10)",  "rgba(0,212,170,0.22)",  "Average Salary",   f"${avg_sal:,.0f}", "Across all predictions"),
        ("#4A9EFF", "rgba(74,158,255,0.10)", "rgba(74,158,255,0.22)", "Highest Salary",   f"${max_sal:,.0f}", "Peak predicted salary"),
        ("#FFB347", "rgba(255,179,71,0.10)", "rgba(255,179,71,0.22)", "Lowest Salary",    f"${min_sal:,.0f}", "Floor predicted salary"),
        ("#A78BFA", "rgba(167,139,250,0.10)","rgba(167,139,250,0.22)","Model Accuracy",   "90%",              "R² on test set"),
    ]

    k1, k2, k3, k4 = st.columns(4)
    for col, (accent, bg, border, label, value, sub) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(f"""
            <div style="
                background: {bg}; border: 1px solid {border};
                border-radius: 12px; padding: 22px 20px;
            ">
                <div style="font-size: 11px; font-weight: 700; color: {accent};
                            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                    {label}
                </div>
                <div style="font-size: 30px; font-weight: 800; color: #E8F0FE;
                            letter-spacing: -0.5px; line-height: 1; margin-bottom: 6px;">
                    {value}
                </div>
                <div style="font-size: 12px; color: #8892A4;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── Section: Salary drivers ───────────────────────────────────────────────
    st.markdown("""
    <div style="font-size: 11px; font-weight: 700; color: #00D4AA;
                text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Salary Drivers</div>
    <div style="font-size: 19px; font-weight: 700; color: #E8F0FE; margin-bottom: 20px;">
        What drives salary the most?
    </div>
    """, unsafe_allow_html=True)

    ch1, ch2 = st.columns(2, gap="large")

    with ch1:
        exp_order = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}
        exp_df = df.copy()
        exp_df["experience_label"] = exp_df["experience_level"].map(exp_order)
        exp_means = (
            exp_df.groupby("experience_label")["predicted_salary"]
            .mean()
            .reindex(["Entry", "Mid", "Senior", "Executive"])
        )
        fig1, ax1 = plt.subplots(figsize=(5, 3.4))
        bars = ax1.bar(exp_means.index, exp_means.values, color=PALETTE[0], width=0.55, zorder=3)
        ax1.bar_label(bars, fmt="$%.0f", padding=4, color=CHART_TEXT, fontsize=8)
        ax1.set_ylabel("Avg Salary (USD)")
        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
        style_ax(ax1)
        plt.xticks(rotation=0)
        plt.tight_layout(pad=1.2)
        st.markdown("""<div style="font-size:13px; font-weight:600; color:#E8F0FE; margin-bottom:8px;">
            Salary by Experience Level</div>""", unsafe_allow_html=True)
        st.pyplot(fig1)

    with ch2:
        loc_means = (
            df.groupby("employee_residence")["predicted_salary"]
            .mean()
            .sort_values(ascending=True)
        )
        fig2, ax2 = plt.subplots(figsize=(5, 3.4))
        bars2 = ax2.barh(loc_means.index, loc_means.values, color=PALETTE[1], height=0.55, zorder=3)
        ax2.bar_label(bars2, fmt="$%.0f", padding=4, color=CHART_TEXT, fontsize=8)
        ax2.set_xlabel("Avg Salary (USD)")
        ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
        style_ax_h(ax2)
        plt.tight_layout(pad=1.2)
        st.markdown("""<div style="font-size:13px; font-weight:600; color:#E8F0FE; margin-bottom:8px;">
            Salary by Employee Location</div>""", unsafe_allow_html=True)
        st.pyplot(fig2)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Section: Predictions vs real ─────────────────────────────────────────
    st.markdown("""
    <div style="font-size: 11px; font-weight: 700; color: #4A9EFF;
                text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Model Validation</div>
    <div style="font-size: 19px; font-weight: 700; color: #E8F0FE; margin-bottom: 20px;">
        How do predictions compare to real salaries?
    </div>
    """, unsafe_allow_html=True)

    real_data = {
        "Job Title": [
            "Data Scientist", "Data Analyst", "ML Engineer",
            "Data Engineer", "Director of Data Science",
        ],
        "Real Avg Salary (USD)": [137000, 75000, 140000, 120000, 180000],
        "Predicted Salary (USD)": [
            df[df["job_title"] == "Data Scientist"]["predicted_salary"].mean(),
            df[df["job_title"] == "Data Analyst"]["predicted_salary"].mean(),
            df[df["job_title"] == "ML Engineer"]["predicted_salary"].mean(),
            df[df["job_title"] == "Data Engineer"]["predicted_salary"].mean(),
            df[df["job_title"] == "Director of Data Science"]["predicted_salary"].mean(),
        ],
    }
    compare_df = pd.DataFrame(real_data).dropna()

    fig3, ax3 = plt.subplots(figsize=(9, 4))
    x = range(len(compare_df))
    w = 0.38
    b1 = ax3.barh(
        [i - w / 2 for i in x], compare_df["Real Avg Salary (USD)"],
        w, label="Real Market", color=PALETTE[0], zorder=3,
    )
    b2 = ax3.barh(
        [i + w / 2 for i in x], compare_df["Predicted Salary (USD)"],
        w, label="Model Prediction", color=PALETTE[1], zorder=3,
    )
    ax3.bar_label(b1, fmt="$%.0f", padding=4, color=CHART_TEXT, fontsize=8)
    ax3.bar_label(b2, fmt="$%.0f", padding=4, color=CHART_TEXT, fontsize=8)
    ax3.set_yticks(list(x))
    ax3.set_yticklabels(compare_df["Job Title"])
    ax3.set_xlabel("Salary (USD)")
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
    ax3.legend(
        frameon=True, framealpha=0.3, facecolor=CHART_BG,
        edgecolor="#1E3A5F", labelcolor=CHART_TEXT, fontsize=9,
    )
    style_ax_h(ax3)
    plt.tight_layout(pad=1.2)
    st.pyplot(fig3)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Predictions table ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size: 11px; font-weight: 700; color: #A78BFA;
                text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Records</div>
    <div style="font-size: 19px; font-weight: 700; color: #E8F0FE; margin-bottom: 4px;">
        All Saved Predictions
    </div>
    <p style="font-size: 13px; color: #8892A4; margin-bottom: 16px;">
        Click any row to view its AI salary analysis below.
    </p>
    """, unsafe_allow_html=True)

    display_df = df[[
        "job_title", "experience_level", "employee_residence",
        "remote_ratio", "company_size", "predicted_salary",
    ]].copy()
    display_df.columns = [
        "Job Title", "Experience", "Location",
        "Remote %", "Company Size", "Predicted Salary (USD)",
    ]

    selected = st.dataframe(
        display_df,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    if selected and selected["selection"]["rows"]:
        row_index = selected["selection"]["rows"][0]
        selected_row = df.iloc[row_index]
        st.markdown(f"""
        <div style="
            background: rgba(167,139,250,0.07); border: 1px solid rgba(167,139,250,0.20);
            border-radius: 12px; padding: 24px 28px; margin-top: 16px;
        ">
            <div style="font-size: 11px; font-weight: 700; color: #A78BFA;
                        text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px;">
                🤖 AI Analysis
            </div>
            <div style="font-size: 15px; font-weight: 600; color: #E8F0FE; margin-bottom: 14px;">
                {selected_row["job_title"]}
                <span style="color:#8892A4; font-weight:400;">
                    &nbsp;&middot;&nbsp; {selected_row["experience_level"]}
                    &nbsp;&middot;&nbsp; {selected_row["employee_residence"]}
                </span>
            </div>
            <p style="color:#B0BAC8; line-height:1.75; margin:0; font-size:15px;">
                {selected_row["llm_analysis"]}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="font-size: 13px; color: #3D4F62; margin-top: 8px;">
            ↑ Click a row above to see its AI salary analysis.
        </p>
        """, unsafe_allow_html=True)
