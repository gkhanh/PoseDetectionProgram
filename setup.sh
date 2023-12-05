#!/bin/sh

# Install the correct Python version
brew install pyenv
pyenv install --skip-existing 3.11

pyenv global 3.11
pyenv local 3.11
python --version

# Install virtual environment
pip install virtualenv
virtualenv ./.venv
python --version
source ./.venv/bin/activate

python --version

pip install -r requirements.txt