#!/bin/bash
set -e

VENV_NAME=pyenv
PYTHON_DIR=python
THIS_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Move to the test directory and start testing
echo "Activating python environment.."
source ${VENV_NAME}/bin/activate
cd "${THIS_SCRIPT_DIR}/../${PYTHON_DIR}/src"
export PYTHONPATH=$(pwd)

# Run linters/formatters
cd ../..
echo "Running linters and formatters.."
ruff check --show-fixes ${PYTHON_DIR}
ruff format --check --diff ${PYTHON_DIR}

# Run the unit tests
echo "Running unit tests.."
cd ${PYTHON_DIR}/test
python3 -m unittest -v
deactivate
