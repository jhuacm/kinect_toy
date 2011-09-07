#ktmodel.py
"""
 Model classes for kinect_toy
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""

class Face(object):
	pass

class Frame(object):
	def __init__(self, image, depth):
		self._faces = []
		self._observers = []
		self.update(image, depth)

	def update(self, image, depth):
		self._image = image
		self._rawDepth = depth
		self._filteredDepth = depth
		self._notifyObservers()
	
	def getImage(self):
		return self._image
	
	def getDepthRaw(self):
		return self._rawDepth
	
	def getDepthFiltered(self):
		return self._filteredDepth
	
	def registerObserver(self, observer):
		self._observers.append(observer)
	
	def removeObserver(self, observer):
		self._observers.remove(observer)
	
	def _notifyObservers(self):
		for observer in self._observers:
			observer.modelChanged(self)
		

