#!/bin/bash

# check if pygame is installed
if ! python3 -c "import pygame" &> /dev/null; then
    # Install Pygame
    pip3 install -r requirements.txt
fi

# set the environment variable to hide the support prompt
export PYGAME_HIDE_SUPPORT_PROMPT="hide"

echo -e "Choose one agent to play:\n1. Minimax agent\n2. Q-learning agent"
read -p "> " choice
if [ "$choice" -eq 1 ]; then
    python3 play_against_minimax.py
elif [ "$choice" -eq 2 ]; then
    python3 play_against_qlearning.py
else
    echo "Invalid choice."
fi
