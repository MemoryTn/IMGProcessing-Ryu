import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🖼️ แสดงภาพจาก URL และดูภาพเต็ม")

# URLs ของภาพที่ใช้ได้แน่นอน
image_urls = [
    "https://blog.wu.ac.th/wp-content/uploads/2023/01/2-768x578.jpg",
    "https://blog.wu.ac.th/wp-content/uploads/2023/01/3-1-768x576.jpg",
    "https://blog.wu.ac.th/wp-content/uploads/2023/01/5-1024x769.jpg"
]

# สร้างคอลัมน์ 3 รูป
cols = st.columns(3)
selected_index = None

for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=f"ภาพที่ {i+1}", use_column_width=True)
            if st.button(f"🔍 ดูภาพที่ {i+1}", key=f"btn_{i}"):
                selected_index = i
        except UnidentifiedImageError:
            st.error(f"❌ ไม่สามารถเปิดภาพที่ {i+1} ได้ (Image error)")
        except Exception as e:
            st.error(f"⚠️ เกิดข้อผิดพลาดในภาพที่ {i+1}: {e}")

# แสดงภาพแบบเต็ม
if selected_index is not None:
    st.markdown("---")
    st.subheader(f"🔎 ภาพที่ {selected_index + 1} แบบเต็ม")
    try:
        full_image = Image.open(BytesIO(requests.get(image_urls[selected_index]).content))
        st.image(full_image, use_column_width=True)
    except:
        st.error("❌ โหลดภาพแบบเต็มไม่สำเร็จ")
