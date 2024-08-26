#!/bin/bash

# -------------------------------------------------------------------------------------------
# This script help to run in the editable mode where you can develop and test at the run time
# -------------------------------------------------------------------------------------------
pip uninstall mcmd
rm -rf build dist *egg* __pycache__
python setup.py sdist bdist_wheel
pip install -e .