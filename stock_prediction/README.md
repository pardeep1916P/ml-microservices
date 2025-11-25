
stock_prediction
=========

Backend:
- create_dummy_model.py -> generates a small example model and saves model.pkl
- app.py -> Flask app exposing /predict (POST). Run:
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python create_dummy_model.py
    python app.py

Frontend:
- Minimal React-like files included. Your frontend dev can replace with full CRA/Next.js app.
- Files: package.json, src/index.js, src/App.js
