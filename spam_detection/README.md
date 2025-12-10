# Spam Detection System

AI-powered spam filter with React frontend and Flask backend.

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

- React 18 UI with real-time spam detection
- Naive Bayes classifier with TF-IDF vectorization
- Confidence and spam probability scores
- Pre-loaded example messages (spam & ham)
- Auto backend status detection

## 🛠️ Tech Stack

**Backend:** Flask, Scikit-learn, TF-IDF  
**Frontend:** React 18, Create React App  
**Model:** Multinomial Naive Bayes

## 📊 API

**GET /** - Health check  
**POST /predict** - Spam detection
```json
{
  "text": "Your message here"
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
