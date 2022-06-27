#!/bin/bash

echo "I hope you don't forgot to use pyenv for install python 3.10"
python3 -m virtualenv --python="$1" .venv
source .venv/bin/activate

printf "\nInstalling pre-commit...\n"
pip install -U pre-commit
pre-commit install

printf "\nConfig poetry...\n"
poetry config virtualenvs.create false
printf "Poetry configured\n"

if [ -e ".env" ]; then
  echo "\".env\" already exists, skips creating"
else
  cat .env.local >>.env && echo "\".env\" created from \".env.local\""
fi

printf "\nInstalling dependencies...\n"
cd system/python && poetry update
cd ../..
