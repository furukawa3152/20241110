import streamlit as st
import base64
from openai import OpenAI
import json
import requests

api_key = st.sidebar.text_input("OpenAIのAPIキーを入力", type="password")

client = OpenAI(api_key=api_key)

st.title("名刺OCRアプリ")

uploaded_file = st.file_uploader("名刺の画像を入れてください。", type=["png", "jpg", "jpeg","HEIC"])

if uploaded_file is not None and api_key:
    base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": "以下に名刺の画像を与えます。内容を読み取り、「氏名」、「会社名」、「電話番号1」、「電話番号2」、「住所」、「メールアドレス1」,"
                         "「メールアドレス2」、「備考」の8項目のキーを持つでjson形式で返してください。回答はjson飲みを返すこと。読み取れない項目については、バリューは空白で返して下さい。回答は必ず有効なJSON形式のみで返してください。"
                 },
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                 }
            ]

        }
    ]
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500
    )

    response_content = res.choices[0].message.content
    st.write(response_content)
    # JSON形式の確認と整形
    if not response_content.startswith("{"):
        response_content = response_content[response_content.find("{"):response_content.rfind("}") + 1]
    # JSON形式のチェックと変換
    try:
        response_json = json.loads(response_content)
    except json.JSONDecodeError:
        st.error("APIレスポンスが有効なJSON形式ではありません。以下のレスポンスを確認してください。")
        st.write(response_content)
        st.stop()

    # 各項目の取得
    re_name = response_json["氏名"]
    re_company = response_json["会社名"]
    re_tel1 = response_json["電話番号1"]
    re_tel2 = response_json["電話番号2"]
    re_address = response_json["住所"]
    re_mail1 = response_json["メールアドレス1"]
    re_mail2 = response_json["メールアドレス2"]
    re_memo = response_json["備考"]

    # 編集フォーム
    st.write("データを編集してください：")
    with st.form("edit_form"):
        edited_name_text = st.text_input("氏名", value=re_name)
        edited_company_text = st.text_input("会社名", value=re_company)
        edited_tel1_text = st.text_input("電話番号1", value=re_tel1)
        edited_tel2_text = st.text_input("電話番号2", value=re_tel2)
        edited_address_text = st.text_input("住所", value=re_address)
        edited_mail_text1 = st.text_input("メールアドレス", value=re_mail1)
        edited_mail_text2 = st.text_input("メールアドレス", value=re_mail2)
        edited_memo_text = st.text_input("備考", value=re_memo)

        submit_button = st.form_submit_button("送信")
        if submit_button:
            url = f"https://script.google.com/macros/s/AKfycbxG7jYN0QuAAfuLrlI6X9R7vMU34UPYk1pgiqz8vQxwpB97Ic1JfG0v722UUO9jaJmztA/exec?data_col1={edited_name_text}&data_col2={edited_company_text}&data_col3={edited_tel1_text}&data_col4={edited_tel2_text}&data_col5={edited_address_text}&data_col6={edited_mail_text1}&data_col7={edited_mail_text2}&data_col8={edited_memo_text}"
            requests.get(url)
            st.write("データを登録しました。")
