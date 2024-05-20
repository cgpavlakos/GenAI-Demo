#!/bin/bash

# Allow traffic on port 8502 (replace with your desired port if needed)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8502 -j ACCEPT

# Activate virtual environment and navigate to app directory
cd ~/src/llama/llamaenv/bin
source activate
cd ~/src/GenAI-Demo-main

# Run the application in the background
nohup streamlit run streamlit_app_oci.py &

echo "Application started in the background."
