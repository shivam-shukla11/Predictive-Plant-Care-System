import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import os
from threading import Lock

# ----------------------
# Paths
# ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "plant_disease_detection.h5")
CATEGORIES_PATH = os.path.join(BASE_DIR, "models", "categories.json")

# ----------------------
# Global objects (lazy load)
# ----------------------
model = None
class_names = None
load_lock = Lock()  # prevents double-load in parallel requests

# ----------------------
# Lazy loader (SAFE)
# ----------------------
def load_ai():
    global model, class_names

    # Already loaded → do nothing
    if model is not None and class_names is not None:
        return

    with load_lock:
        # Double-check inside lock
        if model is None:
            model = load_model(MODEL_PATH)
            print("✅ Disease model loaded")

        if class_names is None:
            with open(CATEGORIES_PATH, "r") as f:
                class_names = json.load(f)
            print("✅ Disease categories loaded")

# ----------------------
# Prediction function
# ----------------------
def predict_disease(image_path: str):
    # 🔑 KEY CHANGE: load here if needed
    load_ai()

    # Load & preprocess image
    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    predictions = model.predict(img, verbose=0)
    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions))

    disease_name = class_names.get(str(class_index), "Unknown")

    return {
        "disease": disease_name,
        "confidence": round(confidence, 4)
    }
