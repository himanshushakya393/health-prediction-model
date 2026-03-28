import pickle
import numpy as np
import os

# 🔹 Base directory (where predict.py is located)
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
LE_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "model", "columns.pkl")

# 🔹 Load model files
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LE_PATH, "rb") as f:
    le = pickle.load(f)

with open(COLUMNS_PATH, "rb") as f:
    columns = pickle.load(f)


# 🔹 Create input vector
def create_input(symptom_list):
    input_data = [0] * len(columns)

    for symptom in symptom_list:
        if symptom in columns:
            index = columns.index(symptom)
            input_data[index] = 1

    return input_data


# 🔹 Basic prediction
def predict_disease(symptom_list):
    try:
        input_data = create_input(symptom_list)
        prediction = model.predict([input_data])
        disease = le.inverse_transform(prediction)[0]
        return disease
    except Exception as e:
        return f"Error: {str(e)}"


# 🔥 ADVANCED: Prediction with confidence + TOP 3 diseases
def predict_with_confidence(symptom_list):
    input_data = create_input(symptom_list)

    # Predict probabilities
    probabilities = model.predict_proba([input_data])[0]

    # Get top 3 indices
    top_indices = np.argsort(probabilities)[-3:][::-1]

    # Convert to disease names
    top_diseases = [
        (le.inverse_transform([i])[0], round(probabilities[i] * 100, 2))
        for i in top_indices
    ]

    # Best prediction
    best_disease = top_diseases[0][0]
    confidence = top_diseases[0][1]

    return best_disease, confidence, top_diseases
