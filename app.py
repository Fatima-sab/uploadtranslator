import os
from gtts import gTTS
from googletrans import Translator
from docx import Document
import tempfile
import io
import streamlit as st

# Initialize the Translator
translator = Translator()

# Streamlit UI
st.title("Document Translation and Audio Pronunciation")
st.subheader("Upload a .txt or .docx file to translate and listen to the audio pronunciation in Urdu")

# File uploader for .txt and .docx files
uploaded_file = st.file_uploader("Choose a .txt or .docx file", type=["txt", "docx"])

# Extract text from the .docx file
def extract_text_from_docx(docx_file):
    docx_file = io.BytesIO(docx_file)
    document = Document(docx_file)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

# Extract text from a .txt file
def extract_text_from_txt(txt_file):
    text = txt_file.decode("utf-8")
    return text

# Translate text to Urdu using googletrans
def translate_text(text):
    translation = translator.translate(text, dest='ur')
    return translation.text

# Generate audio pronunciation using gTTS
def generate_audio(text, lang='ur'):
    tts = gTTS(text=text, lang=lang)
    temp_audio_path = tempfile.mktemp(suffix='.mp3')
    tts.save(temp_audio_path)
    return temp_audio_path

# Process the uploaded document
if uploaded_file is not None:
    # Check file type and extract text
    if uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file.getvalue())
    elif uploaded_file.name.endswith(".txt"):
        text = extract_text_from_txt(uploaded_file.getvalue())
    else:
        st.error("Unsupported file format.")
        st.stop()
    
    # Display original text
    st.subheader("Original Text")
    st.text_area("Original Text", text, height=200)

    # Translate text to Urdu
    translated_text = translate_text(text)
    st.subheader("Translated Text (Urdu)")
    st.text_area("Translated Text", translated_text, height=200)

    # Generate audio from translated text
    audio_path = generate_audio(translated_text)
    
    # Display audio player
    st.subheader("Audio Pronunciation")
    st.audio(audio_path)
