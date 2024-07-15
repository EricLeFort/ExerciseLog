# Setup the git config for this projct
git config core.hooksPath .githooks

# Perform some universal python basics
python3 -m pip install --upgrade pip
pip3 install virtualenv isort

# Setup a virtual environment for this project
VENV_NAME=pyenv
virtualenv ${VENV_NAME}
source ${VENV_NAME}/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
deactivate

# Node.js setup
curl -fsSL https://fnm.vercel.app/install | bash
fnm use --install-if-missing 20

# Install relevant node packages
npm install -g npm
npm install -g typescript
npm install --save @types/d3
npm install --save @types/jquery