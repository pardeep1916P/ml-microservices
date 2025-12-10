# Fraud & Intrusion Detection System

ML-powered fraud detection with React frontend and Flask backend.

## 🚀 Quick Start

**Backend:**
```bash
cd backend
./setup.sh        # First time only
./start_backend.sh
```
Runs on http://localhost:5000

**Frontend:**
```bash
cd frontend
npm install       # First time only
npm start
```
Runs on http://localhost:3000

## 📋 Features

- React 18 UI with real-time predictions
- Random Forest ML model (lightweight, <10ms inference)
- 10-feature fraud detection
- Confidence and risk scoring
- Auto backend status detection

## 🛠️ Tech Stack

**Backend:** Flask, Scikit-learn, NumPy  
**Frontend:** React 18, Create React App  
**Model:** Random Forest (10 estimators, 500 training samples)

## 📊 API

**GET /** - Health check  
**POST /predict** - Fraud detection
```json
{
  "features": [0.5, -1.2, 0.8, -0.3, 1.5, 0.2, -0.9, 1.1, -0.4, 0.7]
}
```

## 📦 Structure

```
backend/
  ├── app.py                  # Flask API
  ├── create_dummy_model.py   # ML model generator
  └── requirements.txt        # Python deps

frontend/
  ├── src/
  │   ├── App.js             # Main React component
  │   └── App.css            # Styles
  └── package.json           # npm deps
```

## 📝 Requirements

- Python 3.7+
- Node.js 14+
- npm
