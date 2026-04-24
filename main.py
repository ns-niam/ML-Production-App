from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

app = FastAPI(title="ML Model API", version="2.0")

# Load model
try:
    model = joblib.load("model.joblib")
except Exception as e:
    raise RuntimeError(f"Model loading failed: {e}")

# Input schema
class InputData(BaseModel):
    data: list[float] = Field(..., example=[5.1, 3.5, 1.4, 0.2])

# Root endpoint
@app.get("/")
def root():
    return {"message": "ML API is running successfully 🚀"}

# Prediction endpoint
@app.post("/predict")
def predict(input_data: InputData):
    try:
        features = np.array(input_data.data).reshape(1, -1)

        prediction = model.predict(features).tolist()
        confidence = model.predict_proba(features).tolist()

        return {
            "input": input_data.data,
            "prediction": prediction,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))