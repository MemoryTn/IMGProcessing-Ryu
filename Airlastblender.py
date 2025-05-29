import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Blending ภาพจาก URL")

# --- URL ภาพ 2 รูป (จาก Imgur ที่รองรับ bot และเปิดได้แน่นอน) ---
URL_IMAGE_1 = "https://i.imgur.com/8vuLtqi.png"
URL_IMAGE_2 = "https://i.imgur.com/ExdKOOz.png"

# --- ฟังก์ชันโหลดภาพ พร้อมจัดการ error ---
def load_image_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGBA")
        return np.array(image) / 255.0
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดรูปภาพจาก URL ได้:\n{url}\n\n📌 Error: {e}")
        st.stop()

# --- ฟังก์ชัน blend ---
def blend_images(img1, img2, alpha, mode):
    if mode == 'normal':
        return img1 * (1 - alpha) + img2 * alpha
    elif mode == 'multiply':
        return img1 * (1 - alpha) + (img1 * img2) * alpha
    elif mode == 'screen':
        return img1 * (1 - alpha) + (1 - (1 - img1) * (1 - img2)) * alpha
    elif mode == 'overlay':
        return img1 * (1 - alpha) + np.where(img1 < 0.5,
                                             2 * img1 * img2,
                                             1 - 2 * (1 - img1) * (1 - img2)) * alpha
    return img1 * (1 - alpha) + img2 * alpha

# --- โหลดภาพ ---
img1 = load_image_from_url(URL_IMAGE_1)
img2 = load_image_from_url(URL_IMAGE_2)

# --- ปรับขนาดให้เท่ากัน ---
h, w = min(img1.shape[0], img2.shape[0]), min(img1.shape[1], img2.shape[1])
img1 = img1[:h, :w]
img2 = img2[:h, :w]

# --- UI ด้านซ้าย: เลือก blending ---
col1, col2 = st.columns([1, 2])
with col1:
    alpha = st.slider("Blending Ratio (alpha)", 0.0, 1.0, 0.5, 0.01)
    mode = st.selectbox("Blending Mode", ['normal', 'multiply', 'screen', 'overlay'])

# --- ประมวลผลภาพ blend ---
blended = blend_images(img1, img2, alpha, mode)

# --- แสดงผลภาพทั้ง 3 ด้วย matplotlib ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img1)
axes[0].set_title("Image 1")
axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")

axes[1].imshow(img2)
axes[1].set_title("Image 2")
axes[1].set_xlabel("X")
axes[1].set_ylabel("Y")

axes[2].imshow(blended)
axes[2].set_title(f"Blended ({mode}, α={alpha:.2f})")
axes[2].set_xlabel("X")
axes[2].set_ylabel("Y")

st.pyplot(fig)
