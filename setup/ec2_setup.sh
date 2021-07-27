#!/bin/bash

# install python
#sudo yum update -y
#sudo yum install python3 -y

# create venv and activate
#python3 -m venv python_env
#source python_env/bin/activate

# install python libs
pip install --upgrade pip
pip install moviepy
pip install regex
pip install streamlit
pip install nltk
pip install --no-cache-dir tensorflow
pip install tensorflow-hub
pip install --no-cache-dir torch
pip install punctuator
pip install gingerit
pip install keybert	