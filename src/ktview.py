"""
 ktview.py
 View classes for kinect_toy
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""

import ktmodel as ktm
import cv

IMG_RAW_SUFFIX = "_img_raw"
DEPTH_RAW_SUFFIX = "_depth_raw"
DEPTH_FILTERED_SUFFIX = "_depth_filtered"

class KTView(object):
	def __init__(self, name, frame):
		self._name = name
		self._frame = frame
		self._frame.registerObserver(self)
	
	def getName(self):
		return self._name
	
	def getFrame(self):
		return self._frame

	def isVisible(self):
		pass

	def setVisible(self, visible):
		pass
	
	def modelChanged(self, frame):
		pass

	def updateView(self):
		pass

class CVKTView(KTView):
	def __init__(self, name, frame, debug=False):
		super(CVKTView, self).__init__(name, frame)	
		self._imageRawName = name + IMG_RAW_SUFFIX
		self._depthRawName = name + DEPTH_RAW_SUFFIX
		self._depthFilteredName = name + DEPTH_FILTERED_SUFFIX
		self._visible = False
		self._debug = debug

	def setVisible(self, visible):
		self._visible = visible
		self.updateView()

	def isVisible(self):
		return self._visible

	def setDebug(self, debug):
		self._debug = debug
		self.updateView()
	
	def isDebugging(self):
		return self._debug
	
	def modelChanged(self, frame):
		self.updateView()

	def updateView(self):
		self._updateWindowVisibility()
		if self.isVisible():
			self._drawMainWindow()
			if self.isDebugging():
				self._drawDebuggingWindows()
	
#Drawing Functions
	def _drawMainWindow(self):
		windowImage = self.getFrame().getImage()
		faces = self.getFrame().getFaces()
		for face in faces:
			v1 = face.getV1()
			v2 = face.getV2()
			color = face.getColor()
			cv.Rectangle(windowImage, v1, v2, color)
		cv.ShowImage(self.getName(), windowImage)
	
	def _drawDebuggingWindows(self):
		frame = self.getFrame()
		cv.ShowImage(self._imageRawName, frame.getImage())
		cv.ShowImage(self._depthRawName, frame.getDepthRaw())
		cv.ShowImage(self._depthFilteredName, frame.getDepthFiltered())

#Window management functions
	def _createMainWindow(self):
		cv.NamedWindow(self.getName())
		
	def _createDebugWindows(self):
		cv.NamedWindow(self._imageRawName)
		cv.NamedWindow(self._depthRawName)
		cv.NamedWindow(self._depthFilteredName)
		
	def _destroyDebugWindows(self):
		cv.DestroyWindow(self._imageRawName)
		cv.DestroyWindow(self._depthRawName)
		cv.DestroyWindow(self._depthFilteredName)

	def _destroyWindows(self):
		cv.DestroyAllWindows()

	def _updateWindowVisibility(self):
		if self.isVisible():
			self._createMainWindow()
			if self._debug:
				self._createDebugWindows()
			else:
				self._destroyDebugWindows()
		else:
			self._destroyWindows()

