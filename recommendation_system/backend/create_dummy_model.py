
import pickle
import numpy as np
# simple user-item matrix small example
user_item = {
    "u1": {"i1":5, "i2":3},
    "u2": {"i1":4, "i3":2},
    "u3": {"i2":4, "i3":5}
}
with open("model.pkl", "wb") as f:
    pickle.dump(user_item, f)
print("Saved dummy recommendation data to model.pkl")
