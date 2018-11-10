from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.
def signup(request):
	if request.method=='POST':
		if request.POST['pass1']==request.POST['pass2']:
			if request.POST['username'] and request.POST['firstname'] and request.POST['lastname'] and request.POST['email'] and request.POST['pass1']:
				try:
					user = User.objects.get(username =request.POST['username'])
					return render(request, 'accounts/signup.html',{'error':'Username already taken!'})
				except User.DoesNotExist:
					user = User.objects.create_user(
						request.POST['username'],
						first_name=request.POST['firstname'],
						last_name=request.POST['lastname'],
						email=request.POST['email'],
						password=request.POST['pass1']
						)
					auth.login(request, user)
					return redirect('home')
			else:
				return render(request,'accounts/signup.html',{'error':'All fields are required!'})	
		else:
			return render(request, 'accounts/signup.html',{'error':'Passwords must match!'})
	return render(request, 'accounts/signup.html')

def login(request):
	if request.user.is_authenticated:
		return redirect('panel')
	if request.method=='POST':
		user = auth.authenticate(username=request.POST['username'],password=request.POST['pass'])
		if user is not None:
			auth.login(request, user)
			return redirect('panel')
		else:
			return render(request, 'accounts/login.html',{'error':'Incorrect info!'})
	else:	
		return render(request, 'accounts/login.html')

def logout(request):
	if request.method=='POST':
		auth.logout(request)
		return redirect('home')