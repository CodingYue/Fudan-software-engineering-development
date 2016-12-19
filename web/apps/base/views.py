"""Views for the base app"""

from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
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
	if response["message"] == Message.SUCCESS:
		return HttpResponseRedirect('/')
	else:
		return render(request, 'simulation/upload_images.html', response)

@csrf_exempt
def search_by_image(request):
	response = service.handle_search_by_image(request)
	if response["message"] == Message.SUCCESS:
		return render(request, 'simulation/search.html', response)
	else:
		return render(request, 'simulation/search_by_image.html', response)

def search(request):
	pass

@csrf_exempt
def click_like(request):
	response = service.handle_click_like(request)
	if response["message"] == Message.SUCCESS:
		return HttpResponse()
	else:
		return HttpResponseNotFound()
