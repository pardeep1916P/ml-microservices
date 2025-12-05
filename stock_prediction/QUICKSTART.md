# 🚀 QUICK START - Stock Prediction App

## Option 1: Using yfinance (NO API KEY NEEDED) ✅

### Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

**Done!** Open http://localhost:3000

---

## Option 2: Using Alpha Vantage (Optional)

### 1. Get FREE API Key
Visit: https://www.alphavantage.co/support/#api-key

### 2. Configure Backend
```bash
cd backend
copy .env.example .env
```

Edit `.env`:
```
ALPHA_VANTAGE_API_KEY=YOUR_KEY_HERE
API_MODE=alphavantage
```

### 3. Start (same as above)
```bash
pip install -r requirements.txt
python train_model.py
python app.py
```

---

## 📊 Usage

1. Enter stock symbol (e.g., AAPL, GOOGL, MSFT)
2. Click "Predict"
3. View next day's price prediction + charts

## 🔧 Switching APIs

Edit `backend/.env`:
- `API_MODE=yfinance` (free, no key)
- `API_MODE=alphavantage` (requires key)

---

## ⚠️ Disclaimer
Educational purposes only. Not financial advice.
