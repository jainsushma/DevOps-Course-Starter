#!/bin/bash

# Set Python 3.8.5 as Global Python Version

if grep 3.8.5 <<< "$(python -V 2>&1)" ;then
    echo "Correct Python Version Already Installed"
else
    echo "--- Using PYENV to install Python 3.8.5 ---"
    pyenv install 3.8.5
    pyenv global 3.8.5
fi

# Install Poetry
echo "--- Installing Poetry ---"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Install Dependencies
echo "--- Installing dependencies ---"
poetry install
cp .env.template .env

# Running App
echo "--- Running the App ---"
poetry run flask run
poetry run pytest