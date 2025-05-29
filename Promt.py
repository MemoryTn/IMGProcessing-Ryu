import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🖼️ คลิกเพื่อดูภาพแบบเต็ม")

# 3 URLs ของภาพ
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Iris_sanguinea.JPG/800px-Iris_sanguinea.JPG",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_and_Times_Square_by_night.jpg/800px-Broadway_and_Times_Square_by_night.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Nature_landscape.jpg/800px-Nature_landscape.jpg"
]

# ใช้ columns แสดงภาพแบบ responsive
cols = st.columns(3)

# ตัวแปรเลือกภาพ
selected_index = None

for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=f"ภาพที่ {i+1}", use_column_width=True)

            if st.button(f"🔍 ดูภาพที่ {i+1}", key=f"btn_{i}"):
                selected_index = i
        except:
            st.error(f"❌ โหลดภาพที่ {i+1} ไม่สำเร็จ")

# ถ้ามีการกดปุ่มดูภาพ
if selected_index is not None:
    st.markdown("---")
    st.subheader(f"🔎 ภาพที่ {selected_index + 1} แบบเต็ม")
    full_img = Image.open(BytesIO(requests.get(image_urls[selected_index]).content))
    st.image(full_img, use_column_width=True)
