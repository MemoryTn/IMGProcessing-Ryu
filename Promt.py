import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🖼️ แสดงภาพจาก URL และดูภาพเต็ม")

st.markdown("กรอก URL รูปภาพ 3 รูป:")

# ป้อน URL รูปภาพ
url1 = st.text_input("https://shortrecap.co/wp-content/uploads/2020/05/Catcover_web.jpg", "")
url2 = st.text_input("https://shortrecap.co/wp-content/uploads/2020/05/Catcover_web.jpg", "")
url3 = st.text_input("https://shortrecap.co/wp-content/uploads/2020/05/Catcover_web.jpg", "")

image_urls = [url1, url2, url3]
cols = st.columns(3)
selected_index = None

# แสดง preview 3 ภาพ
for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        if url:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                res = requests.get(url, headers=headers, timeout=10)
                image = Image.open(BytesIO(res.content))
                st.image(image, caption=f"ภาพที่ {i+1}", use_column_width=True)
                if st.button(f"🔍 ดูภาพที่ {i+1}", key=f"btn_{i}"):
                    selected_index = i
            except UnidentifiedImageError:
                st.error(f"❌ ไม่สามารถเปิดภาพที่ {i+1} ได้ (Image error)")
            except Exception as e:
                st.error(f"⚠️ เกิดข้อผิดพลาดในภาพที่ {i+1}: {e}")
        else:
            st.info(f"📭 กรุณากรอก URL สำหรับภาพที่ {i+1}")

# แสดงภาพเต็มเมื่อคลิก
if selected_index is not None:
    st.markdown("---")
    st.subheader(f"🔎 ภาพที่ {selected_index + 1} แบบเต็ม")
    try:
        full_image = Image.open(BytesIO(requests.get(image_urls[selected_index]).content))
        st.image(full_image, use_column_width=True)
    except:
        st.error("❌ โหลดภาพแบบเต็มไม่สำเร็จ")
