import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🖼️ Display Images from URL with Zoom and Rotation")

image_urls = [
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/960px-Cat_August_2010-4.jpg"
]

# สร้างคอลัมน์ 3 รูป พร้อมปุ่มเลือกภาพ
cols = st.columns(3)

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
            st.image(image, caption=f"Image {i+1}", width=300)  # fix ขนาดรูปเล็กไว้ที่ 300 px
            if st.button(f"🔍 View Image {i+1}", key=f"btn_{i}"):
                st.session_state.selected_index = i
        except UnidentifiedImageError:
            st.error(f"❌ Cannot open Image {i+1}: Unsupported image format")
        except requests.exceptions.HTTPError as e:
            st.error(f"⚠️ Cannot load Image {i+1}: HTTP {e.response.status_code}")
        except requests.exceptions.RequestException:
            st.error(f"⚠️ Connection error loading Image {i+1}")
        except Exception as e:
            st.error(f"⚠️ Error loading Image {i+1}: {e}")

if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader(f"🔎 Full view of Image {st.session_state.selected_index + 1} (matplotlib)")

    # Sliders on top of the image
    full_img_scale = st.slider("Resize full image (%)", min_value=10, max_value=100, value=50, step=5)
    rotate_degree = st.slider("Rotate image (degrees)", min_value=0, max_value=360, value=0, step=5)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_urls[st.session_state.selected_index], headers=headers, timeout=10)
        response.raise_for_status()
        full_image = Image.open(BytesIO(response.content)).convert("RGB")

        # Resize and rotate
        w, h = full_image.size
        new_w = int(w * full_img_scale / 100)
        new_h = int(h * full_img_scale / 100)
        resized_image = full_image.resize((new_w, new_h))
        rotated_image = resized_image.rotate(rotate_degree, expand=True)

        # Show with matplotlib, smaller figure size
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(rotated_image)
        ax.set_xlabel('X axis (pixels)', fontsize=9)
        ax.set_ylabel('Y axis (pixels)', fontsize=9)
        ax.set_title(f"Image {st.session_state.selected_index + 1} (Size: {new_w}x{new_h}px, Rotation: {rotate_degree}°)", fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.axis('on')

        st.pyplot(fig)

    except UnidentifiedImageError:
        st.error("❌ Cannot load full image: Unsupported image format")
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ Cannot load full image: HTTP {e.response.status_code}")
    except requests.exceptions.RequestException:
        st.error("⚠️ Cannot load full image: Connection error")
    except Exception as e:
        st.error(f"❌ Failed to load full image: {e}")
