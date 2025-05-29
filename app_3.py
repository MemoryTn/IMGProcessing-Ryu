import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO
import cv2
import numpy as np
from collections import Counter

st.title("YOLOv8 Object Detection from Image URL")

# ใส่ URL รูปภาพ
img_url = st.text_input("Enter Image URL")

if img_url:
    try:
        # โหลดรูปจาก URL
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # แปลงเป็น numpy array (BGR) ให้ YOLO ใช้ได้
        img_np = np.array(img)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # โหลดโมเดล YOLOv8 nano
        model = YOLO("yolov8n.pt")  # ต้องมีไฟล์นี้อยู่ใน path หรือดาวน์โหลดเอง

        # ทำ inference
        results = model(img_cv)[0]

        # วาดกรอบกล่องและ label ลงบนภาพ
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]
            cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(img_cv, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0,255,0), 2)

        # แปลง BGR กลับเป็น RGB สำหรับแสดงบน Streamlit
        img_display = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        st.image(img_display, caption="Detected Objects", use_column_width=True)

        # นับจำนวนวัตถุแต่ละประเภท
        classes_detected = [model.names[int(cls)] for cls in results.boxes.cls]
        count = Counter(classes_detected)

        st.markdown("### Objects detected:")
        for obj, qty in count.items():
            st.write(f"- {obj}: {qty}")

    except Exception as e:
        st.error(f"Error: {e}")
