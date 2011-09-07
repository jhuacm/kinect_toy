#ktmodel.py
"""
 Model classes for kinect_toy
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""

import cv
import time

DEFAULT_DETECT_INTERVAL=.1

CASCADE_DEFAULT_PATH = "../resources/haarcascade_frontalface_default.xml"
CASCADE_SCALE_FACTOR = 1.2
CASCADE_MIN_NEIGHBORS = 2
CASCADE_FLAGS = cv.CV_HAAR_DO_CANNY_PRUNING
CASCADE_MIN_SIZE = (40, 30)


class Face(object):
	def __init__(self, x, y, w, h):
		self._v1 = (x, y)
		self._v2 = (x+w, y+h)

	def getV1(self):
		return self._v1
	
	def getV2(self):
		return self._v2

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
		self._nextDetect = time.time()
		self.update(image, depth)

	def update(self, image, depth):
		self._image = image
		self._rawDepth = depth
		t = time.time()
		if t >= self._nextDetect:
			self._nextDetect = t + self._detectInterval
			self._preprocess()
			tupleList = self._findFaces()
			self._mergeFaces(tupleList)
		self._notifyObservers()
	
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
		for tup in tupleList:
			x, y, w, h = tup[0]
			f = Face(x, y, w, h)
			newFaceList.append(f)
		self._faces = newFaceList

#observing methods
	def registerObserver(self, observer):
		self._observers.append(observer)
	
	def removeObserver(self, observer):
		self._observers.remove(observer)
	

	def _notifyObservers(self):
		for observer in self._observers:
			observer.modelChanged(self)
		

