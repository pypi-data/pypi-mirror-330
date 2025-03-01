
# How to upload a package to PyPi

# Install the required packages
pip install setuptools wheel twine

# Build the package
python setup.py sdist bdist_wheel

# Upload the package
twine upload dist/*
