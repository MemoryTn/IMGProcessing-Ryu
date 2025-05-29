import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🖼️ แสดงภาพจาก URL และดูภาพเต็ม")

# URLs ของภาพที่ใช้ได้แน่นอน
image_urls = [
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1529688530647-93a5c4a3f8b0?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1493244040629-496f6d136cc3?auto=format&fit=crop&w=800&q=80"
]

# สร้างคอลัมน์ 3 รูป
cols = st.columns(3)
selected_index = None

for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            image = Image.open(BytesIO(response.content)).convert("RGB")
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
        response = requests.get(image_urls[selected_index], headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        full_image = Image.open(BytesIO(response.content)).convert("RGB")
        st.image(full_image, use_column_width=True)
    except:
        st.error("❌ โหลดภาพแบบเต็มไม่สำเร็จ")
