import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🖼️ แสดงภาพจาก URL และดูภาพเต็ม พร้อมปรับขนาดและหมุนภาพ")

image_urls = [
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/960px-Cat_August_2010-4.jpg"
]

# Slider สำหรับภาพเล็ก (ความกว้าง)
img_width = st.slider("ปรับขนาดความกว้างของรูปภาพเล็ก (พิกเซล)", min_value=100, max_value=600, value=300, step=10)

# สร้างคอลัมน์ 3 รูป พร้อมปุ่มเลือกภาพ
cols = st.columns(3)
selected_index = None

for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
            st.image(image, caption=f"ภาพที่ {i+1}", width=img_width)
            if st.button(f"🔍 ดูภาพที่ {i+1}", key=f"btn_{i}"):
                selected_index = i
        except UnidentifiedImageError:
            st.error(f"❌ ไม่สามารถเปิดภาพที่ {i+1} ได้: รูปแบบภาพไม่ถูกต้อง")
        except requests.exceptions.HTTPError as e:
            st.error(f"⚠️ ไม่สามารถโหลดภาพที่ {i+1}: HTTP {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ เกิดข้อผิดพลาดในภาพที่ {i+1}: ปัญหาการเชื่อมต่อ")
        except Exception as e:
            st.error(f"⚠️ เกิดข้อผิดพลาดในภาพที่ {i+1}: {e}")

# ถ้ามีการเลือกภาพ แสดง slider ปรับขนาดและหมุนภาพ ใต้ภาพเล็ก
if selected_index is not None:
    st.markdown("---")
    st.subheader(f"🔎 ภาพที่ {selected_index + 1} แบบเต็ม (matplotlib)")

    # สร้าง slider ในคอลัมน์เดียวใต้ปุ่มเลือกภาพ
    col_slider = st.columns([1, 3, 1])[1]  # จัดให้อยู่กลาง
    with col_slider:
        # ปรับขนาดภาพเต็ม (resize) เพื่อส่งให้ matplotlib
        full_img_scale = st.slider("ปรับขนาดภาพเต็ม (สัดส่วน scale)", min_value=10, max_value=100, value=100, step=5)
        rotate_degree = st.slider("หมุนภาพ (องศา)", min_value=0, max_value=360, value=0, step=5)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_urls[selected_index], headers=headers, timeout=10)
        response.raise_for_status()
        full_image = Image.open(BytesIO(response.content)).convert("RGB")

        # ปรับขนาดภาพเต็มตาม scale slider (scale เป็น % ของขนาดจริง)
        w, h = full_image.size
        new_w = int(w * full_img_scale / 100)
        new_h = int(h * full_img_scale / 100)
        resized_image = full_image.resize((new_w, new_h))

        # หมุนภาพ (expand=True เพื่อให้ภาพไม่ถูกตัด)
        rotated_image = resized_image.rotate(rotate_degree, expand=True)

        # แสดงด้วย matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(rotated_image)
        ax.set_xlabel('แกน X (พิกเซล)')
        ax.set_ylabel('แกน Y (พิกเซล)')
        ax.set_title(f"ภาพที่ {selected_index + 1} แบบเต็ม (ขนาด {new_w}x{new_h}px, หมุน {rotate_degree}°)")
        ax.axis('on')
        st.pyplot(fig)

    except UnidentifiedImageError:
        st.error("❌ ไม่สามารถโหลดภาพแบบเต็มได้: รูปแบบภาพไม่ถูกต้อง")
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ ไม่สามารถโหลดภาพแบบเต็มได้: HTTP {e.response.status_code}")
    except requests.exceptions.RequestException:
        st.error("⚠️ ไม่สามารถโหลดภาพแบบเต็มได้: ปัญหาการเชื่อมต่อ")
    except Exception as e:
        st.error(f"❌ โหลดภาพแบบเต็มไม่สำเร็จ: {e}")
