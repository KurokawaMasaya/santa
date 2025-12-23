import streamlit as st

# 設定頁面為全螢幕模式，並隱藏 Streamlit 的預設元件
st.set_page_config(page_title="Merry Christmas 🎄", layout="wide", initial_sidebar_state="collapsed")

# 讀取 index.html 的內容
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 使用 markdown 的 unsafe_allow_html 來注入全螢幕的 HTML
# 這樣做可以確保沒有 Streamlit 討厭的白色邊距
st.markdown(f"""
    <style>
        /* 移除 Streamlit 預設的 Padding 和 Margin */
        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }}
        header, footer {{
            display: none !important;
        }}
        /* 強制 iframe 全螢幕 */
        iframe {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            border: none;
            z-index: 99999;
        }}
    </style>
    """, unsafe_allow_html=True)

# 渲染 HTML
st.components.v1.html(html_code, height=1000, scrolling=False)
