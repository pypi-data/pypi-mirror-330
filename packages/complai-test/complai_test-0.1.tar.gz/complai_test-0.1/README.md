Steps to setup environments to run code
=======================================

It is suggeseted to maintain 2 different environments to run the code,one for the scan component and the other to run the application.

The below steps are for setting up the environment using Anaconda. Please refer to the below link for more details:

https://docs.anaconda.com/anaconda/install/index.html


Steps to Run the code
=====================
1. Ensure you are in the complai directory

Optional Steps to RUN/RERUN SCAN
=================================
0. Create and switch to new Anaconda Environment:
"conda create -n <NEW SCAN ENVIRONMENT NAME> python=3.8"
"conda activate <NEW SCAN ENVIRONMENT NAME>"

1. Install complai_scan using pip, using below code.
"pip install <PATH TO INSTALLABLE>/complai_scan-0.1.0.tar.gz"

2. To run the scan , move to the respective directory.
For e.g. : "cd titanic"

3. Run the code using the below command.
"python run_binary.py"

Steps to LAUNCH APP
===================
0. Create and switch to new Anaconda Environment:
"conda create -n <NEW APP ENVIRONMENT NAME> python=3.8"
"conda activate <NEW APP ENVIRONMENT NAME>"

1. Move to the complai_ui directory using the below command.
"cd compali_ui"
2. Install app dependencies (Preferably in a new env), using the below command
"pip install -r requirements.txt"
3. Run the below command to launch the stramlit app.
"streamlit run app.py"

Note: If you are on Dark Theme then please go to settings of the streamlit app and select Theme as Light. Changing Theme is very easy as explained in this link
https://blog.streamlit.io/content/images/2021/08/Theming-1--No-Padding---1-.gif

Steps to Configure YAML
=======================

1. This project requires the user to configure 2 yaml files. 
For e.g. :"tiatnic_config.yaml" and "tiatnic_policy.yaml"

 Please refer to the yaml files for further information