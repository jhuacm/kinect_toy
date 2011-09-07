# ktkinect.py
"""
 Module for communicating with the Kinect sensor
 Author: Charles Duyk
 Email: charles.duyk@gmail.com
 Date: September 7, 2011
"""
import freenect
import frame_convert as fc

TILT_UPPER_BOUND = 30
TILT_LOWER_BOUND = -30
TILT_NEUTRAL = 0
desiredTilt = 0
	
def clampTiltValue(val):
	if val > TILT_UPPER_BOUND:
		val = TILT_UPPER_BOUND
	elif val < TILT_LOWER_BOUND:
		val = TILT_LOWER_BOUND
	return val

def incrementTilt(val):
	global desiredTilt
	desiredTilt = clampTiltValue(desiredTilt + val)

def tilt():
	freenect.set_tilt_degs(dev, desiredTilt)
	cv.WaitKey(10)

def tiltLoop():
	freenect.runloop(body=tilt)

class Kinect(object):
	def __init__(self):
		pass

	def adjustTilt(self, val):
# 		incrementTilt(val)
#		tiltLoop()
		raise KTKinectError("Tilting is broken :-(")
		
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

