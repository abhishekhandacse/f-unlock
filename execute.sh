#!/bin/bash
cd test-data
fswebcam -r 640x480 --jpeg 85 -D 1 web-cam-shot.jpg
cd ..
python OpenCV-Face-Recognition-Python.py

