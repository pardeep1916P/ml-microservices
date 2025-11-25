
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
    return jsonify({"status":"ok", "project":"ai_chatbot_service"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}

m = load_model()
msg = data.get("message", "").lower()
if not msg:
    return jsonify({"error":"send 'message' field"}), 400
for k,v in m.items():
    if k in msg:
        return jsonify({"reply": v})
return jsonify({"reply": m.get("default")})

if __name__ == "__main__":
    # ensure model exists
    if not os.path.exists(MODEL_PATH):
        try:
            from create_dummy_model import *
        except Exception as e:
            print("Could not create model:", e)
    app.run(host="0.0.0.0", port=5000)
