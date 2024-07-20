#!/bin/bash

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
if ! command -v node &> /dev/null; then
    curl -fsSL https://fnm.vercel.app/install | bash
    fnm use --install-if-missing 20
else
    echo "Node already installed."
fi

# Open source is great but goddamn this output adds so much damn clutter
npm config set fund false

# Install relevant node packages
declare -a NODE_PACKAGES=(
    "npm"
    "typescript"
    "eslint@8.56.x"
    "typescript-eslint"
    "@eslint/js"
    "@types/d3"
    "@types/jquery"
    "@types/eslint__js"
)
npm install "${NODE_PACKAGES[@]}"
