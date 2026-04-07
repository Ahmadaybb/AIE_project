import pandas as pd

# Load the dataset
df = pd.read_csv("data/ds_salaries.csv")

# Drop columns we don't need
df = df.drop(columns=["salary", "salary_currency", "Unnamed: 0"])

# Drop duplicates
df = df.drop_duplicates()

# Drop missing values
df = df.dropna()

# Convert text columns to numbers using Label Encoding
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

text_columns = ["experience_level", "employment_type", "company_location",
                "employee_residence", "company_size", "job_title"]

for col in text_columns:
    df[col] = le.fit_transform(df[col])

# Save the cleaned data
df.to_csv("data/cleaned_salaries.csv", index=False)

print("Data cleaned and saved.")