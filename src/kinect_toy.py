#! /usr/bin/env python
"""
 kinect_toy.py
 Entry point for the kinect_toy. Serves as controller.
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""

import sys
import cv
import ktkinect as ktk
import ktmodel as ktm
import ktview as ktv

WINDOW_NAME = "JHUACM Kinect Demo"
debug = False

def parseArgs(args):
	global debug
	for string in args:
		if string == "--debug":
			debug = True

def main(args):
	parseArgs(args)
	kinect = ktk.Kinect()
	image, depth = kinect.getSensorData()
	frame = ktm.Frame(image, depth)
	view = ktv.CVKTView(WINDOW_NAME, frame)
	view.setVisible(True)
	while True:
		image, depth = kinect.getSensorData()
		frame.update(image, depth)
		char = cv.WaitKey(10)
		if char == 27:
			break
		elif char == -1:
			pass
		else:
			print char

if __name__ == "__main__":
	main(sys.argv[:])
	
