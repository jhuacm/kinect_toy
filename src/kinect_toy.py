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

#commadn line switches
cascadePath = None
detectInterval = -1.0
debug = False
usageNeeded = False

#character maps for control
def charsToInt(characterSet):
	return set(map(ord, characterSet))

quitChars = ('q', chr(27))
debugChars = ('d')
upChars = ('w')
downChars = ('s')
levelChars = ('e')
quitInts = charsToInt(quitChars)
debugInts = charsToInt(debugChars)
upInts = charsToInt(upChars)
downInts = charsToInt(downChars)
levelInts = charsToInt(levelChars)
movementInts = upInts.union(downInts).union(levelInts)


def instructions():
	print "Select the window and type the following commands:"
	print "--------------------------------------------------"
	print "Press %s or ESC inside the window to quit" % " ".join(quitChars)
	print "Press d to toggle debugging mode"

def parseArgs(args):
	global debug
	global cascadePath
	global detectInterval
	global usageNeeded
	for string in args[1:]:
		strings = string.split("=")
		if string == "--debug":
			debug = True
		elif strings[0] == "--cascade-path":
			if len(strings) > 1:
				cascadePath = strings[1]
		elif strings[0] == "--detect-interval":
			if len(strings) > 1:
				detectInterval = float(strings[1])
		else:
			usageNeeded = True
			break

def usage(name):
	print """usage: %s [--detect-interval=<float>] [--cascade-path=<path>] [--debug | -d]""" % name

def main():
	global debug
	global cascadePath
	global detectInterval
	kinect = ktk.Kinect()
	image, depth = kinect.getSensorData()
	frame = ktm.Frame(image, depth, cascadePath, detectInterval)
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
			"""
		elif char in movementInts:
			frame.stopDetecting()
			if char in upInts:
				kinect.adjustTilt(1)
			elif char in downInts:
				kinect.adjustTilt(-1)
			elif char in levelInts:
				kinect.resetTilt()
			frame.startDetecting()
			"""
		elif char == -1:
			pass
		else:
			print char

if __name__ == "__main__":
	parseArgs(sys.argv)
	if usageNeeded:
		usage(sys.argv[0])
	else:
		instructions()
		main()
	
