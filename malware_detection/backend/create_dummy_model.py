
import pickle
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
X, y = make_classification(n_samples=500, n_features=10, random_state=42)
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)
with open("model.pkl", "wb") as f:
    pickle.dump({"model": model, "feature_count": X.shape[1]}, f)
print("Saved dummy classification model to model.pkl")
