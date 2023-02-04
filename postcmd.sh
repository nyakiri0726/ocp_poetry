#!/bin/bash

#source ~/.bashrc
#eval "$(pyenv init --path)"

pip install --upgrade pip
pip install poetry

poetry config virtualenvs.create false
poetry install --no-root