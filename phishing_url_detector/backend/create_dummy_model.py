
import pickle
import logging
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_model():
    """Create and save a dummy classification model"""
    try:
        logger.info("Creating dummy classification model...")
        
        # Generate synthetic dataset
        X, y = make_classification(
            n_samples=500,
            n_features=10,
            n_informative=8,
            n_redundant=2,
            random_state=42,
            class_sep=1.0
        )
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        logger.info(f"Model trained - Accuracy: {accuracy:.3f}, Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")
        
        # Save model
        model_data = {
            "model": model,
            "feature_count": X.shape[1],
            "metrics": {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(f1)
            }
        }
        
        with open("model.pkl", "wb") as f:
            pickle.dump(model_data, f)
        
        logger.info("Model saved to model.pkl")
        return model_data
        
    except Exception as e:
        logger.error(f"Failed to create model: {str(e)}")
        raise

if __name__ == "__main__":
    create_model()
