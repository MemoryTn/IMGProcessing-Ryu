import streamlit as st
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests
from io import BytesIO
import validators
import logging

# ตั้งค่า logging เพื่อบันทึกข้อมูลสำหรับการดีบัก
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.title("🖼️ แสดงภาพจาก URL และดูค่าสีของ Pixel")

# รับ URL จากผู้ใช้
image_url = st.text_input("กรอก URL ของภาพ", 
                          "https://images.unsplash.com/photo-1617957681498-30e3e3d8e8bc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")

if image_url:
    # ตรวจสอบว่า URL ถูกต้อง
    if not validators.url(image_url):
        st.error("URL ไม่ถูกต้อง กรุณาใส่ URL ที่สมบูรณ์ (เช่น เริ่มด้วย http:// หรือ https://)")
    else:
        try:
            # ตั้งค่า headers เพื่อระบุ user-agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            logger.debug(f"กำลังร้องขอ URL: {image_url}")
            # ขอข้อมูลจาก URL
            response = requests.get(image_url, headers=headers, timeout=10)

            # ตรวจสอบสถานะการตอบกลับ
            if response.status_code != 200:
                st.error(f"ไม่สามารถโหลดภาพได้: ได้รับสถานะ HTTP {response.status_code}")
                logger.error(f"HTTP Status Code: {response.status_code}")
            else:
                # ตรวจสอบ Content-Type
                content_type = response.headers.get('Content-Type', '').lower()
                logger.debug(f"Content-Type: {content_type}")
                if not content_type.startswith('image'):
                    st.error(f"URL นี้ไม่ได้ชี้ไปยังไฟล์ภาพโดยตรง (Content-Type: {content_type})")
                    logger.error(f"Content-Type ไม่ใช่ภาพ: {content_type}")
                else:
                    # ตรวจสอบขนาดเนื้อหา
                    content_length = len(response.content)
                    logger.debug(f"ขนาดเนื้อหา: {content_length} bytes")
                    if content_length < 100:  # ขนาดเล็กเกินไปอาจไม่ใช่ภาพ
                        st.error("เนื้อหาที่ดึงมามีขนาดเล็กเกินไป อาจไม่ใช่ไฟล์ภาพที่ถูกต้อง")
                        logger.error("เนื้อหามีขนาดเล็กเกินไป")
                    else:
                        # พยายามเปิดภาพ
                        try:
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

                        except UnidentifiedImageError as e:
                            st.error("ไม่สามารถระบุรูปแบบภาพได้ อาจเป็นไฟล์เสียหายหรือไม่ใช่ภาพที่รองรับ (เช่น .jpg, .png)")
                            logger.error(f"UnidentifiedImageError: {str(e)}")
                            logger.debug(f"เนื้อหาแรก 100 bytes: {response.content[:100]}")
                        except Exception as e:
                            st.error(f"เกิดข้อผิดพลาดในการประมวลผลภาพ: {str(e)}")
                            logger.error(f"ข้อผิดพลาดในการประมวลผลภาพ: {str(e)}")

        except requests.exceptions.Timeout:
            st.error("การร้องขอ URL หมดเวลา กรุณาลองใหม่หรือตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
            logger.error("Timeout error")
        except requests.exceptions.RequestException as e:
            st.error(f"ไม่สามารถโหลดภาพจาก URL ได้: {str(e)}")
            logger.error(f"RequestException: {str(e)}")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {str(e)}")
            logger.error(f"ข้อผิดพลาดทั่วไป: {str(e)}")
