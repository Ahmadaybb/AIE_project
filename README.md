# Data Science Salary Benchmarker

An end-to-end AI-powered salary benchmarking tool for data science roles. Enter a job profile and instantly get a market salary estimate backed by a machine learning model, plus an AI-generated explanation of the driving factors.

---

## Overview

HR managers and hiring teams often struggle to know whether a salary offer is competitive. This tool solves that by combining a trained ML model with a large language model to give instant, explainable salary estimates for data science positions across 8 countries.

**What it does:**
- Predicts annual salary (USD) for any data science role based on experience, location, employment type, and company size
- Streams an AI-generated explanation of the salary via a 70B parameter language model
- Displays market insights — KPI cards, salary-by-experience charts, salary-by-location charts, and a real vs. predicted comparison
- Stores all predictions and their AI analyses in a cloud database

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User (Browser)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Streamlit Dashboard  (dashboard/)              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   app.py     │  │  try_it.py   │  │   Insights.py    │  │
│  │ Landing Page │  │  Predictor   │  │  Analytics View  │  │
│  └──────────────┘  └──────┬───────┘  └────────┬─────────┘  │
└─────────────────────────── │ ──────────────────│────────────┘
                             │ HTTP POST         │ SELECT *
                             ▼                   ▼
              ┌──────────────────────┐  ┌───────────────────┐
              │   FastAPI  (api/)    │  │  Supabase (cloud) │
              │   /predict endpoint  │  │  predictions table│
              └──────────┬───────────┘  └───────────────────┘
                         │                        ▲
                         ▼                        │
              ┌──────────────────────┐   ┌────────────────────┐
              │  ML Model            │   │ scripts/analyze.py │
              │  DecisionTree        │   │ Bulk batch runner  │
              │  models/model.joblib │   └────────┬───────────┘
              └──────────────────────┘            │
                                         ┌────────┴────────┐
                                         │    Groq API      │
                                         │  LLaMA 3.3 70B   │
                                         └─────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit 1.56 |
| API | FastAPI + Uvicorn |
| ML Model | Scikit-learn — Decision Tree Regressor |
| AI Explanation | Groq API — LLaMA 3.3 70B Versatile |
| Database | Supabase (PostgreSQL) |
| Data Processing | Pandas, NumPy |
| Visualisation | Matplotlib |
| Model Serialisation | Joblib |
| Containerisation | Docker |
| Environment | Python 3.12, python-dotenv |

---

## Project Structure

```
salary_prediction/
│
├── api/
│   └── main.py               # FastAPI app — /predict endpoint
│
├── dashboard/
│   ├── app.py                # Home / landing page
│   ├── .streamlit/
│   │   └── config.toml       # Dark theme config (prevents flash on page switch)
│   └── pages/
│       ├── try_it.py         # Interactive salary predictor form
│       └── Insights.py       # Charts, KPI cards, predictions table
│
├── models/
│   ├── model.joblib          # Trained Decision Tree model
│   └── encoders.joblib       # Label encoders for categorical features
│
├── scripts/
│   ├── clean_data.py         # Raw CSV → cleaned_salaries.csv
│   ├── train_model.py        # Train + evaluate + save model
│   ├── predict.py            # One-off prediction helper
│   └── analyze.py            # Batch predictions + LLM analysis → Supabase
│
├── data/
│   └── cleaned_salaries.csv  # Processed training data
│
├── ds_salaries.csv           # Raw dataset (2020–2022, ~3,700 rows)
├── Dockerfile                # Containerises the FastAPI service
├── requirements.txt
└── .env                      # Secret keys (not committed)
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- A [Supabase](https://supabase.com) project with a `predictions` table
- A [Groq](https://console.groq.com) API key
- Docker (optional, for running the API in a container)

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd salary_prediction
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
GROQ_API_KEY=your-groq-api-key
API_URL=http://127.0.0.1:8000
```

### 5. Set up the Supabase table

Run this SQL in your Supabase SQL editor:

```sql
create table predictions (
  id                 bigint generated always as identity primary key,
  work_year          int,
  experience_level   text,
  employment_type    text,
  job_title          text,
  employee_residence text,
  remote_ratio       int,
  company_location   text,
  company_size       text,
  predicted_salary   float,
  llm_analysis       text,
  created_at         timestamptz default now()
);
```

---

## Running the Project

### Step 1 — Train the model

```bash
python scripts/clean_data.py
python scripts/train_model.py
```

Saves `models/model.joblib` and `models/encoders.joblib`.

### Step 2 — Start the FastAPI server

```bash
uvicorn api.main:app --reload
```

API available at `http://127.0.0.1:8000`  
Interactive docs at `http://127.0.0.1:8000/docs`

#### Or run with Docker

```bash
docker build -t salary-api .
docker run -p 8000:8000 salary-api
```

### Step 3 — (Optional) Populate the insights database

Runs a batch of job combinations through the API, generates LLM analyses, and saves everything to Supabase:

```bash
python scripts/analyze.py
```

### Step 4 — Launch the dashboard

```bash
cd dashboard
streamlit run app.py
```

---

## API Reference

### `POST /predict`

Returns a predicted annual salary in USD.

**Request body:**

```json
{
  "work_year": 2022,
  "experience_level": "SE",
  "employment_type": "FT",
  "job_title": "Data Scientist",
  "employee_residence": "US",
  "remote_ratio": 100,
  "company_location": "US",
  "company_size": "L"
}
```

**Field values:**

| Field | Options |
|---|---|
| `experience_level` | `EN` (Entry), `MI` (Mid), `SE` (Senior), `EX` (Executive) |
| `employment_type` | `FT` (Full Time), `PT` (Part Time), `CT` (Contract), `FL` (Freelance) |
| `company_size` | `S` (Small), `M` (Medium), `L` (Large) |
| `remote_ratio` | `0` (On-site), `50` (Hybrid), `100` (Fully Remote) |
| `employee_residence` / `company_location` | ISO codes: `US` `GB` `DE` `FR` `IN` `CA` `ES` `AU` |

**Response:**

```json
{
  "predicted_salary_usd": 142500.00
}
```

---

## Model Details

| Property | Value |
|---|---|
| Algorithm | Decision Tree Regressor |
| Max depth | 3 |
| Train / test split | 80 / 20 |
| R² score | ~0.90 |
| Training data | ds_salaries.csv — 2020–2022, ~3,700 rows |
| Features | work_year, experience_level, employment_type, job_title, employee_residence, remote_ratio, company_location, company_size |
| Target | salary_in_usd |

Categorical features are label-encoded. The encoders are saved alongside the model so the API can consistently transform unseen inputs at inference time.

---

## Dashboard Pages

| Page | File | Description |
|---|---|---|
| Home | `app.py` | Landing page — hero section, feature cards, how-it-works steps |
| Salary Predictor | `pages/try_it.py` | Role form → ML prediction → streaming AI explanation |
| Market Insights | `pages/Insights.py` | KPI cards, experience/location charts, real vs. predicted comparison, clickable predictions table with AI analysis |

---

## Environment Variables

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Supabase anon/public key |
| `GROQ_API_KEY` | Groq API key for LLaMA 3.3 70B |
| `API_URL` | Base URL of the FastAPI service (default: `http://127.0.0.1:8000`) |

---

## Limitations

- Training data covers **2020–2022 only** — estimates reflect market conditions from that period, not current rates
- The dataset has ~3,700 rows; predictions for rare job title / country combinations may be less accurate
- The Decision Tree is capped at depth 3 for interpretability — a gradient boosting model would yield higher accuracy

---

## Built With

[FastAPI](https://fastapi.tiangolo.com) · [Scikit-learn](https://scikit-learn.org) · [Groq](https://groq.com) · [Supabase](https://supabase.com) · [Streamlit](https://streamlit.io)
