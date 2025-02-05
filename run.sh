#!/bin/bash
set -eou pipefail

# clear python cache
rm -rf **/__pycache__

# check if pygame is installed
if ! python3 -c "import pygame" &> /dev/null; then
    # Install Pygame
    pip3 install -r requirements.txt
fi

# set the environment variable to hide the support prompt
export PYGAME_HIDE_SUPPORT_PROMPT="hide"

# Run the game
python3 play_against_qlearning.py
