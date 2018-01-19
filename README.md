################################################################################################################################
# Name: 	      SolarSIM
#
# Description:    A simple simulation of the Earth orbiting the Sun. It should help to understand the Milankovitch cycles.
#
# Version: 	      1.0.0
#
# Author: 	      Stefan Mario Fuchs
# Email:	   	  stefan.mario.fuchs@web.de
#
# Python version: 2.7
# Requirements:   Anaconda, pip, matplotlib=1.4.3, numpy, pil, wxpython, mwcraig vpython
#
# You can download the program from this location: https://github.com/FuchsS/SolarSIM
################################################################################################################################
#
# PREREQUISITES:
#
# First, we create a virtual environment to make any changes there:
#
#    conda create -n solarSIM python=2.7
#
# Now we activate the virtual environment to install the packages there:
#
# • Windows:
#    activate solarSIM
#
# • macOS and Linux:
#    source activate solarSIM
#
# Now we install all missing packages:
#
#    conda install wxpython
#    conda install -c mwcraig vpython
#    conda install matplotlib=1.4.3
#    pip install numpy --upgrade
#    conda install pil
#
#
#
# STARTING THE SIMULATION:
#
# If the virtual environment is not already activated, activate it with the following commands:
#
# • Windows:
#    activate solarSIM
#
# • macOS and Linux:
#    source activate solarSIM
#
# In order to run the simulation, switch to the app directory and execute 'python app.py':
#
#    cd app
#    python app.py