import streamlit as st
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests
from io import BytesIO

st.title("🖼️ แสดงภาพจาก URL และดูค่าสีของ Pixel")

# รับ URL จากผู้ใช้
image_url = st.text_input("กรอก URL ของภาพ", 
                          "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Iris_sanguinea.JPG/800px-Iris_sanguinea.JPG")

if image_url:
    try:
        # ขอข้อมูลจาก URL
        response = requests.get(image_url, timeout=10)

        # ตรวจสอบ Content-Type ว่าเป็นภาพหรือไม่
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type:
            st.error("URL นี้ไม่ได้ชี้ไปยังไฟล์ภาพโดยตรง (Content-Type ไม่ใช่ภาพ)")
        else:
            # เปิดภาพ
            img = Image.open(BytesIO(response.content)).convert("RGB")
            st.image(img, caption="ภาพจาก URL", use_column_width=True)

            # แปลงเป็น numpy array
            img_array = np.array(img)
            height, width = img_array.shape[:2]
            st.write(f"ขนาดภาพ: {width} x {height} pixels")

            # เลือกตำแหน่ง pixel
            x = st.slider("ตำแหน่ง X", 0, width - 1, 0)
            y = st.slider("ตำแหน่ง Y", 0, height - 1, 0)

            pixel_value = img_array[y, x]
            st.write(f"🎯 ค่าสีของ Pixel (X={x}, Y={y}): RGB = {pixel_value}")
            st.color_picker("ตัวอย่างสี", f'rgb({pixel_value[0]}, {pixel_value[1]}, {pixel_value[2]})', disabled=True)

    except UnidentifiedImageError:
        st.error("ไม่สามารถระบุรูปแบบภาพจาก URL นี้ได้ (UnidentifiedImageError)")
    except requests.exceptions.RequestException as e:
        st.error(f"ไม่สามารถโหลดภาพจาก URL ได้: {e}")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
