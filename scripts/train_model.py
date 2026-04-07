import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle

# Load cleaned data
df = pd.read_csv("data/cleaned_salaries.csv")

# Split into X and y
X = df.drop(columns=["salary_in_usd"])
y = df["salary_in_usd"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae}")

# Save the model
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved.")