pip uninstall mcmd
rm -rf build dist *egg* __pycache__
python setup.py sdist bdist_wheel
pip install -e .