import streamlit as st
from PIL import Image
import numpy as np
import requests
from io import BytesIO

# URL ของภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Iris_sanguinea.JPG/800px-Iris_sanguinea.JPG"

# โหลดภาพจาก URL
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# แสดงภาพ
st.title("แสดงภาพจาก URL และดูค่า Pixel")
st.image(img, caption="Iris Flower", use_column_width=True)

# แปลงภาพเป็นอาร์เรย์ numpy
img_array = np.array(img)

st.subheader("ขนาดของภาพ:")
st.write(f"{img_array.shape[0]} x {img_array.shape[1]} pixels")

# เลือกตำแหน่ง pixel ที่ต้องการดู
x = st.slider("เลือกค่า X (แนวนอน)", 0, img_array.shape[1] - 1, 0)
y = st.slider("เลือกค่า Y (แนวตั้ง)", 0, img_array.shape[0] - 1, 0)

# แสดงค่า pixel ที่เลือก
pixel_value = img_array[y, x]  # แถวก่อนคอลัมน์ (y, x)
st.write(f"ค่าสีของ Pixel ที่ตำแหน่ง (X={x}, Y={y}): {pixel_value}")
