# Setup the git config for this projct
git config core.hooksPath .githooks

# Perform some universal python basics
python3 -m pip install --upgrade pip
pip3 install virtualenv

# Setup a virtual environment for this project
VENV_NAME=pyenv
virtualenv ${VENV_NAME}
source ${VENV_NAME}/bin/activate
python3 -m pip install -r requirements.txt
deactivate