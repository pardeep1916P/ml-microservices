
import pickle
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
X, y = make_regression(n_samples=500, n_features=10, noise=0.1, random_state=42)
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X, y)
with open("model.pkl", "wb") as f:
    pickle.dump({"model": model, "feature_count": X.shape[1]}, f)
print("Saved dummy regression model to model.pkl")
