import streamlit as st
import pyocr.builders
import os
from PIL import Image

path_tesseract = "C:\Program Files\Tesseract-OCR"
# pathを通す
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract
# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

st.title("OCRアプリ")
uploaded_file = st.file_uploader("アップロード", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="アップロードされた画像です")
    # OCR実行
    builder = pyocr.builders.TextBuilder(tesseract_layout=3)
    result = tool.image_to_string(uploaded_image, lang="jpn", builder=builder)
    st.text(result)
    st.text_input("name")
