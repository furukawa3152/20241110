import streamlit as st
import base64
from openai import OpenAI

api_key = st.sidebar.text_input("OpenAIのAPIキーを入力", type="password" )

client = OpenAI(api_key=api_key)


st.title("OCRアプリ（GPT編）")

uploaded_file = st.file_uploader("文字起こししたい画像を入れてね", type=["png","jpg","jpeg"])

if uploaded_file is not None and api_key:
    base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")

    messages = [
        {
            "role": "user",
            "content":[
                {"type":"text",
                 "text":"与えられる画像から「回答者の名前」と「このテーマに取り組んだ理由」をjson形式で返して下さい。"
                 },
                {"type":"image_url",
                 "image_url":{"url": f"data:image/jpeg;base64,{base64_image}"},
                 }
            ]

        }
    ]
    res = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages = messages,
        max_tokens=500
    )

    responce = res.choices[0].message.content
    st.write(responce)
    if responce:
        st.write("データを編集してください：")

        # デフォルト値を設定したフォーム
        with st.form("edit_form"):
            edited_text = st.text_input("テキスト", value=responce)