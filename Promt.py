import streamlit as st
from PIL import Image
import numpy as np
import requests
from io import BytesIO

st.title("🔍 ดูค่าสีของ Pixel จากภาพออนไลน์")

# ช่องให้กรอก URL ของภาพ
image_url = st.text_input("กรอก URL ของภาพที่ต้องการแสดง", 
                          "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Iris_sanguinea.JPG/800px-Iris_sanguinea.JPG")

if image_url:
    try:
        # โหลดภาพจาก URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # แสดงภาพ
        st.image(img, caption="ภาพจาก URL", use_column_width=True)

        # แปลงภาพเป็นอาร์เรย์ numpy
        img_array = np.array(img)

        # แสดงขนาดภาพ
        height, width = img_array.shape[0], img_array.shape[1]
        st.write(f"ขนาดภาพ: {width} x {height} pixels")

        # ให้ผู้ใช้เลือกตำแหน่งพิกเซล
        x = st.slider("ตำแหน่ง X (แนวนอน)", 0, width - 1, 0)
        y = st.slider("ตำแหน่ง Y (แนวตั้ง)", 0, height - 1, 0)

        # ดึงค่าสีจากตำแหน่งที่เลือก
        pixel_value = img_array[y, x]  # (row, column) = (y, x)
        st.markdown(f"🎯 **ตำแหน่ง (X={x}, Y={y})**: ค่าสี RGB = `{pixel_value}`")

        # แสดงสีแบบตัวอย่าง
        st.markdown("ตัวอย่างสีนี้:")
        st.color_picker("สีของพิกเซลนี้", f'rgb({pixel_value[0]}, {pixel_value[1]}, {pixel_value[2]})', disabled=True)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพจาก URL ได้: {e}")
