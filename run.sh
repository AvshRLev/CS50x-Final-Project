#! /bin/bash

pip3 install -r requirements.txt
cp application.py app.py
apt install -y python3-flask
flask run 
