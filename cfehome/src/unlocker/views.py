from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import useractivity,facedata
from .models import OneTimeRequest
import picamera
import time
import subprocess
from django.core.files import File

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def onetime(request):
	# cmd = "raspistill -o /home/pi/Dev/cfehome/media-root/cam.jpg"
	# subprocess.call(cmd, shell=True)
	if request.method == 'POST':
		# camera = picamera.PiCamera()
		# camera.start_preview()
		# time.sleep(3)
		# camera.capture("/home/pi/Dev/cfehome/media-root/cam.jpg")
		# camera.stop_preview()
		# cmd = "raspistill -o /home/pi/Dev/cfehome/media-root/cam.jpg"
		# subprocess.call(cmd, shell=True)
		# subprocess.Popen(["python","/home/pi/Dev/cfehome/media-root/cam.py"], close_fds=True)
		subprocess.call("raspistill --nopreview -t 5000 -o /home/pi/Dev/cfehome/media-root/cam.jpg", shell=True)
		time.sleep(5)
		reopen = open('/home/pi/Dev/cfehome/media-root/cam.jpg', "r+b")
		django_file = File(reopen)
		tempvar = OneTimeRequest()
		tempvar.image.save("cam.jpg", django_file, save=True)
		# tempvar = OneTimeRequest.objects.create(image=django_file)
	return render(request,'unlocker/home.html')

def home(request):
	# unlocker = unlocker.objects
	return render(request,'unlocker/home.html')

@login_required
def panel(request):
	# unlocker = unlocker.objects
	if request.method == 'POST':
		new_act = useractivity.objects.create(user=request.user,activity='checkin')

	userdata = get_object_or_404(facedata,owner=request.user)
	userdetails = get_object_or_404(User,username=request.user)
	checkins = useractivity.objects.all().filter(user=request.user).order_by("-timestamp")
	return render(request,'unlocker/panel.html',{'list':checkins, 'userdata':userdata, 'userdetails':userdetails})