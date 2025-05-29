import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv8
model = YOLO("yolov8n.pt")

st.title("🔍 Object Detection จาก URL ด้วย YOLO (ไม่ใช้ OpenCV)")

url = st.text_input("ใส่ URL ของภาพ:")

if url:
    try:
        # โหลดภาพจาก URL
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        st.image(image, caption="ภาพต้นฉบับ", use_column_width=True)

        # ตรวจจับวัตถุ
        results = model.predict(image)

        # ดึงภาพผลลัพธ์จาก .plot() แล้วแปลงเป็น Image
        result_np = results[0].plot()
        result_img = Image.fromarray(result_np)
        st.image(result_img, caption="ผลลัพธ์ Object Detection", use_column_width=True)

        # แสดงรายการวัตถุที่ตรวจพบ
        st.subheader("🔎 รายการวัตถุที่พบ:")
        labels = results[0].names
        detected = [labels[int(cls)] for cls in results[0].boxes.cls]
        st.write(set(detected))

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
