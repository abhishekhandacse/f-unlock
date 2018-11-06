from django.shortcuts import render,redirect, get_object_or_404
# from .models import 

# Create your views here.
def home(request):
	# unlocker = unlocker.objects
	return render(request,'unlocker/home.html')

def panel(request):
	# unlocker = unlocker.objects
	return render(request,'unlocker/panel.html')