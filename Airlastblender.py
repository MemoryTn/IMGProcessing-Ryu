import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Blending ภาพจาก URL")

# --- URL ภาพ 2 รูป (กำหนดไว้ล่วงหน้า) ---
URL_IMAGE_1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Fronalpstock_big.jpg/320px-Fronalpstock_big.jpg"
URL_IMAGE_2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/June_odd-eyed-cat_cropped.jpg/320px-June_odd-eyed-cat_cropped.jpg"

# --- ฟังก์ชันโหลดภาพ ---
def load_image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert("RGBA")
    return np.array(image) / 255.0

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

# --- ปรับขนาดให้ตรงกัน ---
h, w = min(img1.shape[0], img2.shape[0]), min(img1.shape[1], img2.shape[1])
img1 = img1[:h, :w]
img2 = img2[:h, :w]

# --- UI: เลือก blending mode และ alpha ---
col1, col2 = st.columns([1, 2])
with col1:
    alpha = st.slider("Blending Ratio (alpha)", 0.0, 1.0, 0.5, 0.01)
    mode = st.selectbox("Blending Mode", ['normal', 'multiply', 'screen', 'overlay'])

# --- ประมวลผล blended image ---
blended = blend_images(img1, img2, alpha, mode)

# --- แสดงผลด้วย Matplotlib ---
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
