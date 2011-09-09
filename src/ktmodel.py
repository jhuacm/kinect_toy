#ktmodel.py
"""
 Model classes for kinect_toy
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""

import cv
import time
import random

DEFAULT_DETECT_INTERVAL=.0

CASCADE_DEFAULT_PATH = "../resources/haarcascade_frontalface_default.xml"
CASCADE_SCALE_FACTOR = 1.2
CASCADE_MIN_NEIGHBORS = 2
CASCADE_FLAGS = cv.CV_HAAR_DO_CANNY_PRUNING
CASCADE_MIN_SIZE = (40, 30)

def now():
	return time.time()
def distantFuture():
	return now() + 60*60*24*365

def generateRandomColor():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	ordinal = random.randint(0,2)
	color = [r, g, b]
	color[ordinal] = 0
	return tuple(color)

def pairwiseSum(tup):
	return reduce(lambda x, y: tuple(sum(t) for t in zip(x, y)), tup)

def midpoint(rect):
	return (rect[0] + rect[2], rect[1] + rect[3])

class Face(object):
	def __init__(self, rect):
		self._history = [rect for i in range(4)]
		self._color = generateRandomColor()
		self._histPos = 0
		self._updatePoints()
	
	def getX(self):
		return self._xy[0]
	
	def getY(self):
		return self._xy[1]

	def getWidth(self):
		return self._wh[0]

	def getHeight(self):
		return self._wh[1]
	
	def getWidthHeight(self):
		return self._wh

	def getV1(self):
		return self._xy
	
	def getV2(self):
		return self._v2
	
	def getColor(self):
		return self._color
	
	def merge(self, rect):
		ret = self._contains(rect)
		if ret:
			self._updateHistory(rect)
			self._updatePoints()
		return ret
	
	def _contains(self, rect):
		myX = self.getX()
		otherX = rect[0]
		res = otherX - myX
		if res < 0 or res > self.getWidth():
			return False
		myY = self.getY()
		otherY = rect[1]
		res = otherY - myY
		if res < 0 or res > self.getHeight():
			return False
		return True
		
	def _updatePoints(self):
		tup = pairwiseSum(self._history)
		tup = map(lambda x: x>>2, tup)
		xy = tuple(tup[:2])
		wh = tuple(tup[2:])
		self._xy = xy
		self._wh = wh
		self._v2 = pairwiseSum((xy, wh))
	
	def _updateHistory(self, tup):
		pos = self._histPos
		self._history[pos] = tup
		pos = pos + 1
		pos = pos % 4
		self._histPos = pos


class Frame(object):
	def __init__(self, image, depth, cascadePath=None, detectInterval=-1.0):
		self._faces = []
		self._observers = []
		if not cascadePath:
			cascadePath = CASCADE_DEFAULT_PATH
		if detectInterval < 0.0:
			detectInterval = DEFAULT_DETECT_INTERVAL
		self._cascade = cv.Load(cascadePath)
		self._bwImage = cv.CreateImage((image.width, image.height), cv.IPL_DEPTH_8U, 1)
		self._memStorage = cv.CreateMemStorage()
		self._detectInterval = detectInterval
		self._nextDetect = now()
		self.update(image, depth)

	def update(self, image, depth):
		self._image = image
		self._rawDepth = depth
		t = now()
		if t >= self._nextDetect:
			self._nextDetect = t + self._detectInterval
			self._preprocess()
			tupleList = self._findFaces()
			self._mergeFaces(tupleList)
		self._notifyObservers()
	
	def startDetecting(self):
		self._nextDetect = now()

	def stopDetecting(self):
		self._nextDetect = distantFuture()
		self._faces = []
	
	def getFaces(self):
		return self._faces
	
	def getImage(self):
		return self._image
	
	def getBWImage(self):
		return self._bwImage
	
	def getDepthRaw(self):
		return self._rawDepth
	
	def getDepthFiltered(self):
		return self._filteredDepth

#Image processing
	def _preprocess(self):
		self._filteredDepth = self._rawDepth
		cv.CvtColor(self._image, self._bwImage, cv.CV_BGR2GRAY)
		
	def _findFaces(self):
#returns a list of tuples of ((x, y, w, h), n). Every cycle counts here.
		rects = cv.HaarDetectObjects(self._bwImage, self._cascade, self._memStorage, CASCADE_SCALE_FACTOR, CASCADE_MIN_NEIGHBORS, CASCADE_FLAGS, CASCADE_MIN_SIZE)
		return rects
	
	def _mergeFaces(self, tupleList):
		newFaceList = []
		success = False
		for tup in tupleList:
			rect = tup[0]
			lastFace = None
			for face in self.getFaces():
				success = face.merge(rect)
				if success:
					lastFace = face
					break
			if not success:
				f = Face(rect)
				newFaceList.append(f)
			else:
				newFaceList.append(lastFace)
		self._faces = newFaceList

#observing methods
	def registerObserver(self, observer):
		self._observers.append(observer)
	
	def removeObserver(self, observer):
		self._observers.remove(observer)
	

	def _notifyObservers(self):
		for observer in self._observers:
			observer.modelChanged(self)
		

