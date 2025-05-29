import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGBA')
    return np.array(img) / 255.0

def blend_images(img1, img2, alpha, mode):
    if mode == 'normal':
        return img1 * (1 - alpha) + img2 * alpha
    elif mode == 'multiply':
        return img1 * (1 - alpha) + (img1 * img2) * alpha
    elif mode == 'screen':
        return img1 * (1 - alpha) + (1 - (1 - img1) * (1 - img2)) * alpha
    elif mode == 'overlay':
        overlay = np.where(img1 < 0.5,
                           2 * img1 * img2,
                           1 - 2 * (1 - img1) * (1 - img2))
        return img1 * (1 - alpha) + overlay * alpha
    else:
        return img1 * (1 - alpha) + img2 * alpha

st.title("Image Blending App with Streamlit")

# URL input (ใส่ URL รูปภาพ 2 รูป)
url1 = st.text_input("Image URL 1", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Fronalpstock_big.jpg/320px-Fronalpstock_big.jpg")
url2 = st.text_input("Image URL 2", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/June_odd-eyed-cat_cropped.jpg/320px-June_odd-eyed-cat_cropped.jpg")

try:
    img1 = load_image(url1)
    img2 = load_image(url2)

    # ปรับขนาดภาพให้เท่ากัน
    height = min(img1.shape[0], img2.shape[0])
    width = min(img1.shape[1], img2.shape[1])
    img1 = img1[:height, :width]
    img2 = img2[:height, :width]

    # เลือกโหมด blending
    mode = st.selectbox("Select blending mode", ['normal', 'multiply', 'screen', 'overlay'])
    # เลือก alpha
    alpha = st.slider("Blending ratio (alpha)", 0.0, 1.0, 0.5, 0.01)

    blended = blend_images(img1, img2, alpha, mode)

    # แสดงรูปภาพต้นฉบับ 2 รูป + รูป blended
    fig, axs = plt.subplots(1, 3, figsize=(15,5))
    axs[0].imshow(img1)
    axs[0].set_title('Image 1')
    axs[0].axis('on')  # show axis (x,y pixel)

    axs[1].imshow(img2)
    axs[1].set_title('Image 2')
    axs[1].axis('on')

    axs[2].imshow(blended)
    axs[2].set_title(f'Blended ({mode}, alpha={alpha:.2f})')
    axs[2].axis('on')

    st.pyplot(fig)

except Exception as e:
    st.error(f"Error loading images: {e}")
