"""Views for the base app"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.html import escape
from django.contrib.auth.models import User
from .forms import UploadImageForm
from .models import Image

def home(request):
    """ Default view for the root """
    if request.user.is_authenticated():
    	isLogged = True
    else:
    	isLogged = False
    return render(request, 'base/home.html', {'isLogged' : isLogged})

def login_user(request):

	logout(request)
	if request.POST:

		#print 'views.login_user : Login!'
		username = escape(request.POST['username'])
		password = escape(request.POST['password'])

		user = authenticate(username = username, password = password)

		isLogged = False

		if user is not None:
			if user.is_active:
				login(request, user)
				response = "You are logged in, and allowed to access any page of the website."
				isLogged = True
				return redirect("/", {'response' : response, 'isLogged' : isLogged})
			else:
				response = "Disabled account"
				isLogged = False
				return render(request, 'simulation/login.html', {'response' : response, 'isLogged' : isLogged})
		else:
			response = "Invalid username or password."
			isLogged = False
			return render(request, 'simulation/login.html', {'response' : response, 'isLogged' : isLogged})
	else:
		response = ''
		isLogged = False
		return render(request, 'simulation/login.html', {'response' : response, 'isLogged' : isLogged})

def logout_user(request):
	logout(request)
	isLogged = False
	text = """You are logged out"""
	return redirect("/", {'text' : text, 'isLogged' : isLogged})

def registration_user(request):
	logout(request)

	isLogged = False
	response = '';

	if request.POST:
		#print 'views.registration : Register!'
		username = escape(request.POST['username'])
		password = escape(request.POST['password'])
		email = escape(request.POST['email'])

		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None

		if user is None:
			response = 'registration success!'
			user = User.objects.create_user(username, email, password)
			user.save()
			return redirect('/login', {'response' : response, 'isLogged' : isLogged})
		else:
			response = 'username already exists!'
			return render(request, 'simulation/registration.html', {'response' : response, 'isLogged' : isLogged})
	else:
		response = ''
		return render(request, 'simulation/registration.html', {'response' : response, 'isLogged' : isLogged})

def upload_images(request):
	if request.user.is_authenticated():
		isLogged = True
	else:
		isLogged = False

	response = ""

	if not isLogged:
		response = "Log in at first, please"
		return redirect("/", {"response" : response, "isLogged" : isLogged})

	form = UploadImageForm()

	if request.POST:
		print "upload_image : uploading"
		
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			newImage = Image(file = request.FILES['file'])
			newImage.save()
			return render(request, 'simulation/upload_images.html', {'response' : response, 'isLogged' : isLogged, "form":form})
		else:
			form = UploadImageForm()

	return render(request, 'simulation/upload_images.html', {'response' : response, 'isLogged' : isLogged, "form" : form})