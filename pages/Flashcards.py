import streamlit as st
import random

st.set_page_config(page_title="Flashcard Application", page_icon=":memo:", layout="wide")

# Function to reset the flashcards
def reset_flashcards():
    st.session_state['flashcards'] = []
    st.session_state['index'] = 0
    st.session_state['show_answer'] = False

# Check if the flashcards variable exists in the session state
if 'flashcards' not in st.session_state:
    reset_flashcards()

# Check if the current flashcard index exists in the session state
if 'index' not in st.session_state:
    st.session_state['index'] = 0

# Check if the answer visibility flag exists in the session state
if 'show_answer' not in st.session_state:
    st.session_state['show_answer'] = False

# Check if hint is in the session state
if 'hint' not in st.session_state:
    st.session_state['hint'] = 'Here is a hint!'

st.title("Flashcard Application")

st.sidebar.header("Controls")

# Checkbox to decide whether to reset the flashcards
if st.sidebar.checkbox('Start from scratch'):
    if st.sidebar.button("Confirm Reset"):
        reset_flashcards()

# Function to add a flashcard
def add_flashcard():
    st.sidebar.subheader("Add a new flashcard")
    question = st.sidebar.text_input('Question')
    answer = st.sidebar.text_input('Answer')
    difficulty = st.sidebar.select_slider('Difficulty', options=list(range(1, 11)))  # difficulty rating
    if st.sidebar.button('Add flashcard'):
        st.session_state['flashcards'].append({
            'question': question,
            'answer': answer,
            'number': len(st.session_state['flashcards']) + 1,
            'difficulty': difficulty
        })

add_flashcard()

# If there are flashcards, display the current one
if st.session_state['flashcards']:
    if not st.session_state['show_answer']:
        st.markdown(f"<h2 style='text-align: center; color: purple;'>Question #{st.session_state['flashcards'][st.session_state['index']]['number']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; border:2px solid black; padding: 20px; background-color: #e6e6e6;'><h1 style='color: black;'>{st.session_state['flashcards'][st.session_state['index']]['question']}</h1></div>", unsafe_allow_html=True)
        st.write('Difficulty: ', st.session_state['flashcards'][st.session_state['index']]['difficulty'])
        if st.button('Flip Card'):
            st.session_state['show_answer'] = True
    else:
        st.markdown(f"<h2 style='text-align: center; color: purple;'>Answer #{st.session_state['flashcards'][st.session_state['index']]['number']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; border:2px solid black; padding: 20px; background-color: #e6e6e6;'><h1 style='color: black;'>{st.session_state['flashcards'][st.session_state['index']]['answer']}</h1></div>", unsafe_allow_html=True)
        st.write('Difficulty: ', st.session_state['flashcards'][st.session_state['index']]['difficulty'])
        if st.button('Flip Card'):
            st.session_state['show_answer'] = False

    st.write('Flashcard: ', st.session_state['index'] + 1, '/', len(st.session_state['flashcards']))

    if st.button('Next Flashcard'):
        st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['flashcards'])
        st.session_state['show_answer'] = False

    def navigate_flashcards():
        sorted_flashcards = sorted(st.session_state['flashcards'], key=lambda x: x['difficulty'], reverse=True)
        difficulties = [f"Flashcard {i+1} - Difficulty {card['difficulty']}" for i, card in enumerate(sorted_flashcards)]
        selection = st.selectbox('Navigate Flashcards', difficulties)
        st.session_state['index'] = difficulties.index(selection)
    navigate_flashcards()

    def randomize_flashcards():
        if st.button('Randomize flashcards'):
            random.shuffle(st.session_state['flashcards'])
            st.session_state['index'] = 0
    randomize_flashcards()

    with st.sidebar.expander("More options"):
        def delete_flashcard():
            if st.button('Delete current flashcard'):
                del st.session_state['flashcards'][st.session_state['index']]
                st.session_state['index'] = 0
        delete_flashcard()

if st.checkbox('Show Hint'):
    hint = st.text_input('Hint', value=st.session_state['hint'])
    st.session_state['hint'] = hint
