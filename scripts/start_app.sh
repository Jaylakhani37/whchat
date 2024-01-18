#!/bin/bash
# Start the Streamlit application
cd /home/ubuntu/whchat
screen -dmS streamlit_app bash -c 'streamlit run app.py --server.port 8501'
