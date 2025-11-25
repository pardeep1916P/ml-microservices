
import pickle
# simple pattern-based replies
replies = {
    "hello": "Hi there!",
    "how are you": "I'm a bot, I'm fine.",
    "default": "Sorry, I don't understand."
}
with open("model.pkl", "wb") as f:
    pickle.dump(replies, f)
print("Saved dummy chatbot data to model.pkl")
