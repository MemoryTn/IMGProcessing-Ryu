import streamlit as st
from ultralytics import YOLO
from PIL import Image
import requests
from io import BytesIO

# โหลดโมเดล
model = YOLO("yolov8n.pt")

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img

st.title("YOLOv8 Object Detection without OpenCV")

url = st.text_input("ใส่ URL ภาพที่นี่")

if url:
    image = load_image_from_url(url)
    st.image(image, caption="Input Image", use_column_width=True)

    # รัน detect
    results = model(image)

    # แสดงผล object detection (bounding boxes) โดยใช้ PIL
    results_plotted = results[0].plot()  # plot() คืนภาพเป็น numpy array

    # แปลง numpy array -> PIL.Image เพื่อแสดงบน Streamlit โดยไม่ต้อง cv2
    result_img = Image.fromarray(results_plotted)
    st.image(result_img, caption="Detected Objects", use_column_width=True)
