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
# 画像の読み込み
img_org = Image.open("test1.png")
# OCR実行
builder = pyocr.builders.TextBuilder(tesseract_layout=3)
result = tool.image_to_string(img_org, lang="jpn", builder=builder)
print(result)
