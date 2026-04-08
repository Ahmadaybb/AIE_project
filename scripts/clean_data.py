import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load raw data
df = pd.read_csv("data/ds_salaries.csv")

# Drop useless columns
df = df.drop(columns=["Unnamed: 0", "salary", "salary_currency"])

# Drop duplicates and missing values
df = df.drop_duplicates()
df = df.dropna()

# Columns to encode
text_columns = ["experience_level", "employment_type", "company_location",
                "employee_residence", "company_size", "job_title"]

# Save encoders so we use the same mapping every time
encoders = {}

for col in text_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Save all encoders to one file
os.makedirs("models", exist_ok=True)
joblib.dump(encoders, "models/encoders.joblib")

# Save cleaned data
df.to_csv("data/cleaned_salaries.csv", index=False)

print("Data cleaned and saved.")
print("Encoders saved.")