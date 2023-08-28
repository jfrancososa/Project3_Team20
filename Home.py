import streamlit as st

# Set page title
APP_NAME = "Focus Frame"
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

# Feature page names will be in the pages directory
# Function below is for getting those names dynamically and automatically updating the list
def get_page_names():
    import os
    names = []
    for file in os.listdir("pages"):
        if file.endswith(".py"):
            names.append((file.split(".")[0]))
    return names
names = get_page_names()

# Set page descriptions below, the links will be automatically generated
# Format: features = {
#           "Feature_Name": {
#               "description": "Feature description",
#               "link": "(/Feature_Name, "redirects to new tab")",
#               "name": ' '.join([word.capitalize() for word in "Feature Name".split("_")])
#           },
#           "Feature_Name_2": {
#               "description": "Feature description",
#               "link": "(/Feature_Name_2, "redirects to new tab")",
#               "name": ' '.join([word.capitalize() for word in "Feature Name 2".split("_")])
#           },
#           ...
#       }
features = {name: {"description": "",
                   "link": f"(/{name} 'Opens {name} page in a new tab')",
                   "name": ' '.join([word.capitalize() for word in name.split("_")])
                   } for name in names if name != "Eye_Tracker"
            }

features["Flashcards"]["description"] = "Create flashcards and study them using the Leitner System."
features["Read_Radar"]["description"] = "Focus on reading by setting a timer using the Pomodoro Technique."

feature_list = '\n'.join(
    [f"- [{features[feature]['name']}]{features[feature]['link']} : {features[feature]['description']}"
     for feature in features
     ])
st.markdown(feature_list)


st.subheader("Learn More")
st.write("We design our feature pages around the following study techniques:")
st.markdown("- [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)")
st.markdown("- [Leitner System](https://en.wikipedia.org/wiki/Leitner_system)")
st.markdown("- [Feynman Technique](https://en.wikipedia.org/wiki/Feynman_technique)")
st.markdown("- [Pareto Principle](https://en.wikipedia.org/wiki/Pareto_principle)")
st.markdown("- [SQ3R](https://en.wikipedia.org/wiki/SQ3R)")
st.markdown("- [PQRST](https://en.wikipedia.org/wiki/Study_skills#Reading_and_listening)")
