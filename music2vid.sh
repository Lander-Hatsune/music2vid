#! /bin/bash

source venv/bin/activate
export FFMPEG_BINARY=$(where ffmpeg)
python convert.py input/
