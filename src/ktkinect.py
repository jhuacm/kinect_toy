# ktkinect.py
"""
 Module for communicating with the Kinect sensor
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""
import freenect
import frame_convert as fc
import cv

class Kinect(object):
	
	def getDepthData(self):
		npDepth, _ = freenect.sync_get_depth()
		cvDepth = fc.pretty_depth_cv(npDepth)
		return cvDepth

	def getImageData(self):
		npImage, _ = freenect.sync_get_video()
		cvImage = fc.video_cv(npImage)
		return cvImage
		
	def getSensorData(self):
		"""
		Returns a tuple of cvImages containing (imageData, depthData)

		TODO: error handling
		"""
		image = self.getImageData()
		depth = self.getDepthData()
		return (image, depth)


class KTKinectError(Exception):
	def __init__(self, reason):
		self.reason = reason
	def __str__(self):
		return self.reason

