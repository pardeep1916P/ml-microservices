
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
    return jsonify({"status":"ok", "project":"blockchain_microservice"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}

m = load_model()
rid = data.get("record_id")
if not rid:
    return jsonify({"error":"send 'record_id' field"}), 400
ok = rid in m.get("verified_ids", [])
return jsonify({"record_id": rid, "verified": bool(ok)})

if __name__ == "__main__":
    # ensure model exists
    if not os.path.exists(MODEL_PATH):
        try:
            from create_dummy_model import *
        except Exception as e:
            print("Could not create model:", e)
    app.run(host="0.0.0.0", port=5000)
