# Team 20 - Techwise Capstone Project

## Focus Frame
Focus frame is a web app composed of various study techniques and methods to help students study more efficiently and 
effectively. We plan to incorporate eye-tracking technology based off of computer vision techniques in order to extend 
those features further. 

The web app is composed of a home page, a flashcard page, and a pomodoro timer page.
The home page is a landing page that gives a brief description of the web app and the various study techniques and 
methods. The flashcard page is a page where users can create flashcards and study them. The pomodoro timer page is 
where users can set a timer for 25 minutes and upload a pdf file to read for that time.

This project was created as part of the Google sponsored TalentSprint TechWise program and serves demonstrates the 
culmination of the skills and technologies learned throughout the program.

## Team Members
- [Johnathan Franco Sosa]()
- [Zak Buffington]()
- [Javier Perez]()

## Deployment 
https://focusframe.streamlit.app

## Environment Setup
Clone the repo and cd into the repo folder
```bash
git clone https://github.com/jfrancososa/Project3_Team20.git
cd Project3_Team20
```
Once in the Repo folder, create a virtual environment and activate it
#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
#### Bash 
```bash
python -m venv venv
source venv/Scripts/activate
```
Then install the requirements
```bash
pip install -r requirements.txt
```

When you are done working, deactivate the virtual environment
```bash
deactivate
```

* Note: I ran into an issue with PyCharm where it would set the python interpreter to the venv and the bash terminal would not have the (venv) prefix but still be active. So when you activate the venv, the bash terminal will lose all of its commands, and you'll have to restart it but not activate the venv since it's apparently automatically activated.

## Running Web App for Development
While in the main repo folder and with the virtual environment activated and all requirements installed:
```bash
streamlit run some-page.py  # ex: streamlit run Home.py
```
This will open a browser window with the web app running. If you want changes in the code to automatically
update the web app, you need to activate the setting in the web apps top right settings menu.

* Note: In order for the page to automatically re-run when the source code is saved, it must be ran using the above
command. For example, if I want to work on the Read Radar page and have it automatically update, I would use:
streamlit run pages/Read_Radar.py


* Note: To close the web app, you first need to press ctrl+c in the terminal where the streamlit command was entered 
before closing the browser tab. If you close the tab first and then try to stop the process in the terminal, it will
not stop, but you can re-open the browser tab then stop the process in the terminal.
