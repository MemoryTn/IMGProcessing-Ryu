import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้า Streamlit
st.set_page_config(page_title="Image Display App", page_icon="🖼️", layout="wide")

# หัวข้อ
st.title("แอปแสดงรูปภาพและขยายเมื่อคลิก")

# รายการ URL รูปภาพ (ตัวอย่างจาก Unsplash)
image_urls = [
    "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0",
    "https://images.unsplash.com/photo-1519337265831-2f69a06b26f4",
    "https://images.unsplash.com/photo-1472214103451-9374a3b28a2e"
]

# คำอธิบาย
st.write("คลิกที่รูปภาพเพื่อดูภาพขยาย")

# HTML และ CSS สำหรับการแสดงรูปภาพและ modal
html_code = """
<style>
.image-container {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
}
.thumbnail {
    width: 200px;
    height: 200px;
    object-fit: cover;
    cursor: pointer;
    transition: transform 0.2s;
    border-radius: 8px;
}
.thumbnail:hover {
    transform: scale(1.05);
}
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.8);
    justify-content: center;
    align-items: center;
}
.modal-content {
    max-width: 90%;
    max-height: 90%;
    border-radius: 8px;
}
.close-btn {
    position: absolute;
    top: 20px;
    right: 30px;
    color: white;
    font-size: 40px;
    cursor: pointer;
}
</style>

<div class="image-container">
"""

# เพิ่มรูปภาพลงใน HTML
for i, url in enumerate(image_urls):
    html_code += f"""
    <img src="{url}" class="thumbnail" onclick="openModal('modal{i}')" alt="Image {i+1}">
    <div id="modal{i}" class="modal">
        <span class="close-btn" onclick="closeModal('modal{i}')">×</span>
        <img src="{url}" class="modal-content">
    </div>
    """

# JavaScript สำหรับจัดการ modal
html_code += """
</div>
<script>
function openModal(modalId) {
    document.getElementById(modalId).style.display = "flex";
}
function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}
</script>
"""

# แสดง HTML ใน Streamlit
components.html(html_code, height=600)

# คำแนะนำการใช้งาน
st.markdown("""
### วิธีใช้งาน:
- คลิกที่รูปภาพเพื่อดูภาพขยาย
- คลิกที่เครื่องหมาย X หรือนอกภาพเพื่อปิด
""")
