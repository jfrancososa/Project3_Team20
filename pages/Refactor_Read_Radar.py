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


# PDF Viewer ###
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


# Pomodoro Counter and Timers ###
# Utility Functions


def set_time(mode):
    hr_button_key = f"{mode}_hours"
    hr_button_value = st.session_state[hr_button_key]
    min_button_key = f"{mode}_minutes"
    min_button_value = st.session_state[min_button_key]
    st.session_state[mode]["hours"] = hr_button_value
    st.session_state[mode]["minutes"] = min_button_value
    st.session_state[mode]["curr_time"] = st.session_state[mode]["hours"] * 3600 + \
                                          st.session_state[mode]["minutes"] * 60 + \
                                          st.session_state[mode]["seconds"]


def format_time(mode):
    hours = st.session_state[mode]["curr_time"] // 3600
    minutes = (st.session_state[mode]["curr_time"] % 3600) // 60
    seconds = ((st.session_state[mode]["curr_time"] % 3600) // 60) % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def reset_time(mode):
    st.session_state[mode]["curr_time"] = st.session_state[mode]["hours"] * 3600 + \
                                          st.session_state[mode]["minutes"] * 60 + \
                                          st.session_state[mode]["seconds"]
    st.session_state[mode]["state"] = False
    st.session_state[mode]["label"] = "Start"


def toggle_state(mode):
    st.session_state[mode]["state"] = not st.session_state[mode]["state"]
    if st.session_state[mode]["state"]:
        st.session_state[mode]["label"] = "Pause"
    else:
        st.session_state[mode]["label"] = "Start"


async def timer(mode):
    while True:
        if not st.session_state:
            break
        st.session_state[mode]["curr_time"] = max(0, st.session_state[mode]["curr_time"] - 1)
        format_time(mode)
        await asyncio.sleep(1)

with st.sidebar:
    if "pomodoro" not in st.session_state:
        st.session_state["pomodoro"] = {
            "count": 0,
            "total": 4,
            "default_count": 0,
            "default_total": 4,
        }
    st.sidebar.title("Pomodoro Counter")
    st.write(f"Completed: {st.session_state.pomodoro['count']}/{st.session_state.pomodoro['total']}")

    # Set Session Values for Focus and Break Timers
    if "focus" not in st.session_state:
        st.session_state["focus"] = {
            "hours": 1,
            "minutes": 30,
            "seconds": 0,
            "default_hours": 1,
            "default_minutes": 30,
            "default_seconds": 0,
            "state": False,
            "label": "Start",
            "curr_time": 0,
        }
    if "rest" not in st.session_state:
        st.session_state["rest"] = {
            "hours": 0,
            "minutes": 5,
            "seconds": 0,
            "default_hours": 0,
            "default_minutes": 5,
            "default_seconds": 0,
            "state": False,
            "label": "Start",
            "curr_time": 0,
        }

    # Focus Timer #############################################################
    title_col, timer_col = st.sidebar.columns([0.5, 0.5])
    with title_col:
        st.header("Focus Timer")
    with timer_col:
        if st.session_state.focus["state"]:
            asyncio.run(timer("focus"))
        else:
            st.header(f"{format_time('focus')}")

    hr_col, min_col = st.sidebar.columns(2)
    with hr_col:
        st.number_input("Hours", key="focus_hours",
                        min_value=0, max_value=24, value=1, step=1,
                        on_change=lambda: set_time("focus"))
    with min_col:
        st.number_input("Minutes", key="focus_minutes",
                        min_value=0, max_value=60, value=30, step=1,
                        on_change=lambda: set_time("focus"))
    state_col, reset_col = st.sidebar.columns([0.5, 0.5])
    with state_col:
        st.button(st.session_state.focus["label"], key="focus_state",
                  on_click=lambda: toggle_state("focus"))
    with reset_col:
        st.button("Reset", key="focus_reset",
                  on_click=lambda: reset_time("focus"))

    # Break Timer #############################################################
    title_col, timer_col = st.sidebar.columns([0.5, 0.5])
    with title_col:
        st.header("Break Timer")
    with timer_col:
        st.header(f"{format_time('rest')}")

    hr_col, min_col = st.sidebar.columns(2)
    with hr_col:
        st.number_input("Hours", key="rest_hours",
                        min_value=0, max_value=24, value=0, step=1,
                        on_change=lambda: set_time("rest"))
    with min_col:
        st.number_input("Minutes", key="rest_minutes",
                        min_value=0, max_value=60, value=5, step=1,
                        on_change=lambda: set_time("rest"))
    state_col, reset_col = st.sidebar.columns([0.5, 0.5])
    with state_col:
        st.button(st.session_state.rest["label"], key="rest_state",
                  on_click=lambda: toggle_state("rest"))
    with reset_col:
        st.button("Reset", key="rest_reset",
                  on_click=lambda: reset_time("rest"))

    if st.session_state.rest["state"]:
        print("Break Timer Running")
        print("Calling async function")
    else:
        print("Break Timer Stopped")

st.write(st.session_state)
