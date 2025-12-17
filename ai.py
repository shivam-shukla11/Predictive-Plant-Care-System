import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array

# Paths
MODEL_PATH = "models/plant_disease_detection.h5"
CATEGORIES_PATH = "models/categories.json"

# Load model ONCE
model = load_model(MODEL_PATH)

# Load categories (keys are strings)
with open(CATEGORIES_PATH, "r") as f:
    class_names = json.load(f)

def predict_disease(image_path: str):
    # Load & preprocess image
    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    predictions = model.predict(img)
    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions))

    # 🔑 FIX: convert index → string for JSON lookup
    disease_name = class_names.get(str(class_index), "Unknown")

    return {
        "disease": disease_name,
        "confidence": round(confidence, 4)
    }
