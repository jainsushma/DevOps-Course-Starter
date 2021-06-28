#!/bin/bash

# Set Python 3.8.5 as Global Python Version

if grep 3.8.5 <<< "$(python -V 2>&1)" ;then
    echo "Correct Python Version Already Installed"
else
    echo "--- Using brew to install Python 3.8.5 ---"
    git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow
    brew install python-tk@3.8.5
fi

# Install Poetry
echo "--- Installing Poetry ---"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Install Dependencies
echo "--- Installing dependencies ---"
poetry install

# Create a .env file from the .env.template
cp -n .env.template .env

# Running App
echo "--- Running the App ---"
poetry run flask run
