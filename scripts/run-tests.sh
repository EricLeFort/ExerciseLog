#!/bin/bash
set -e

VENV_NAME=pyenv
THIS_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Run linters/formatters
source ${VENV_NAME}/bin/activate
isort --check --diff python/
black --check --diff --color python/
# TODO pylint
# TODO flake8

# Move to the test directory and start the test
cd "${THIS_SCRIPT_DIR}/../python/src"
export PYTHONPATH=$(pwd)
cd ../test
python3 -m unittest -v
deactivate
