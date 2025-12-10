
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle, os
app = Flask(__name__)
CORS(app)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model_obj = None
def load_model():
    global model_obj
    if model_obj is None:
        with open(MODEL_PATH, "rb") as f:
            model_obj = pickle.load(f)
    return model_obj

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"status":"ok", "project":"spam_detection"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    m = load_model()
    vec = m["vectorizer"]
    clf = m["model"]
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "send 'text' in JSON"}), 400
    X = vec.transform([text])
    pred = clf.predict(X)[0]
    prob = clf.predict_proba(X)[0]
    return jsonify({
        "prediction": int(pred),
        "is_spam": bool(pred),
        "confidence": float(max(prob)),
        "spam_probability": float(prob[1]) if len(prob) > 1 else 0.0
    })

if __name__ == "__main__":
    # ensure model exists
    if not os.path.exists(MODEL_PATH):
        try:
            from create_dummy_model import *
        except Exception as e:
            print("Could not create model:", e)
    app.run(host="0.0.0.0", port=5000)
