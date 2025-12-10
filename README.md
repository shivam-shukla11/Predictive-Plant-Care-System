# 🌱 Predictive Plant Care System (IoT + AI)

An intelligent IoT and AI-powered system that monitors plant health in real time and predicts optimal watering needs while detecting plant diseases using computer vision. Designed for smart homes, gardens, farmers, and SMEs.

---

## 🚀 Key Features

- Real-time monitoring of:
  - Soil moisture
  - Temperature
  - Humidity
  - Light intensity
- AI-based water requirement prediction
- Image-based plant disease detection
- Cloud-based data storage & analytics
- Live web dashboard for visualization
- Scalable architecture for future automation
- Phase-2 ready for smart irrigation automation

---

## 🧠 How It Works

1. Sensors collect real-time environmental data.
2. ESP32 sends data to the FastAPI backend via WiFi.
3. Data is stored securely in MongoDB Atlas.
4. AI models analyze the data to:
   - Predict watering needs  
   - Detect plant diseases from images  
5. Results are displayed on a live dashboard.
6. (Phase 2) Smart automation using pump & relay.

---

## 🧰 Tech Stack

### 🔧 Hardware & IoT
- ESP32 / ESP8266 – WiFi-enabled microcontroller  
- Capacitive Soil Moisture Sensor  
- DHT11 / DHT22 – Temperature & Humidity  
- LDR – Light sensor  
- OLED Display (Optional – Prototype only)  
- Power supply / Battery module  

---

### 🧠 Artificial Intelligence & Machine Learning
- **Scikit-learn** – Water prediction  
  - Model: `RandomForestRegressor`
- **TensorFlow / Keras** – Disease detection  
  - Model: `MobileNetV2` / `EfficientNet` (Pretrained)
- **OpenCV** – Image processing  
- **Pillow (PIL)** – Image handling  

---

### ⚙️ Backend
- **Python**
- **FastAPI**
- **Uvicorn**

---

### 🗄️ Database
- **MongoDB Atlas (Cloud Database)**

---

### ☁️ Cloud & Deployment
- **Render** – Backend hosting  
- **MongoDB Atlas** – Database hosting  
- **GitHub** – Version control  

---

### 📊 Frontend / Dashboard
- HTML, CSS, JavaScript  
- Chart.js / Recharts for graphs  
- REST API-based data flow  

---

### 📡 Communication
- REST API  
- JSON format  
- WiFi-based communication from ESP32  

---

## 🔍 Phase-Wise Development

### ✅ Phase 1 – Prototype
- Sensor monitoring
- Cloud database
- Water prediction
- Disease detection
- Web dashboard

### 🔮 Phase 2 – Smart Automation
- Mobile app
- Multi-user login
- Alerts & notifications
- Automated irrigation
- Farmer & SME analytics

---

## ⚙️ Installation & Setup

1. Clone the repo:
```bash
git clone https://github.com/<shivam-shukla11>/Predictive-Plant-Care.git
```
2. Navigate to the project folder:<br>
 ```bash
cd Predictive-Plant-Care
```
3. Create a virtual environment:
```bash 
python -m venv venv
```
4. Activate the virtual environment:
```bash
   # Windows
    venv\Scripts\activate
   # Linux/Mac 
    source venv/bin/activate
```
5. Install dependencies:
```bash
pip install -r requirements.txt
```
6. Run Backend:
```bash
uvicorn main:app --reload
```
Backend will run on:
```bash
http://127.0.0.1:8000
```
## 📌 Use Cases

- Smart home plant care
- Nursery & gardening automation
- Farmers & agri-SMEs
- Greenhouse monitoring
- Educational IoT + AI demos


# 👥Team
  Built By:

- [Shivam Shukla](https://github.com/shivam-shukla11) - Backend & AI   
- [Mihir Parmar](https://github.com/mihirparmar31) - Hardware & IoT  
- [Dhruv Joshi](https://github.com/burfi-jalabi) - Frontend & Dashboard

## Contribution
- Contributions are welcome! Please fork the repo, make changes, and submit a pull request.

## 📜 License
- This project is for educational, research, and prototyping purposes.
