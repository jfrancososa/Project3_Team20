import streamlit as st
from os.path import basename
import base64
import asyncio

# Set streamlit to wide mode
st.set_page_config(layout="wide")

# Streamlit uses the file name as the title for the sidebar
# Just need to replace underscores with spaces and remove the file extension
FILE_NAME = basename(__file__)
PAGE_TITLE = FILE_NAME.split(".")[0].replace("_", " ")
st.title(PAGE_TITLE)

st.divider()

pdf_col, timer_col = st.columns([0.7, 0.3])


def show_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" ' \
                  f'width="800" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


with pdf_col:
    st.write("Upload a PDF file to get started")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file is not None:
        show_pdf(uploaded_file)
    else:
        st.write("No file uploaded yet")


def set_time():
    st.session_state.curr_time = st.session_state.hours * 3600 + st.session_state.minutes * 60


def bttn_toggle():
    st.session_state.timer_start = not st.session_state.timer_start
    if st.session_state.time_label == "Start":
        st.session_state.time_label = "Stop"
    else:
        st.session_state.time_label = "Start"


async def timer(face):
    while True:
        st.session_state.curr_time -= 1
        hrs = st.session_state.curr_time // 3600
        mins = (st.session_state.curr_time - hrs * 3600) // 60
        secs = st.session_state.curr_time - hrs * 3600 - mins * 60
        face.markdown(f"**{hrs:02d}:{mins:02d}:{secs:02d}**")
        await asyncio.sleep(1)


face = st.empty()
with timer_col:
    st.header("Timer")
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = False
    if "time_label" not in st.session_state:
        st.session_state.time_label = "Start"
    if "hours" not in st.session_state:
        st.session_state.hours = 1
    if "minutes" not in st.session_state:
        st.session_state.minutes = 30

    hrs_col, mins_col = st.columns(2)
    with hrs_col:
        hours = st.number_input("Hours", key="hours", min_value=0, max_value=24, on_change=set_time)
    with mins_col:
        minutes = st.number_input("Minutes", key="minutes", min_value=0, max_value=60, on_change=set_time)
    timer_col, face_col = st.columns(2)
    with timer_col:
        timer_button = st.button(label=st.session_state.time_label, on_click=bttn_toggle)

    if st.session_state.timer_start:
        st.write("Timer started")
        asyncio.run(timer(face))
    else:
        st.write("Timer stopped")

# st.write(st.session_state)
