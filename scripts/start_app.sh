#!/bin/bash
# Start the Streamlit application
screen -dmS streamlit_app bash -c 'cd /home/ubuntu/whchat; streamlit run app.py --server.port 8501'