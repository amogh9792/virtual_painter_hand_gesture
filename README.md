# 🖌️ Virtual Painter using Hand Gestures (Whiteboard Mode)

A computer vision-based **Virtual Painter** where you can draw, erase, and change colors using **hand gestures**. The camera captures your hand, and based on the gesture, it triggers painting actions on a **whiteboard background** with your **faint live feed** visible.

---

## 🚀 Features

✅ Draw on a whiteboard using **index finger (right/left hand)**  
✅ Change brush colors with **two-finger gesture**  
✅ Erase with **hand grip**  
✅ Fullscreen Mode (Press `f`)  
✅ Smooth lines instead of dots  
✅ Slight webcam visibility in the background

---

## 🖥️ Project Structure

```
virtual_painter/
│
├── app.py                 # Main application
├── painter.py             # Painter class handling drawing logic
├── hand_tracking.py       # Hand detection using MediaPipe
├── requirements.txt       # Python dependencies
└── README.md              # Project instructions
```

---

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/amogh9792/virtual_painter.git
cd virtual_painter
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv painter_venv
painter_venv\Scripts\activate  # For Windows
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## ✅ Run the Application

```bash
python app.py
```

### 🎯 **Controls / Gestures**

| Gesture               | Action            |
| --------------------- | ----------------- |
| **Index Finger Up**   | Draw (Brush Mode) |
| **Index + Middle Up** | Change Color      |
| **Hand Grip**         | Eraser Mode       |
| **Press 'f' key**     | Fullscreen Toggle |
| **Press 'q' key**     | Quit              |

---

## 📦 `requirements.txt`

```text
opencv-python
mediapipe
numpy
```

Install:

```bash
pip install -r requirements.txt
```

---

## ⚠️ Notes

- Works with both **Right** and **Left** hands.
- Webcam feed is slightly visible in the background.
- Draws smooth lines instead of dots.
- The screen opens as a **whiteboard**, not the raw camera feed.

---

## 💻 Example Output:

_(You'll see yourself faintly and draw on a white canvas using hand gestures)_

---
