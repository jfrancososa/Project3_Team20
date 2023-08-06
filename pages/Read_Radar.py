import streamlit as st
from os.path import basename
import base64
import asyncio

from pages.utils.read_radar import *
from pages.utils.eye_tracker import EyeTracker

# Set streamlit to wide mode
st.set_page_config(layout="wide")

# Streamlit uses the file name as the title for the sidebar
# Just need to replace underscores with spaces and remove the file extension
FILE_NAME = basename(__file__)
PAGE_TITLE = FILE_NAME.split(".")[0].replace("_", " ")
title_col, capture_col = st.columns([0.75, 0.25])

with title_col:
    st.title(PAGE_TITLE)


async def frame_analysis(container):
    while st.session_state.eye_tracker.capture.isOpened():
        tracker_frame = st.session_state.eye_tracker.track_blinks()
        if len(tracker_frame) == 0:
            break
        container.image(tracker_frame, channels="BGR", use_column_width=True)
        await asyncio.sleep(0.1)


with capture_col:
    if "eye_tracker" not in st.session_state:
        st.session_state.eye_tracker = EyeTracker()
    if "display_feed" not in st.session_state:
        st.session_state.display_feed = False
    with st.expander("Blink Tracker"):
        camera_container = st.empty()
        st.write("Click the button below to start the webcam capture")
        buttons_col, count_col = st.columns([0.55, 0.45])
        with buttons_col:
            if st.button("Start Eye Capture"):
                st.session_state.eye_tracker.start_capture()
                st.session_state.display_feed = True
            if st.button("Stop Eye Capture"):
                st.session_state.eye_tracker.stop_capture()
                st.session_state.display_feed = False
        with count_col:
            st.write("Session Blinks")
            st.write(st.session_state.eye_tracker.get_blink_count())

with st.expander("Overview", expanded=True):
    st.write("This page provides a pomodoro style timer in the sidebar with a built-in pdf viewer that allows you to "
             "manage your productivity while reading. An explanation of the Pomodoro technique is included below and "
             "default timer values are already set, you just press the start button and the time will automatically "
             "count down as you focus on reading.")
with st.expander("Pomodoro Technique", expanded=False):
    st.markdown("From the Wikipedia article for the "
                "[Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique), "
                "the Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. "
                "It uses a kitchen timer to break work into intervals, typically 25 minutes in length, separated by "
                "short breaks. Each interval is known as a pomodoro, from the Italian word for tomato, after the "
                "tomato-shaped kitchen timer Cirillo used as a university student.")
    st.markdown("""
    The original technique has six steps:
    1. Decide on the task to be done.
    2. Set the pomodoro timer (traditionally to 25 minutes).
    3. Work on the task.
    4. End work when the timer rings and take a short break (typically 5-10 minutes). 
    5. Go back to Step 2 and repeat until you complete four pomodoros.
    6. After four pomodoros are done, take a long break (typically 20 to 30 minutes) instead of a short break. Once the
    long break is finished return to step 2. 
    """)

st.divider()


# PDF Viewer ####
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


# Pomodoro Counter and Timers ################################################
# Utility Functions
async def timer(mode, output):
    while True:
        if not st.session_state:
            st.stop()
        if st.session_state[mode]["curr_time"] == 0:
            break
        st.session_state[mode]["curr_time"] = max(0, st.session_state[mode]["curr_time"] - 1)
        output.subheader(format_time(mode, st.session_state))
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
    complete_col, incomplete_col, reset_col = st.sidebar.columns([0.5, 0.25, 0.25])
    with complete_col:
        with st.expander("Completed"):
            st.write("A complete Pomodoro consists of 1 focus session and 1 break session.")
    with incomplete_col:
        st.subheader(f"{st.session_state['pomodoro']['count']}")
    with reset_col:
        st.button("Reset", key="pomodoro_reset", on_click=lambda: reset_count(st.session_state))

    # Timers ##################################################################
    # Set Session Values for Focus and Break Timers ###########################
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
        set_curr_time("focus", st.session_state)
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
        set_curr_time("rest", st.session_state)

    # Focus Timer #############################################################
    focus_container = st.sidebar.container()

    hr_col, min_col = st.sidebar.columns(2)
    # Hours Input #############################
    with hr_col:
        st.number_input("Hours", key="focus_hours",
                        min_value=0, max_value=24, value=st.session_state["focus"]["default_hours"], step=1,
                        on_change=lambda: set_time("focus", st.session_state))
    # Minutes Input ###########################
    with min_col:
        st.number_input("Minutes", key="focus_minutes",
                        min_value=0, max_value=60, value=st.session_state["focus"]["default_minutes"], step=1,
                        on_change=lambda: set_time("focus", st.session_state))
    state_col, reset_col = st.sidebar.columns([0.5, 0.5])
    # Start/Pause Button ######################
    with state_col:
        st.button(st.session_state["focus"]["label"], key="focus_state",
                  on_click=lambda: toggle_state("focus", st.session_state))
    # Reset Button ############################
    with reset_col:
        st.button("Reset", key="focus_reset",
                  on_click=lambda: reset_time("focus", st.session_state))
    # Title and Timer #########################
    title_col, timer_col = focus_container.columns([0.5, 0.5])
    with title_col:
        st.subheader("Focus Timer")
    with timer_col:
        face = st.empty()
        if st.session_state["focus"]["state"]:
            asyncio.run(timer("focus", face))
            st.session_state["pomodoro"]["focus_count"] += 1
            st.session_state["focus"]["focus_complete"] = True
            reset_time("focus", st.session_state)
            st.experimental_rerun()
        else:
            face.subheader(format_time('focus', st.session_state))

    # Break Timer #############################################################
    rest_container = st.sidebar.container()

    hr_col, min_col = st.sidebar.columns(2)
    # Hours Input #############################
    with hr_col:
        st.number_input("Hours", key="rest_hours",
                        min_value=0, max_value=24, value=0, step=1,
                        on_change=lambda: set_time("rest", st.session_state))
    # Minutes Input ###########################
    with min_col:
        st.number_input("Minutes", key="rest_minutes",
                        min_value=0, max_value=60, value=5, step=1,
                        on_change=lambda: set_time("rest", st.session_state))
    state_col, reset_col = st.sidebar.columns([0.5, 0.5])
    # Start/Pause Button ######################
    with state_col:
        st.button(st.session_state["rest"]["label"], key="rest_state",
                  on_click=lambda: toggle_state("rest", st.session_state))
    # Reset Button ############################
    with reset_col:
        st.button("Reset", key="rest_reset",
                  on_click=lambda: reset_time("rest", st.session_state))
    # Title and Timer #########################
    title_col, timer_col = rest_container.columns([0.5, 0.5])
    with title_col:
        st.subheader("Break Timer")
    with timer_col:
        face = st.empty()
        if st.session_state["rest"]["state"]:
            asyncio.run(timer("rest", face))
            # Check if pomodoro is complete by checking if the focus count is 1
            if st.session_state["pomodoro"]["focus_count"] == 1:
                st.session_state["pomodoro"]["count"] += 1
                st.session_state["pomodoro"]["focus_count"] = 0
                st.session_state["pomodoro"]["complete"] = True
            st.session_state["rest"]["rest_complete"] = True
            reset_time("rest", st.session_state)
            st.experimental_rerun()
        else:
            face.subheader(format_time('rest', st.session_state))

    # Display Timer Completion Messages #######################################
    if st.session_state["focus"]["focus_complete"]:
        st.info("Nice work! Take a break, you've earned it!")
        st.session_state["focus"]["focus_complete"] = False
    if st.session_state["rest"]["rest_complete"]:
        st.info("Rest complete! Start another focus session!")
        st.session_state["rest"]["rest_complete"] = False
    if st.session_state["pomodoro"]["complete"]:
        st.success("Congrats! You've completed a Pomodoro!")
        st.session_state["pomodoro"]["complete"] = False

    st.divider()

    # Task List ###############################
    st.title("Task List")
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = {}
    if "task_id" not in st.session_state:
        st.session_state["task_id"] = 0

    checkmark_col, task_name_col, settings_col = st.columns([0.1, 0.7, 0.2])
    for task_id in st.session_state["tasks"]:
        task = st.session_state["tasks"][task_id]
        with checkmark_col:
            st.checkbox("Complete", label_visibility="collapsed", key=f"{task_id}_state",
                        on_change=lambda: toggle_tasks(st.session_state), )
        with task_name_col:
            st.text_input("Name", task["title"], label_visibility="collapsed", key=f"{task_id}_title",
                          disabled=task["status"])
        with settings_col:
            if st.button("delete", key=f"{task_id}_delete"):
                remove_task(task_id, st.session_state)
                st.experimental_rerun()
    with checkmark_col:
        st.checkbox("Complete", disabled=True, key="new_checkmark", label_visibility="collapsed")
    with task_name_col:
        st.text_input("Title", placeholder="ex. read 3 pages", label_visibility="collapsed",
                      key=f"{st.session_state['task_id']}_title")
    with settings_col:
        if st.button("add", key="create_task"):
            add_task(st.session_state)
            st.experimental_rerun()

# st.write(st.session_state)


if st.session_state.display_feed:
    asyncio.run(frame_analysis(camera_container))
