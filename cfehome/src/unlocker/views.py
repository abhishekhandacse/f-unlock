from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import useractivity,facedata
from .models import OneTimeRequest
import picamera
import time
import subprocess
from django.core.files import File
import boto3
import os

def onetime(request):
	if request.method == 'POST':
		subprocess.call("raspistill --nopreview -t 2000 -o /home/pi/Dev/cfehome/media-root/cam.jpg -q 60", shell=True)
		time.sleep(2)
		reopen = open('/home/pi/Dev/cfehome/media-root/cam.jpg', "r+b")
		django_file = File(reopen)
		tempvar = OneTimeRequest()
		tempvar.image.save("cam.jpg", django_file, save=True)
	return render(request,'unlocker/home.html')

def home(request):
	return render(request,'unlocker/home.html')

def grant(request,id):
	if request.method=='POST':
		pro = get_object_or_404(OneTimeRequest,pk=id)
		pro.access = True
		pro.save()
		return redirect('/unlocker/panel/')
	return redirect('/unlocker/panel/')	

def face_comp():
    client = boto3.client('rekognition')
    source_imgs_path = '/home/pi/Dev/cfehome/media-root/source_imgs'
    target_img_path = '/home/pi/Dev/cfehome/media-root/target.jpg'
    result = None
    for file_name in sorted(os.listdir(source_imgs_path)):
        if file_name.endswith('jpg') or file_name.endswith('png'):
            source_img = open(os.path.join(source_imgs_path, file_name), 'rb')
            target_img = open(target_img_path, 'rb')
            try:
            	response = client.compare_faces(SimilarityThreshold=70,
                                            SourceImage={'Bytes': source_img.read()},
                                            TargetImage={'Bytes': target_img.read()})
            except:
            	source_img.close()
            	target_img.close()
            	return "Denied"
            if response['FaceMatches'] is not None and len(response['FaceMatches']) > 0:
                result = file_name[:len(file_name)-4]
                break
            source_img.close()
            target_img.close()
    if result is not None:
    	return result
    return "Denied"

def funlock(request):
	msg = ""
	if request.method == 'POST':
		# subprocess.call("raspistill --nopreview -t 2000 -o /home/pi/Dev/cfehome/media-root/target.jpg -q 80", shell=True)
		time.sleep(3)
		# result = face_comp()
		result = "Denied"
		if result == "Denied":
			msg = "No"
			return render(request,'unlocker/home.html',{'msg':msg})
		else:
			obj = get_object_or_404(User,username=result)
			new_act = useractivity.objects.create(user=obj,activity='checkin')
			msg = "Success! Door Unlocked. Welcome, " + obj.first_name + " " + obj.last_name
	
	return render(request,'unlocker/home.html',{'msg':msg})

@login_required
def panel(request):
	msg = ""
	if request.method == 'POST':
		new_act = useractivity.objects.create(user=request.user,activity='checkin')
		msg = "Welcome, Ajay Jindal!"
	
	userdata = get_object_or_404(facedata,owner=request.user)
	userdetails = get_object_or_404(User,username=request.user)
	checkins = useractivity.objects.all().filter(user=request.user).order_by("-timestamp")
	onetimerequests = OneTimeRequest.objects.all().order_by("-request_time")
	return render(request,'unlocker/panel.html',
		{
		'list':checkins, 
		'userdata':userdata, 
		'userdetails':userdetails,
		'onetimerequests':onetimerequests,
		'msg':msg,
		})
