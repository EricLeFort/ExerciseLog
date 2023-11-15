#!/bin/bash
set -e

VENV_NAME=pyenv
THIS_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Move to the src directory and start the test
source ${VENV_NAME}/bin/activate
cd "${THIS_SCRIPT_DIR}/../python/src"
coverage run \
  --source . \
  --branch \
  -m unittest -v
coverage report --show-missing
deactivate