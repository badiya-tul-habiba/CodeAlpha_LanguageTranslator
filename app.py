
import streamlit as st
import requests

st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Custom design and colors
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f3edff, #e9e5ff);
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

h1, h2, h3, p, label, .stMarkdown {
    color: #30234b !important;
}

.main-title {
    text-align: center;
    color: #542b91 !important;
    font-size: 38px;
    font-weight: 800;
}

.subtitle {
    text-align: center;
    color: #65547d !important;
    font-size: 16px;
}

div[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;
    color: #241b35 !important;
    border: 2px solid #c9b5ee !important;
    border-radius: 12px !important;
    font-size: 16px !important;
}

div[data-testid="stSelectbox"] div,
div[data-testid="stSelectbox"] input {
    color: #30234b !important;
}

div[data-testid="stSelectbox"] > div > div {
    background-color: #ffffff !important;
    border-radius: 10px;
}

.stButton > button {
    background: linear-gradient(90deg, #7545b5, #58318e);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 17px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background: #43236f;
    color: white !important;
    border: none;
}

.output-box {
    background-color: #ffffff;
    color: #241b35 !important;
    border: 2px solid #c9b5ee;
    border-radius: 12px;
    padding: 18px;
    min-height: 100px;
    font-size: 18px;
    line-height: 1.8;
    overflow-wrap: anywhere;
}

.footer {
    text-align: center;
    color: #75658c !important;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


LANGUAGES = {
    "English": "en-GB",
    "Urdu": "ur-PK",
    "Hindi": "hi-IN",
    "Arabic": "ar-SA",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "German": "de-DE",
    "Chinese": "zh-CN",
    "Japanese": "ja-JP",
    "Turkish": "tr-TR"
}


def translate_text(text, source, target):
    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    if data.get("responseStatus") != 200:
        raise Exception(
            data.get("responseDetails", "Translation failed.")
        )

    return data["responseData"]["translatedText"]


# App heading
st.markdown(
    '<h1 class="main-title">🌍 Language Translator</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Translate text easily between different languages</p>',
    unsafe_allow_html=True
)

st.write("")

# Language selection
col1, col2 = st.columns(2)

with col1:
    st.markdown("### From")
    source_language = st.selectbox(
        "Select source language",
        list(LANGUAGES.keys()),
        index=0
    )

with col2:
    st.markdown("### To")
    target_language = st.selectbox(
        "Select target language",
        list(LANGUAGES.keys()),
        index=1
    )

st.write("")

# Text input
st.markdown("### Enter Your Text")

user_text = st.text_area(
    "Write something to translate:",
    height=150,
    max_chars=450,
    placeholder="Type your text here..."
)

st.write("")

# Translation button
if st.button("✨ Translate Now", use_container_width=True):

    if not user_text.strip():
        st.warning("Please enter some text first.")

    elif source_language == target_language:
        st.warning("Please select two different languages.")

    else:
        try:
            with st.spinner("Translating your text..."):

                translated_text = translate_text(
                    user_text,
                    LANGUAGES[source_language],
                    LANGUAGES[target_language]
                )

            st.success("Translation completed successfully!")

            st.markdown("### Translated Text")

            st.markdown(
                f'<div class="output-box" dir="auto">{translated_text}</div>',
                unsafe_allow_html=True
            )

            st.download_button(
                "⬇️ Download Translation",
                data=translated_text,
                file_name="translated_text.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as error:
            st.error("Translation could not be completed.")
            st.write(str(error))

st.write("---")

st.markdown(
    '<p class="footer">Made with Python and Streamlit 💜</p>',
    unsafe_allow_html=True
)
