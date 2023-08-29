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

#home page eye tracker container
async def frame_analysis(container):
    while True:
        if not st.session_state:
            st.stop()
        if not st.session_state.eye_tracker.capture.isOpened():
            st.stop()
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

#page description
with st.expander("Overview", expanded=True):
    st.write("This page offers a structured environment for creating and studying flashcards using the Leitner System. You can create flashcards on various subjects, categorize them via difficulty, and then engage in study sessions to test your memory and understanding. The homepage offers easy navigation , and offers blinking statistics to track your progress.")
with st.expander("Leitner System", expanded=False):
    st.markdown("Derived from the principles outlined by German scientist Sebastian Leitner in the 1970s, the Leitner System is an efficient method for studying flashcards. The system involves a set of compartments that help categorize flashcards based on how well you know the material. The system ensures that you review cards you find challenging more frequently, allowing for efficient and effective study sessions.")
    st.markdown("""
    The methodology has four essential steps:

    1. Create flashcards and organize into difficulty
    2. Initial review
    3. Answer and sort
    4. Track progress
     """)
st.divider()

#sidebar init
def reset_flashcards():
    st.session_state['flashcards'] = []
    st.session_state['index'] = 0
    st.session_state['show_answer'] = False

st.sidebar.header("Controls")
if st.sidebar.checkbox('Start from scratch'):
    if st.sidebar.button("Confirm Reset"):
        reset_flashcards()
if 'flashcards' not in st.session_state:
    reset_flashcards()
    st.session_state['flashcards'] = []
if 'index' not in st.session_state:
    st.session_state['index'] = 0
if 'show_answer' not in st.session_state:
    st.session_state['show_answer'] = False
if 'hint' not in st.session_state:
    st.session_state['hint'] = 'Here is a hint!'

#sidebar options initally 
def add_flashcard():
    st.sidebar.subheader("Add a new flashcard")
    question = st.sidebar.text_input('*Question')
    answer = st.sidebar.text_input('*Answer')
    difficulty = st.sidebar.select_slider('Difficulty', options=list(range(1, 11)))
    hint = st.sidebar.text_input('Hint', value='')
    if st.sidebar.button('Add flashcard'):
        if question and answer: 
            st.session_state['flashcards'].append({
                'question': question,
                'answer': answer,
                'number': len(st.session_state['flashcards']) + 1,
                'difficulty': difficulty,
                'right_mark': 0,    
                'wrong_mark': 0,
                'hint': hint,
                'flagged': False,
            })
            st.sidebar.success("Flashcard added successfully!")
            st.experimental_rerun()
add_flashcard()

if st.session_state['flashcards']:
    def delete_flashcard():
        st.sidebar.subheader("Delete a flashcard")
        flashcard_number = st.sidebar.number_input("Enter the flashcard number to delete", min_value=1, max_value=len(st.session_state['flashcards']), step=1)
        if st.sidebar.button('Delete flashcard'):
            del st.session_state['flashcards'][flashcard_number-1]
            st.session_state['index'] = 0
            st.sidebar.success("Flashcard deleted successfully!")
            st.experimental_rerun()
    delete_flashcard()

def edit_flashcard():
    st.sidebar.subheader("Edit an existing flashcard")
    flashcard_options = [f"Flashcard {card['number']} - Difficulty {card['difficulty']}" for card in st.session_state['flashcards']]
    edit_flashcard_selection = st.sidebar.selectbox("Select a flashcard to edit", flashcard_options)
    edit_index = flashcard_options.index(edit_flashcard_selection)
    selected_flashcard = st.session_state['flashcards'][edit_index]
    # Text input for editing question, answer, and difficulty
    new_question = st.sidebar.text_input("Edit Question", value=selected_flashcard['question'])
    new_answer = st.sidebar.text_input("Edit Answer", value=selected_flashcard['answer'])
    new_difficulty = st.sidebar.select_slider("Edit Difficulty", options=list(range(1, 11)), value=selected_flashcard['difficulty'])
    new_hint = st.sidebar.text_input("Edit Hint", value=selected_flashcard['hint'])
    
    if st.sidebar.button('Update flashcard'):
        # Update flashcard information
        selected_flashcard['question'] = new_question
        selected_flashcard['answer'] = new_answer
        selected_flashcard['difficulty'] = new_difficulty
        selected_flashcard['hint'] = new_hint
        st.sidebar.success("Flashcard updated successfully!")
        st.experimental_rerun()

if st.session_state['flashcards']:
    edit_flashcard()
# If there are no flashcards, prompt the user to create one
if not st.session_state['flashcards']:
    st.write("There are currently no flashcards. Please add a new flashcard from the side bar.")
else:
    current_flashcard = st.session_state['flashcards'][st.session_state['index']]
#header
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<h3 style='color: black;'>Flashcard: {current_flashcard['number']} / {len(st.session_state['flashcards'])}</h3>", unsafe_allow_html=True)
    with col2:
        flagged_flashcards_count = len([card for card in st.session_state['flashcards'] if card['flagged']])
    # Display the count using Streamlit markdown
        st.markdown(f"<h3 style='color: black;'>Flagged: {flagged_flashcards_count}</h3>", unsafe_allow_html=True)
    with col3:
        total_attempts = current_flashcard['right_mark'] + current_flashcard['wrong_mark']
        if total_attempts > 0:
            st.markdown(f"<h3 style='color: black;'>Score: {current_flashcard['right_mark']} / {total_attempts}</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='color: black;'>No marks yet.", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<h3 style='color: black;'>Difficulty: {current_flashcard['difficulty']}/10</h3>", unsafe_allow_html=True)
#buttons
    if st.button('Flip'):
        st.session_state['show_answer'] = not st.session_state['show_answer']   
    if st.session_state['show_answer']:
        st.markdown(f"<div style='text-align: center; border:2px solid black; padding: 20px; background-color: white;'><h1 style='color: black;'>Answer: {current_flashcard['answer']}</h1></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: center; border:2px solid black; padding: 20px; background-color: white;'><h1 style='color: black;'>Question: {current_flashcard['question']}</h1></div>", unsafe_allow_html=True)


    show_hint = st.checkbox('Show Hint')
    if show_hint:
        st.write(f"Hint: {current_flashcard['hint']}")
#buttons
    col1, col2, empty, col3, col4, empty_space, col5, col6 = st.columns(8)
    with col1:
        if st.button('Last Flashcard'):
            if st.session_state['index'] > 0:
                st.session_state['index'] -= 1
            else:
                st.session_state['index'] = len(st.session_state['flashcards']) - 1
            st.experimental_rerun()
    with col2:
        if st.button('Mark as Wrong'):
            current_flashcard['wrong_mark'] += 1
            st.experimental_rerun()
    with empty:
        st.markdown("")
    with col3:
        if st.button('Flag Flashcard'):
            current_flashcard['flagged'] = not current_flashcard['flagged']
            status = 'Flagged' if current_flashcard['flagged'] else 'Unflagged'
            st.write(f"Flashcard {current_flashcard['number']} is now {status}!")
            st.experimental_rerun()
    with col4:
        if st.button('Reset Score'):
            current_flashcard['right_mark'] = 0
            current_flashcard['wrong_mark'] = 0
            st.experimental_rerun()
    with empty_space:
        st.markdown("")
    with col5:
        if st.button('Mark as Right'):
            current_flashcard['right_mark'] += 1
            st.experimental_rerun()
    with col6:
        if st.button('Next Flashcard'):
            if st.session_state['index'] < len(st.session_state['flashcards']) - 1:
                st.session_state['index'] += 1
            else:
                st.session_state['index'] = 0
            st.experimental_rerun()
    sort_preference = st.selectbox('Sort by:', ['Difficulty Ascending', 'Difficulty Descending', 'Flagged'], key='sort')
    if sort_preference == 'Difficulty Ascending':
        st.session_state['flashcards'].sort(key=lambda x: x['difficulty'])
    elif sort_preference == 'Difficulty Descending':
        st.session_state['flashcards'].sort(key=lambda x: x['difficulty'], reverse=True)
    elif sort_preference == 'Flagged':
        st.session_state['flashcards'].sort(key=lambda x: x['flagged'], reverse=True)

    flashcard_options = [f"Flashcard {card['number']} - Difficulty {card['difficulty']}" for card in st.session_state['flashcards']]
    flashcard_selection = st.selectbox('Navigate Flashcards by Number or Difficulty', flashcard_options, index=st.session_state['index'])
    if st.button('Confirm Selection'):
        st.session_state['index'] = flashcard_options.index(flashcard_selection)
        st.write(f"You selected: {flashcard_selection}")
        st.experimental_rerun()

    st.divider()  # Add a visual separator for better readability


# st.write(st.session_state)
    if st.session_state.display_feed:
        asyncio.run(frame_analysis(camera_container))
