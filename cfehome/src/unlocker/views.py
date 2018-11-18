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
import RPi.GPIO as GPIO
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
    s3client = boto3.client('s3')
    client = boto3.client('rekognition')
    source_imgs_path = 'source_imgs'
    target_img_path = '/home/pi/Dev/cfehome/media-root/target.jpg'
    if os.path.exists(target_img_path) is False:
        target_img_path = '/home/pi/Dev/cfehome/media-root/target.jpg'
    result = None
    for obj in s3client.list_objects(Bucket='funlock')['Contents']:
        source_name = obj['Key']
        if source_name.endswith('jpg') or source_name.endswith('png'):
            target_img = open(target_img_path, 'rb')
            try:
                response = client.compare_faces(SimilarityThreshold=50,
                                                SourceImage={'S3Object':{'Bucket':'funlock','Name':source_name}},
                                                TargetImage={'Bytes': target_img.read()})
            except:
                result = "Denied"
                target_img.close()
                return result
            if response['FaceMatches'] is not None and len(response['FaceMatches']) > 0:
                result = source_name[:len(source_name)-4]
                target_img.close()
                break
            # target_img.close()
    if result is not None:
        return result
    else:
        result = "Denied"
        return result

def funlock(request):
	msg = ""
	if request.method == 'POST':
		with picamera.PiCamera() as camera:
			camera.resolution = (1024, 768)
			time.sleep(2)
			camera.capture('/home/pi/Dev/cfehome/media-root/target.jpg')
		# result="ajayjindal"
		result = face_comp()
		if result == "Denied":
			msg = "No"
			return render(request,'unlocker/home.html',{'msg':msg})
		else:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(7,GPIO.OUT)
			p=GPIO.PWM(7,50)
			p.start(7.5)
			time.sleep(1)
			p.ChangeDutyCycle(12.5)
			time.sleep(1)
			p.ChangeDutyCycle(2.5)
			time.sleep(1)
			p.stop()
			GPIO.cleanup()
			obj = get_object_or_404(User,username=result)
			new_act = useractivity.objects.create(user=obj,activity='checkin')
			msg = "Success! Door unlocked. Welcome, " + obj.first_name + " " + obj.last_name
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
