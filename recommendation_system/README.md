# Recommendation System

AI-powered personalized recommendations with React frontend and Flask backend.

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

- React 18 UI with visual product cards
- User-based collaborative filtering
- Rating-based sorting
- Star rating visualization
- Sample user presets
- Auto backend status detection

## 🛠️ Tech Stack

**Backend:** Flask, Python dictionaries (user-item matrix)  
**Frontend:** React 18, Create React App  
**Model:** Collaborative filtering (user-based)

## 📊 API

**GET /** - Health check  
**POST /predict** - Get recommendations
```json
{
  "user": "alice"
}
```

Response:
```json
{
  "user": "alice",
  "recommendations": [
    {"item": "Product A", "rating": 5},
    {"item": "Product F", "rating": 5}
  ],
  "total_items": 2
}
```

## 📦 Structure

```
backend/
  ├── app.py                  # Flask API
  ├── create_dummy_model.py   # Recommendation data
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
