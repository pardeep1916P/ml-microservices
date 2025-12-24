
import pickle
import numpy as np

# Enhanced user-item recommendations with realistic items
user_item = {
    "alice": {
        "Product A": 5,
        "Product B": 4,
        "Product C": 3,
        "Product F": 5
    },
    "bob": {
        "Product A": 4,
        "Product D": 5,
        "Product E": 3,
        "Product G": 4
    },
    "charlie": {
        "Product B": 5,
        "Product C": 4,
        "Product D": 3,
        "Product H": 5
    },
    "diana": {
        "Product A": 3,
        "Product E": 5,
        "Product F": 4,
        "Product I": 5
    },
    "eve": {
        "Product B": 4,
        "Product G": 5,
        "Product H": 4,
        "Product J": 5
    }
}

with open("model.pkl", "wb") as f:
    pickle.dump(user_item, f)
    
print("Saved recommendation data to model.pkl")
print(f"Total users: {len(user_item)}")
print(f"Users: {', '.join(user_item.keys())}")
