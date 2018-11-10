#import picamera
#
#camera.start_preview()
#time.sleep(5)
#camera.capture('/home/pi/Dev/cfehome/media-root/cam.jpg')
#camera.stop_preview()
import picamera
import subprocess
import time
camera = picamera.PiCamera()
camera.start_preview()
time.sleep(5)
camera.capture("/home/pi/Dev/cfehome/media-root/cam.jpg")
camera.stop_preview()