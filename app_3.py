import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from transformers import DetrForObjectDetection, DetrImageProcessor
import torch

model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")

def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

st.title("Object Detection with DETR (no YOLO, no OpenCV)")

url = st.text_input("Input image URL")

if url:
    image = load_image(url)
    st.image(image, caption="Input Image", use_column_width=True)

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Process output detections
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]

    # Draw boxes
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(1)
    ax.imshow(image)

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        if score > 0.7:
            box = box.tolist()
            x, y, x2, y2 = box
            width, height = x2 - x, y2 - y
            rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(x, y, f"{model.config.id2label[label.item()]}: {score:.2f}", color='white',
                    bbox=dict(facecolor='red', alpha=0.5))

    st.pyplot(fig)
