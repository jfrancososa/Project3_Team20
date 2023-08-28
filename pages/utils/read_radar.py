# TODO: Add comments
# TODO: Specify state value instead of passing session_state
# TODO: Update async time function so that it can be imported from here
# import asyncio

# async def timer(mode, output):
#     while True:
#         if not st.session_state:
#             st.stop()
#         if st.session_state[mode]["curr_time"] == 0:
#             break
#         st.session_state[mode]["curr_time"] = max(0, st.session_state[mode]["curr_time"] - 1)
#         output.subheader(format_time(mode, st.session_state))
#         await asyncio.sleep(1)


def set_time(mode, session_state):
    hr_button_key = f"{mode}_hours"
    hr_button_value = session_state[hr_button_key]
    min_button_key = f"{mode}_minutes"
    min_button_value = session_state[min_button_key]
    session_state[mode]["hours"] = hr_button_value
    session_state[mode]["minutes"] = min_button_value
    set_curr_time(mode, session_state)


def set_curr_time(mode, session_state):
    session_state[mode]["curr_time"] = session_state[mode]["hours"] * 3600 + \
                                       session_state[mode]["minutes"] * 60 + \
                                       session_state[mode]["seconds"]


def format_time(mode, session_state):
    hrs = session_state[mode]["curr_time"] // 3600
    mins = (session_state[mode]["curr_time"] - hrs * 3600) // 60
    secs = session_state[mode]["curr_time"] - hrs * 3600 - mins * 60
    return f"**{hrs:02d}:{mins:02d}:{secs:02d}**"


def reset_time(mode, session_state):
    session_state[mode]["curr_time"] = session_state[mode]["hours"] * 3600 + \
                                       session_state[mode]["minutes"] * 60 + \
                                       session_state[mode]["seconds"]
    session_state[mode]["state"] = False
    session_state[mode]["label"] = "Start"


def reset_count(session_state):
    session_state["pomodoro"]["count"] = 0
    session_state["pomodoro"]["focus_count"] = 0


def toggle_state(mode, session_state):
    session_state[mode]["state"] = not session_state[mode]["state"]
    if session_state[mode]["state"]:
        session_state[mode]["label"] = "Pause"
    else:
        session_state[mode]["label"] = "Start"


# Task List Functions #################################################################################################
def add_task(session_state):
    new_task_id = session_state["task_id"] + 0
    task_config = {
        "title": session_state[f"{new_task_id}_title"],
        "delete": False,
        "status": False,
    }
    session_state["tasks"][new_task_id] = task_config
    session_state["task_id"] += 1


def remove_task(del_task_id, session_state):
    del session_state["tasks"][del_task_id]


def toggle_tasks(session_state):
    for toggle_task_id in session_state["tasks"]:
        task_state = session_state[f"{toggle_task_id}_state"]
        if not task_state:
            session_state["tasks"][toggle_task_id]["status"] = False
        else:
            session_state["tasks"][toggle_task_id]["status"] = True
