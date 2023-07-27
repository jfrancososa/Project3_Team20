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

with st.expander("Overview", expanded=True):
    st.write("Description")
with st.expander("Pomodoro Technique", expanded=False):
    st.write("Description")

st.divider()

### PDF Viewer ###
def show_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" ' \
                  f'width="800" height="1000" type="application/pdf"></embed>'
    st.markdown(pdf_display, unsafe_allow_html=True)


st.write("Upload a PDF file to get started")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    show_pdf(uploaded_file)
else:
    st.write("No file uploaded yet")


def reset_focus_time():
    st.session_state.focus_hours = 1
    st.session_state.focus_minutes = 30
    set_focus_time()
    st.session_state.focus_start = False
    st.session_state.focus_label = "Start"


def reset_break_time():
    st.session_state.break_hours = 0
    st.session_state.break_minutes = 5
    set_break_time()
    st.session_state.break_start = False
    st.session_state.break_label = "Start"


def set_focus_time():
    st.session_state.curr_focus_time = st.session_state.focus_hours * 3600 + st.session_state.focus_minutes * 60


def set_break_time():
    st.session_state.curr_break_time = st.session_state.break_hours * 3600 + st.session_state.break_minutes * 60


def format_focus_time(face):
    hrs = st.session_state.curr_focus_time // 3600
    mins = (st.session_state.curr_focus_time - hrs * 3600) // 60
    secs = st.session_state.curr_focus_time - hrs * 3600 - mins * 60
    face.markdown(f"**{hrs:02d}:{mins:02d}:{secs:02d}**")


def format_break_time(face):
    hrs = st.session_state.curr_break_time // 3600
    mins = (st.session_state.curr_break_time - hrs * 3600) // 60
    secs = st.session_state.curr_break_time - hrs * 3600 - mins * 60
    face.markdown(f"**{hrs:02d}:{mins:02d}:{secs:02d}**")


def focus_bttn_toggle():
    st.session_state.focus_start = not st.session_state.focus_start
    if st.session_state.focus_label == "Start":
        st.session_state.focus_label = "Stop"
    else:
        st.session_state.focus_label = "Start"


def break_bttn_toggle():
    st.session_state.break_start = not st.session_state.break_start
    if st.session_state.break_label == "Start":
        st.session_state.break_label = "Stop"
    else:
        st.session_state.break_label = "Start"


async def focus_timer(focus_face):
    while True:
        if not st.session_state:
            break
        st.session_state.curr_focus_time = max(0, st.session_state.curr_focus_time - 1)
        format_focus_time(focus_face)
        await asyncio.sleep(1)


async def break_timer(break_face):
    while True:
        if not st.session_state:
            break
        st.session_state.curr_break_time = max(0, st.session_state.curr_break_time - 1)
        format_break_time(break_face)
        await asyncio.sleep(1)


with st.sidebar:
    st.sidebar.header("Pomodoro's")
    if "pomodoro_count" not in st.session_state:
        st.session_state.pomodoro_count = 0
    if "pomodoro_total" not in st.session_state:
        st.session_state.pomodoro_total = 4
    st.write(f"Completed: {st.session_state.pomodoro_count}/{st.session_state.pomodoro_total}")

    st.sidebar.header("Task Time")
    if "focus_start" not in st.session_state:
        st.session_state.focus_start = False
    if "focus_label" not in st.session_state:
        st.session_state.focus_label = "Start"
    if "focus_hours" not in st.session_state:
        st.session_state.focus_hours = 1
    if "focus_minutes" not in st.session_state:
        st.session_state.focus_minutes = 30
    if "curr_focus_time" not in st.session_state:
        st.session_state.curr_focus_time = 0
        set_focus_time()

    hrs_col, mins_col = st.sidebar.columns(2)
    with hrs_col:
        focus_hours = st.number_input("Hours", key="focus_hours",
                                      min_value=0, max_value=24, on_change=set_focus_time)
    with mins_col:
        focus_minutes = st.number_input("Minutes", key="focus_minutes",
                                        min_value=0, max_value=60, on_change=set_focus_time)

    timer_col, reset_col, face_col = st.sidebar.columns([0.25, 0.25, 0.5])
    with timer_col:
        focus_button = st.button(label=st.session_state.focus_label, key="focus", on_click=focus_bttn_toggle)
    with reset_col:
        reset_button = st.button(label="Reset", key="focus_reset", on_click=reset_focus_time)
    with face_col:
        face = st.empty()
        format_focus_time(face)

    if st.session_state.focus_start:
        print("Timer started")
        asyncio.run(focus_timer(face))
    else:
        print("Timer stopped")

    st.sidebar.header("Break Time")
    if "break_start" not in st.session_state:
        st.session_state.break_start = False
    if "break_label" not in st.session_state:
        st.session_state.break_label = "Start"
    if "break_hours" not in st.session_state:
        st.session_state.break_hours = 0
    if "break_minutes" not in st.session_state:
        st.session_state.break_minutes = 5
    if "curr_break_time" not in st.session_state:
        st.session_state.curr_break_time = 0
        set_break_time()

    hrs_col, mins_col = st.sidebar.columns(2)
    with hrs_col:
        break_hours = st.number_input("Hours", key="break_hours",
                                      min_value=0, max_value=24, on_change=set_break_time)
    with mins_col:
        break_minutes = st.number_input("Minutes", key="break_minutes",
                                        min_value=0, max_value=60, on_change=set_break_time)
    timer_col, reset_col, face_col = st.sidebar.columns([0.25, 0.25, 0.5])
    with timer_col:
        break_button = st.button(label=st.session_state.break_label, key="break", on_click=break_bttn_toggle)
    with reset_col:
        reset_button = st.button(label="Reset", key="break_reset", on_click=reset_break_time)
    with face_col:
        face = st.empty()
        format_break_time(face)

    if st.session_state.break_start:
        print("Timer started")
        asyncio.run(break_timer(face))
    else:
        print("Timer stopped")
# st.write(st.session_state)
