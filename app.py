import streamlit as st
from gtts import gTTS
from googletrans import Translator
import tempfile
import os
from docx import Document

# Initialize the Translator
translator = Translator()

# Streamlit app title
st.title("Document Translator and Pronunciation")

# Allow the user to upload a file
uploaded_file = st.file_uploader("Upload a document (.txt or .docx)", type=["txt", "docx"])

def extract_text_from_docx(docx_file):
    # Extract text from a .docx file
    document = Document(docx_file)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_txt(txt_file):
    # Extract text from a .txt file
    text = txt_file.read().decode("utf-8")
    return text

# Function to translate text to Urdu
@st.cache
def get_translation(text):
    return translator.translate(text, dest='ur').text

# Function to generate pronunciation (audio) for the translated text
@st.cache
def get_pronunciation(text):
    try:
        tts = gTTS(text=text, lang='ur')  # Convert to Urdu pronunciation
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

# If a file is uploaded
if uploaded_file is not None:
    # Extract text from the file
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        text = extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file type")
        text = ""

    if text:
        # Show the original text
        st.subheader("Original Text")
        st.write(text)

        # Translate the text to Urdu
        translated_text = get_translation(text)
        st.subheader("Translated Text (Urdu)")
        st.write(translated_text)

        # Play the pronunciation of the translated text
        if st.button("Play Pronunciation"):
            pronunciation_file = get_pronunciation(translated_text)
            if pronunciation_file:
                st.audio(pronunciation_file)
                os.remove(pronunciation_file)  # Clean up the temporary file
