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
quitChars = ('q', chr(27))
debugChars = ('d')
quitInts = set(map(ord, quitChars))
debugInts = set(map(ord, debugChars))
debug = False


def instructions():
	print "Press %s or ESC inside the window to quit" % " ".join(quitChars)
	print "Press d to toggle debugging mode"

def parseArgs(args):
	global debug
	for string in args:
		if string == "--debug":
			debug = True

def main():
	global debug
	kinect = ktk.Kinect()
	image, depth = kinect.getSensorData()
	frame = ktm.Frame(image, depth)
	view = ktv.CVKTView(WINDOW_NAME, frame, debug)
	view.setVisible(True)
	while True:
		image, depth = kinect.getSensorData()
		frame.update(image, depth)
		char = cv.WaitKey(10)
		if char in quitInts:
			break
		elif char in debugInts:
			debug = not debug
			view.setDebug(debug)
		elif char == -1:
			pass
		else:
			print char

if __name__ == "__main__":
	instructions()
	parseArgs(sys.argv)
	main()
	
