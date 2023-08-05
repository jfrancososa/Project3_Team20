import streamlit as st
import random

st.set_page_config(page_title="Flashcard Application", page_icon=":memo:", layout="wide")

def reset_flashcards():
    st.session_state['flashcards'] = []
    st.session_state['index'] = 0
    st.session_state['show_answer'] = False

if 'flashcards' not in st.session_state:
    reset_flashcards()

if 'index' not in st.session_state:
    st.session_state['index'] = 0

if 'show_answer' not in st.session_state:
    st.session_state['show_answer'] = False

if 'hint' not in st.session_state:
    st.session_state['hint'] = 'Here is a hint!'

st.title("Flashcard Application")

st.sidebar.header("Controls")

if st.sidebar.checkbox('Start from scratch'):
    if st.sidebar.button("Confirm Reset"):
        reset_flashcards()

def add_flashcard():
    st.sidebar.subheader("Add a new flashcard")
    question = st.sidebar.text_input('Question')
    answer = st.sidebar.text_input('Answer')
    difficulty = st.sidebar.select_slider('Difficulty', options=list(range(1, 11)))
    hint = st.sidebar.text_input('Hint', value='')
    if st.sidebar.button('Add flashcard'):
        if question and answer: # checking if question and answer fields are not empty
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

# If there are no flashcards, prompt the user to create one
if not st.session_state['flashcards']:
    st.write("There are currently no flashcards. Please add a new flashcard from the side bar.")
else:
    current_flashcard = st.session_state['flashcards'][st.session_state['index']]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h3 style='color: white;'>Flashcard: {current_flashcard['number']} / {len(st.session_state['flashcards'])}</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h3 style='color: white;'>Difficulty: {current_flashcard['difficulty']}</h3>", unsafe_allow_html=True)

    if st.button('Flip'):
        st.session_state['show_answer'] = not st.session_state['show_answer']   

    if st.session_state['show_answer']:
        st.markdown(f"<div style='text-align: center; border:2px solid black; padding: 20px; background-color: white;'><h1 style='color: black;'>Answer: {current_flashcard['answer']}</h1></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: center; border:2px solid black; padding: 20px; background-color: white;'><h1 style='color: black;'>Question: {current_flashcard['question']}</h1></div>", unsafe_allow_html=True)


    show_hint = st.checkbox('Show Hint')
    if show_hint:
        st.write(f"Hint: {current_flashcard['hint']}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('Next Flashcard'):
            if st.session_state['index'] < len(st.session_state['flashcards']) - 1:
                st.session_state['index'] += 1
            else:
                st.session_state['index'] = 0
            st.experimental_rerun()

    with col2:
        if st.button('Previous Flashcard'):
            if st.session_state['index'] > 0:
                st.session_state['index'] -= 1
            else:
                st.session_state['index'] = len(st.session_state['flashcards']) - 1
            st.experimental_rerun()

    with col3:
        if st.button('Flag Flashcard'):
            current_flashcard['flagged'] = not current_flashcard['flagged']
            status = 'Flagged' if current_flashcard['flagged'] else 'Unflagged'
            st.write(f"Flashcard {current_flashcard['number']} is now {status}!")
    
    st.write("Stats:")
    total_attempts = current_flashcard['right_mark'] + current_flashcard['wrong_mark']
    if total_attempts > 0:
        st.write(f"Right marks: {current_flashcard['right_mark']} ({(current_flashcard['right_mark'] / total_attempts) * 100}%)")
        st.write(f"Wrong marks: {current_flashcard['wrong_mark']} ({(current_flashcard['wrong_mark'] / total_attempts) * 100}%)")
    else:
        st.write("No marks yet.")
    
    if st.button('Mark as Right'):
        current_flashcard['right_mark'] += 1
        st.experimental_rerun()

    if st.button('Mark as Wrong'):
        current_flashcard['wrong_mark'] += 1
        st.experimental_rerun()

    sort_preference = st.selectbox('Sort by:', ['Number Ascending', 'Number Descending', 'Difficulty Ascending', 'Difficulty Descending', 'Flagged'], key='sort')
    if sort_preference == 'Number Ascending':
        st.session_state['flashcards'].sort(key=lambda x: x['number'])
    elif sort_preference == 'Number Descending':
        st.session_state['flashcards'].sort(key=lambda x: x['number'], reverse=True)
    elif sort_preference == 'Difficulty Ascending':
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
