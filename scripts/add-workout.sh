#!/bin/bash
set -e

DATE_FORMAT=[0-9]{2}-[A-Z]{3}-[0-9]{4}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
VENV_NAME=pyenv

# Read in args
dryrun=false
amendCommit=false
date=false

for arg in "$@"
do
    case "$arg" in
    "-d"|"--dryrun")
        dryrun=true
        ;;
    "-a"|"--amend")
        amendCommit=true
        ;;
    *)
        if [[ ${arg} =~ \-\-.* ]]
        then
            echo "Invalid flag ${1}. Allowed arguments are (-d|--dryrun; -a|--amend)"
            exit 1
        elif [[ ${arg} =~ ${DATE_FORMAT} ]]
        then
            date=${arg}
        else
            echo "A date should be passed in as the first argument in the form DD-MMM-YYYY e.g. 01-JAN-2023"
            exit 1
        fi
        ;;
    esac
    shift
done

if [ ${dryrun} = true ] && [ ${amendCommit} = true ]
then
    echo "Cannot set both dryrun and amend"
    exit 1
fi

# Update visuals
echo "Activating python environment.."
source ${VENV_NAME}/bin/activate
cd "${SCRIPT_DIR}/../python/src"
export PYTHONPATH=$(pwd)
python3 "exercise_log/run_updater.py"
deactivate

# Add the new commit
if [ ${dryrun} = false ]
then
    cd ../..
    git add data img
    if [ ${amendCommit} = true ]
    then
        git commit --amend --no-edit
    else
        git commit -m "Added workouts up to $date"
    fi
fi
