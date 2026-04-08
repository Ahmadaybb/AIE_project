import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load cleaned data
df = pd.read_csv("data/cleaned_salaries.csv")

# Split into X and y
X = df.drop(columns=["salary_in_usd"])
y = df["salary_in_usd"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeRegressor(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f"MAE: ${mae:,.2f}")
print(f"R2: {r2:.4f}")

# Save the model
joblib.dump(model, "models/model.joblib")
print("Model saved.")