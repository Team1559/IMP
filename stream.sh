#!/bin/bash

gst-launch-1.0 nvcamerasrc sensor_id = 0 ! video/x-raw, format=I420, width=640, height=480, framerate=30/1 ! jpegdec ! rtpjpegpay ! udpsink host = 10.15.59.70 port = 5000
