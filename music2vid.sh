#! /bin/zsh

source venv/bin/activate
export FFMPEG_BINARY=/usr/bin/ffmpeg
python convert.py input/
