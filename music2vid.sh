#! /bin/bash

source venv/bin/activate
export FFMPEG_BINARY=$(which ffmpeg)
python3 convert.py input/
