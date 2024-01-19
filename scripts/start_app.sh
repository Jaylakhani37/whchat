#!/bin/bash
# This script is used to start the application.
cd /home/ubuntu/whchat
pm2 restart streamlit_app || pm2 start "streamlit run app.py --server.port 8501" --name streamlit_app
