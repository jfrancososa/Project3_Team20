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
    set_curr_time(mode)


def set_curr_time(mode):
    st.session_state[mode]["curr_time"] = st.session_state[mode]["hours"] * 3600 + \
                                          st.session_state[mode]["minutes"] * 60 + \
                                          st.session_state[mode]["seconds"]


def format_time(mode):
    hrs = st.session_state[mode]["curr_time"] // 3600
    mins = (st.session_state[mode]["curr_time"] - hrs * 3600) // 60
    secs = st.session_state[mode]["curr_time"] - hrs * 3600 - mins * 60
    return f"**{hrs:02d}:{mins:02d}:{secs:02d}**"


def reset_time(mode):
    st.session_state[mode]["curr_time"] = st.session_state[mode]["hours"] * 3600 + \
                                          st.session_state[mode]["minutes"] * 60 + \
                                          st.session_state[mode]["seconds"]
    st.session_state[mode]["state"] = False
    st.session_state[mode]["label"] = "Start"


def reset_count():
    st.session_state.pomodoro["count"] = 0
    st.session_state.pomodoro["focus_count"] = 0


def toggle_state(mode):
    st.session_state[mode]["state"] = not st.session_state[mode]["state"]
    if st.session_state[mode]["state"]:
        st.session_state[mode]["label"] = "Pause"
    else:
        st.session_state[mode]["label"] = "Start"


async def timer(mode, face):
    while True:
        if not st.session_state:
            print(f"Session State is empty - exiting {mode} timer")
            break
        if st.session_state[mode]["curr_time"] == 0:
            print(f"{mode.capitalize()} Timer is done")
            break
        st.session_state[mode]["curr_time"] = max(0, st.session_state[mode]["curr_time"] - 1)
        face.header(format_time(mode))
        await asyncio.sleep(1)

with st.sidebar:
    st.sidebar.title("Pomodoro Settings")

    # Pomodoro Counter ########################################################
    if "pomodoro" not in st.session_state:
        st.session_state["pomodoro"] = {
            "count": 0,
            "focus_count": 0,
            "complete": False,
        }
    complete_col, incomplete_col, reset_col = st.sidebar.columns(3)
    with complete_col:
        st.subheader("Completed: ")
    with incomplete_col:
        st.subheader(f"{st.session_state.pomodoro['count']}")
    with reset_col:
        st.button("Reset", key="pomodoro_reset", on_click=lambda: reset_count())
    st.write("*A complete Pomodoro consists of 1 focus session and 1 break session.")

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
            "focus_complete": False,
        }
        set_curr_time("focus")
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
            "rest_complete": False,
        }
        set_curr_time("rest")

    # Focus Timer #############################################################
    focus_container = st.sidebar.container()

    hr_col, min_col = st.sidebar.columns(2)
    # Hours Input #############################
    with hr_col:
        st.number_input("Hours", key="focus_hours",
                        min_value=0, max_value=24, value=1, step=1,
                        on_change=lambda: set_time("focus"))
    # Minutes Input ###########################
    with min_col:
        st.number_input("Minutes", key="focus_minutes",
                        min_value=0, max_value=60, value=30, step=1,
                        on_change=lambda: set_time("focus"))
    state_col, reset_col = st.sidebar.columns([0.5, 0.5])
    # Start/Pause Button ######################
    with state_col:
        st.button(st.session_state.focus["label"], key="focus_state",
                  on_click=lambda: toggle_state("focus"))
    # Reset Button ############################
    with reset_col:
        st.button("Reset", key="focus_reset",
                  on_click=lambda: reset_time("focus"))
    # Title and Timer #########################
    title_col, timer_col = focus_container.columns([0.5, 0.5])
    with title_col:
        st.subheader("Focus Timer")
    with timer_col:
        face = st.empty()
        if st.session_state.focus["state"]:
            asyncio.run(timer("focus", face))
            st.session_state.pomodoro["focus_count"] += 1
            st.session_state.focus["focus_complete"] = True
            reset_time("focus")
            st.experimental_rerun()
        else:
            face.subheader(format_time('focus'))


    # Break Timer #############################################################
    rest_container = st.sidebar.container()

    hr_col, min_col = st.sidebar.columns(2)
    # Hours Input #############################
    with hr_col:
        st.number_input("Hours", key="rest_hours",
                        min_value=0, max_value=24, value=0, step=1,
                        on_change=lambda: set_time("rest"))
    # Minutes Input ###########################
    with min_col:
        st.number_input("Minutes", key="rest_minutes",
                        min_value=0, max_value=60, value=5, step=1,
                        on_change=lambda: set_time("rest"))
    state_col, reset_col = st.sidebar.columns([0.5, 0.5])
    # Start/Pause Button ######################
    with state_col:
        st.button(st.session_state.rest["label"], key="rest_state",
                  on_click=lambda: toggle_state("rest"))
    # Reset Button ############################
    with reset_col:
        st.button("Reset", key="rest_reset",
                  on_click=lambda: reset_time("rest"))
    # Title and Timer #########################
    title_col, timer_col = rest_container.columns([0.5, 0.5])
    with title_col:
        st.subheader("Break Timer")
    with timer_col:
        face = st.empty()
        if st.session_state.rest["state"]:
            asyncio.run(timer("rest", face))
            if st.session_state.pomodoro["focus_count"] == 1:
                st.session_state.pomodoro["count"] += 1
                st.session_state.pomodoro["focus_count"] = 0
                st.session_state.pomodoro["complete"] = True
            st.session_state.rest["rest_complete"] = True
            reset_time("rest")
            st.experimental_rerun()
        else:
            face.subheader(format_time('rest'))

    # Display Timer Completion Messages #######################################
    if st.session_state.focus["focus_complete"]:
        st.info("Nice work! Take a break, you've earned it!")
        st.session_state.focus["focus_complete"] = False
    if st.session_state.rest["rest_complete"]:
        st.info("Rest complete! Start another focus session!")
        st.session_state.rest["rest_complete"] = False
    if st.session_state.pomodoro["complete"]:
        st.success("Congrats! You've completed a Pomodoro!")
        st.session_state.pomodoro["complete"] = False


# st.write(st.session_state)
