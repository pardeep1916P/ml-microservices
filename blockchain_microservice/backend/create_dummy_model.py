
# placeholder: no ML model, this simulates verifying a record
import pickle
data = {"verified_ids": ["rec1", "rec2", "rec3"]}
with open("model.pkl", "wb") as f:
    pickle.dump(data, f)
print("Saved dummy blockchain state to model.pkl")
