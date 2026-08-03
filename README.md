# 🖼️ DetectronV8

Python • FastAPI • YOLOv8 • OpenCV • License

---

## 🎯 Goal of the Project

Upload an image, run YOLOv8 object detection, and get:

- 🖼️ The image with bounding boxes and labels  
- 📋 A list of detected objects with confidence scores

---

## 💡 How It Works — Step by Step

1. Open the web page and upload an image.  
2. Click **Detect Objects**.  
3. FastAPI saves the uploaded image.  
4. YOLOv8 runs object detection on the image.  
5. Bounding boxes and labels are drawn on the image.  
6. The results page shows:
   - 🖼️ The processed image  
   - 📋 A list of detected objects with confidence values  

---

## 📂 Project Structure (Key Files)

| File / Folder | Description |
|---|---|
| `main.py` | FastAPI app, routes, template rendering |
| `utils.py` | YOLOv8 detection logic and image processing |
| `templates/` | HTML templates (`base.html`, `home.html`, `about.html`, `detection.html`) |
| `static/` | Static assets (images, etc.) |
| `media/uploads/` | Uploaded input images |
| `media/processed/` | YOLOv8 processed output images |
| `yolov8n.pt` | YOLOv8 model weights (Nano version) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes `venv/`, `__pycache__/`, etc. |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/IqramZargar/DetectronV8.git
cd DetectronV8-FAST
```

> If your repo folder is different, use your actual folder name.

---

### 2️⃣ Create and activate virtual environment

```bash
python3 -m venv venv
```

**Linux/macOS**
```bash
source venv/bin/activate
```

**Windows**
```powershell
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

⚠️ YOLOv8 requires PyTorch. Install PyTorch first (based on your system), then install project requirements.

#### Install PyTorch

**Linux/macOS (CUDA 11.8 example):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Windows (CPU example):**
```bash
pip install torch torchvision torchaudio
```

#### Install other dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Download YOLOv8 weights (if not already present)

**Linux/macOS**
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

**Windows (PowerShell)**
```powershell
Invoke-WebRequest https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -OutFile yolov8n.pt
```

---

### 5️⃣ Run the FastAPI development server

```bash
uvicorn main:app --reload
```

---

## 🖥️ Usage

1. Open: `http://127.0.0.1:8000/`  
2. Go to **Start Detection**  
3. Upload an image  
4. View detection results:
   - 🖼️ Image with bounding boxes  
   - 📋 Detected objects with confidence scores  

---

## 📜 Example Output

**Objects Detected:**
- Person: 89.0%  
- Car: 78.0%  
- Dog: 91.0%  

The processed image displays bounding boxes with class labels.

---

## 🛠 Tech Stack

- **Backend:** FastAPI  
- **ML Model:** YOLOv8 (Ultralytics)  
- **Language:** Python  
- **Frontend:** HTML + Jinja2 Templates  
- **Image Processing:** OpenCV  

---

## 🤝 Contributing

Pull requests are welcome.  
If you find bugs or have suggestions, please open an issue.

---

## 👨‍💻 Contributors

- **Mohamin Mushtaq Mir** — Frontend Developer  
- **Asrar Shah** — Frontend Developer  
- **Iqram Zargar** — Backend Developer  

---

## 📄 License

This project is licensed under the **MIT License**.