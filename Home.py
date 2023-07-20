import streamlit as st

# Set page title
APP_NAME = "App Name"
st.title(APP_NAME, anchor="center")

st.divider()
# Add page description and key features
st.header(f"What is {APP_NAME}?")

app_description = f"""
    {APP_NAME} is a productivity focused web app that combines various studying techniques and tools 
    to keep you focused and on task.
    \n
    We offer a eye tracking tool based on computer vision techniques to track your eye movements and alert you when you 
    stray away from your material."""
st.write(app_description)
st.subheader("Our Main Features")
st.markdown("""
- [**Focused Reading:**](/Timed_Read "redirects to new tab") Open study material within the app and set a pomodoro timer
to keep you on task and focused using the popular Pomodoro Technique. 
- **Feature 2:** Feature 2 description
- **Feature 3:** Feature 3 description
""")
