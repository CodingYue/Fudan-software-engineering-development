"""Views for the base app"""

from django.shortcuts import render, redirect
from .message import Message
import service

def home(request):
    response = service.handle_list_images(request)
    print response["imageList"]
    return render(request, 'base/home.html', response)

def login_user(request):
	response = service.handle_login(request)
	if response["message"] == Message.SUCCESS:
		return redirect("/", response)
	else:
		return render(request, 'simulation/login.html', response)

def logout_user(request):
	response = service.handle_logout(request)
	return redirect("/", response)

def registration_user(request):
	response = service.handle_registration(request)
	if response["message"] == Message.SUCCESS:
		return redirect('/login', response)
	else:
		return render(request, 'simulation/registration.html', response)

def upload_images(request):
	response = service.handle_upload_images(request)
	return render(request, 'simulation/upload_images.html', response)