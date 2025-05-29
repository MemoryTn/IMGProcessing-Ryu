import streamlit as st
import streamlit.components.v1 as components
from skimage import io, color
from skimage.filters import threshold_otsu, sobel
from skimage.util import random_noise
from skimage.restoration import denoise_tv_chambolle
from scipy.ndimage import gaussian_filter, median_filter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ตั้งค่าหน้า Streamlit
st.set_page_config(page_title="Image Processing App", page_icon="🖼️", layout="wide")

# หัวข้อ
st.title("แอปประมวลผลรูปภาพ")

# รายการ URL รูปภาพ
image_urls = {
    "ภาพที่ 1": "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0",
    "ภาพที่ 2": "https://images.unsplash.com/photo-1519337265831-2f69a06b26f4",
    "ภาพที่ 3": "https://images.unsplash.com/photo-1472214103451-9374a3b28a2e"
}

# แสดงภาพตัวอย่างและจัดการการขยาย
st.subheader("เลือกรูปภาพ")
cols = st.columns(3)
html_code = """
<style>
.thumbnail { width: 100%; height: auto; cursor: pointer; border-radius: 8px; }
.thumbnail:hover { transform: scale(1.05); transition: transform 0.2s; }
.modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8); justify-content: center; align-items: center; }
.modal-content { max-width: 90%; max-height: 90%; border-radius: 8px; }
.close-btn { position: absolute; top: 20px; right: 30px; color: white; font-size: 40px; cursor: pointer; }
</style>
<div class="image-container" style="display: flex; gap: 15px; flex-wrap: wrap; justify-content: center;">
"""

if 'selected_image_url' not in st.session_state:
    st.session_state.selected_image_url = None

for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        st.image(url, caption=name, use_container_width=True)
        if st.button(f"เลือก {name}", key=f"btn_{i}"):
            st.session_state.selected_image_url = url
    html_code += f"""
    <img src="{url}" class="thumbnail" onclick="openModal('modal{i}')" alt="{name}">
    <div id="modal{i}" class="modal">
        <span class="close-btn" onclick="closeModal('modal{i}')">×</span>
        <img src="{url}" class="modal-content">
    </div>
    """

html_code += """
</div>
<script>
function openModal(modalId) { document.getElementById(modalId).style.display = "flex"; }
function closeModal(modalId) { document.getElementById(modalId).style.display = "none"; }
</script>
"""
components.html(html_code, height=300)

# ถ้ามีการเลือกภาพ
if st.session_state.selected_image_url:
    st.subheader("ผลลัพธ์การประมวลผลภาพ")
    image = io.imread(st.session_state.selected_image_url)

    # แปลงเป็นสีเทา
    gray_image = color.rgb2gray(image)
    thresh = threshold_otsu(gray_image)
    binary_image = gray_image > thresh
    edge_image = sobel(gray_image)

    # แสดงผลลัพธ์
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ภาพสีเทา")
        fig1, ax1 = plt.subplots()
        ax1.imshow(gray_image, cmap='gray')
        ax1.axis('off')
        st.pyplot(fig1)
    with col2:
        st.markdown("### ภาพขาวดำ")
        fig2, ax2 = plt.subplots()
        ax2.imshow(binary_image, cmap='gray')
        ax2.axis('off')
        st.pyplot(fig2)

    st.markdown("### ภาพขอบ")
    fig3, ax3 = plt.subplots()
    ax3.imshow(edge_image, cmap='gray')
    ax3.axis('off')
    st.pyplot(fig3)

    # ปรับความสว่าง
    st.subheader("ปรับความสว่าง")
    brightness = st.slider("ความสว่าง", -50, 50, 0, step=1, key="bright")
    enhanced_rgb = np.clip(image.astype(np.int16) + brightness, 0, 255).astype(np.uint8)
    st.image(enhanced_rgb, caption="ภาพหลังปรับความสว่าง", use_container_width=True)

    # เพิ่ม Noise
    st.subheader("เพิ่ม Noise")
    noise_type = st.selectbox("ประเภท Noise", ["gaussian", "salt", "pepper", "s&p"], key="noise")
    if noise_type == "gaussian":
        var = st.slider("ความรุนแรง (variance)", 0.001, 0.1, 0.01, step=0.001, key="var")
        noisy_image = random_noise(enhanced_rgb, mode=noise_type, var=var)
    else:
        amount = st.slider("ระดับ Noise", 0.01, 0.2, 0.05, step=0.01, key="amount")
        noisy_image = random_noise(enhanced_rgb, mode=noise_type, amount=amount)
    noisy_image_uint8 = (np.clip(noisy_image, 0, 1) * 255).astype(np.uint8)
    st.image(noisy_image_uint8, caption="ภาพหลังเพิ่ม Noise", use_container_width=True)

    # ฟื้นฟูภาพ
    st.subheader("ฟื้นฟูภาพ")
    restoration_method = st.selectbox("วิธีการฟื้นฟู", ["Median Filter", "Gaussian Filter", "Total Variation (TV) Denoising"], key="restore")
    def restore_rgb(image, method):
        restored = np.zeros_like(image, dtype=np.float32)
        for c in range(3):
            channel = image[:, :, c]
            if method == "Median Filter":
                restored[:, :, c] = median_filter(channel, size=3)
            elif method == "Gaussian Filter":
                restored[:, :, c] = gaussian_filter(channel, sigma=1)
            elif method == "Total Variation (TV) Denoising":
                restored[:, :, c] = denoise_tv_chambolle(channel, weight=0.1)
        return np.clip(restored, 0, 1)
    restored_image = restore_rgb(noisy_image, restoration_method)
    restored_image_uint8 = (restored_image * 255).astype(np.uint8)
    st.image(restored_image_uint8, caption="ภาพหลังฟื้นฟู", use_container_width=True)

    # ปรับความคมชัด
    st.subheader("ปรับความคมชัด")
    contrast_factor = st.slider("ระดับความคมชัด", 0.5, 2.0, 1.0, step=0.1, key="contrast")
    def adjust_contrast(image, factor):
        image_float = image.astype(np.float32) / 255.0
        mean = np.mean(image_float, axis=(0, 1), keepdims=True)
        adjusted = (image_float - mean) * factor + mean
        return (np.clip(adjusted, 0, 1) * 255).astype(np.uint8)
    contrast_image = adjust_contrast(enhanced_rgb, contrast_factor)
    st.image(contrast_image, caption="ภาพหลังปรับความคมชัด", use_container_width=True)

    # Histogram
    st.subheader("Histogram สี")
    r, g, b = contrast_image[:, :, 0].flatten(), contrast_image[:, :, 1].flatten(), contrast_image[:, :, 2].flatten()
    fig_hist, ax_hist = plt.subplots()
    ax_hist.hist(r, bins=256, color='red', alpha=0.5, label='R')
    ax_hist.hist(g, bins=256, color='green', alpha=0.5, label='G')
    ax_hist.hist(b, bins=256, color='blue', alpha=0.5, label='B')
    ax_hist.set_title("Histogram of RGB Channels")
    ax_hist.set_xlabel("Pixel Intensity")
    ax_hist.set_ylabel("Pixel Count")
    ax_hist.legend()
    st.pyplot(fig_hist)
