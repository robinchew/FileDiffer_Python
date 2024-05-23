#!/bin/bash

#Check if the activate script exists
if [ -f "./.venv/bin/activate" ]; then
    source "./.venv/bin/activate"
else
    echo "Virtual environment does not exist. Creating virtual environment"
    python3 -m venv .venv
    source "./.venv/bin/activate"
fi

echo "Checking dependancies"
pip install -r requirements.txt -q

echo "Running server. Access with http://localhost:8080"
rebar3 compile
rebar3 shell