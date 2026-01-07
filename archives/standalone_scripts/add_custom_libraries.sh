#!/bin/bash


###################################################
# ADD CUSTOM MODULES TO VENV site-packages FOLDER #
###################################################

#1. Go to virtual environment site-packages folder:

cd ~/github/pizza_project/venv/lib/python3.13/site-packages

#2. Add custom modules as links: 

ln -s ~/github/batterypy/ batterypy

ln -s ~/github/dimsumpy/ dimsumpy

