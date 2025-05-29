import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🖼️ แสดงภาพจาก URL และดูภาพเต็ม")

# URLs ของภาพที่ใช้ได้แน่นอน
image_urls = [
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",  # Replaced URL
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/960px-Cat_August_2010-4.jpg"
]

# สร้างคอลัมน์ 3 รูป
cols = st.columns(3)
selected_index = None

for i, (col, url) in enumerate(zip(cols, image_urls)):
    with col:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Check for HTTP errors
            image = Image.open(BytesIO(response.content)).convert("RGB")
            st.image(image, caption=f"ภาพที่ {i+1}", use_column_width=True)
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

# แสดงภาพแบบเต็ม
if selected_index is not None:
    st.markdown("---")
    st.subheader(f"🔎 ภาพที่ {selected_index + 1} แบบเต็ม")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_urls[selected_index], headers=headers, timeout=10)
        response.raise_for_status()
        full_image = Image.open(BytesIO(response.content)).convert("RGB")
        st.image(full_image, use_column_width=True)
    except UnidentifiedImageError:
        st.error("❌ ไม่สามารถโหลดภาพแบบเต็มได้: รูปแบบภาพไม่ถูกต้อง")
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ ไม่สามารถโหลดภาพแบบเต็มได้: HTTP {e.response.status_code}")
    except requests.exceptions.RequestException:
        st.error("⚠️ ไม่สามารถโหลดภาพแบบเต็มได้: ปัญหาการเชื่อมต่อ")
    except Exception as e:
        st.error(f"❌ โหลดภาพแบบเต็มไม่สำเร็จ: {e}")
