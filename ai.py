# ai.py
import json
import os
import numpy as np
from threading import Lock
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array

# ----------------------
# Paths
# ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "plant_disease_detection.h5")
CATEGORIES_PATH = os.path.join(BASE_DIR, "models", "categories.json")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Disease model file not found")

if not os.path.exists(CATEGORIES_PATH):
    raise FileNotFoundError("Categories file not found")

# ----------------------
# Global objects (lazy-loaded)
# ----------------------
_model = None
_class_names = None
_load_lock = Lock()

# ----------------------
# Load AI model safely
# ----------------------
def load_ai():
    global _model, _class_names

    if _model is not None and _class_names is not None:
        return

    with _load_lock:
        if _model is None:
            _model = load_model(MODEL_PATH)
            print("✅ Disease model loaded")

        if _class_names is None:
            with open(CATEGORIES_PATH, "r") as f:
                _class_names = json.load(f)
            print("✅ Disease categories loaded")

# ----------------------
# Predict disease from image
# ----------------------
def predict_disease(image_path: str) -> dict:
    if _model is None or _class_names is None:
        load_ai()

    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = _model.predict(img, verbose=0)
    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions))

    return {
        "disease": _class_names.get(str(class_index), "Unknown"),
        "confidence": round(confidence, 4)
    }
