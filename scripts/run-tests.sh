#!/bin/bash
set -e

VENV_NAME=pyenv
THIS_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Move to the test directory and start testing
echo "Activating python environment.."
source ${VENV_NAME}/bin/activate
cd "${THIS_SCRIPT_DIR}/../python/src"
export PYTHONPATH=$(pwd)

# Run linters/formatters
cd ../..
echo "Running linters and formatters.."
isort --check --diff python/
black --check --diff --color python/
flake8 python/
pylint python/

# Run the unit tests
echo "Running unit tests.."
cd python/test
python3 -m unittest -v
deactivate
