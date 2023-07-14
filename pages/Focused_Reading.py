import streamlit as st
from os.path import basename
import base64

# Streamlit uses the file name as the title for the sidebar
# Just need to replace underscores with spaces and remove the file extension
FILE_NAME = basename(__file__)
PAGE_TITLE = FILE_NAME.split(".")[0].replace("_", " ")
st.title(PAGE_TITLE)

st.divider()

st.write("Upload a PDF file to get started")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")


def show_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" ' \
                  f'width="800" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


if uploaded_file is not None:
    show_pdf(uploaded_file)
else:
    st.write("No file uploaded yet")
