import streamlit as st
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests
from io import BytesIO
import validators

st.title("🖼️ แสดงภาพจาก URL และดูค่าสีของ Pixel")

# รับ URL จากผู้ใช้
image_url = st.text_input("กรอก URL ของภาพ", 
                          "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Iris_sanguinea.JPG/800px-Iris_sanguinea.JPG")

if image_url:
    # ตรวจสอบว่า URL ถูกต้องหรือไม่
    if not validators.url(image_url):
        st.error("URL ไม่ถูกต้อง กรุณาใส่ URL ที่สมบูรณ์ (เช่น เริ่มด้วย http:// หรือ https://)")
    else:
        try:
            # ตั้งค่า headers เพื่อระบุ user-agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            # ขอข้อมูลจาก URL
            response = requests.get(image_url, headers=headers, timeout=10)

            # ตรวจสอบสถานะการตอบกลับ
            if response.status_code != 200:
                st.error(f"ไม่สามารถโหลดภาพได้: ได้รับสถานะ HTTP {response.status_code}")
            else:
                # ตรวจสอบ Content-Type ว่าเป็นภาพหรือไม่
                content_type = response.headers.get('Content-Type', '').lower()
                if not content_type.startswith('image'):
                    st.error(f"URL นี้ไม่ได้ชี้ไปยังไฟล์ภาพโดยตรง (Content-Type: {content_type})")
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
            st.error("ไม่สามารถระบุรูปแบบภาพจาก URL นี้ได้ กรุณาตรวจสอบว่า URL ชี้ไปยังไฟล์ภาพที่ถูกต้อง (เช่น .jpg, .png)")
        except requests.exceptions.Timeout:
            st.error("การร้องขอ URL หมดเวลา กรุณาลองใหม่หรือตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
        except requests.exceptions.RequestException as e:
            st.error(f"ไม่สามารถโหลดภาพจาก URL ได้: {e}")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
