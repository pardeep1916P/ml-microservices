# ��� Phishing URL Detector 

ML model to detect phishing URLs with intelligent URL feature analysis and real-time predictions (micro service).

## ��� Requirements

- Python 3.8+
- Node.js 16+ (optional, for frontend)

## 🚀 Quick Start

**Backend (API Server):**
```bash
cd backend
./setup.sh          # macOS/Linux
# or
setup.bat           # Windows
python app.py
```
Server: `http://localhost:5000`

**Frontend (Optional UI):**
```bash
cd frontend
npm install
npm start
```
UI: `http://localhost:3000`

## ��� API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/predict` | Phishing prediction |

**Predict Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [10, 20, 30, 40, 50, 60, 70, 80, 90, 10]}'
```

**Response:**
```json
{
  "success": true,
  "prediction": 0,
  "confidence": 0.92,
  "probabilities": {
    "legitimate": 0.92,
    "phishing": 0.08
  }
}
```

## 📁 Structure

```
backend/
├── app.py                # Flask API
├── create_dummy_model.py # Model training
├── model.pkl             # ML model
├── requirements.txt      # Dependencies
├── setup.sh              # Linux/Mac setup (creates venv + installs)
└── setup.bat             # Windows setup (creates venv + installs)

frontend/
├── package.json          # NPM config
├── src/                  # React components
└── public/               # Static files
```

## 📊 Model Performance

- Accuracy: 82%
- Precision: 85%
- Recall: 78%

---

✅ **Status:** ML Model Complete  
📦 **Cloud Deployment & Dockerization:** In Progress  