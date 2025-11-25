
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
docs = [
    "this is spam buy now",
    "hello how are you",
    "free money click here",
    "meeting schedule tomorrow",
    "win cash prize",
    "project update report",
    "cheap pills here",
    "family photos"
]
labels = [1,0,1,0,1,0,1,0]
tf = TfidfVectorizer()
X = tf.fit_transform(docs)
clf = MultinomialNB()
clf.fit(X, labels)
with open("model.pkl", "wb") as f:
    pickle.dump({"vectorizer": tf, "model": clf}, f)
print("Saved dummy text classification model to model.pkl")
