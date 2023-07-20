# Project3_Team20

## Environment Setup
### Bash Terminal
Clone the repo and cd into the repo folder
```bash
git clone https://github.com/jfrancososa/Project3_Team20.git
cd Project3_Team20
```
Once in the Repo folder, create a virtual environment and activate it
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

* Note: If working on a page that is not the main page (Home.py), saving the page will not automatically update the web app. You either need to update the main page itself and save the changes, or run the page itself with the above command.


* Note: To close the web app, you need to press ctrl+c in the bash terminal with the tab in the browser still open, otherwise the web app will not close. If you close the tab first you can just reopen it and then close it in the terminal.