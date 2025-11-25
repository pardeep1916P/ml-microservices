
import os
import pickle
import logging
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "*"}})  # Allow all origins for all routes

# Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model_obj = None
EXPECTED_FEATURES = 10

class PredictionError(Exception):
    """Custom exception for prediction errors"""
    pass

def load_model():
    """Load the ML model from pickle file"""
    global model_obj
    if model_obj is None:
        try:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            with open(MODEL_PATH, "rb") as f:
                model_obj = pickle.load(f)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    return model_obj

def validate_features(features):
    """Validate input features"""
    if not isinstance(features, list):
        raise PredictionError("Features must be a list")
    if len(features) != EXPECTED_FEATURES:
        raise PredictionError(f"Expected {EXPECTED_FEATURES} features, got {len(features)}")
    try:
        features = [float(f) for f in features]
    except (ValueError, TypeError):
        raise PredictionError("All features must be numeric")
    return features

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    try:
        load_model()
        return jsonify({"status": "healthy", "model_loaded": True}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/", methods=["GET"])
def hello():
    """Root endpoint"""
    return jsonify({
        "status": "ok",
        "project": "phishing_url_detector",
        "version": "1.0.0",
        "endpoints": ["/health", "/predict", "/"]
    }), 200

@app.route("/predict", methods=["POST"])
def predict():
    """Make predictions on phishing URLs"""
    try:
        data = request.get_json()
        if not data:
            raise PredictionError("Request body must be JSON")
        
        features = data.get("features")
        if features is None:
            raise PredictionError("Missing 'features' key in request")
        
        # Validate and process features
        features = validate_features(features)
        
        # Load model and make prediction
        model = load_model()
        X = np.array([features])
        prediction = model["model"].predict(X)[0]
        probability = model["model"].predict_proba(X)[0]
        
        return jsonify({
            "success": True,
            "prediction": int(prediction),
            "confidence": float(max(probability)),
            "probabilities": {
                "legitimate": float(probability[0]),
                "phishing": float(probability[1])
            }
        }), 200
        
    except PredictionError as e:
        logger.warning(f"Prediction error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in predict: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == "__main__":
    # Ensure model exists
    if not os.path.exists(MODEL_PATH):
        logger.info("Model not found, creating dummy model...")
        try:
            from create_dummy_model import create_model
            create_model()
        except Exception as e:
            logger.error(f"Could not create model: {e}")
            raise
    
    # Run the app
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
