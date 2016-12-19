
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.html import escape
from django import template
from .forms import UploadImageForm, ImageForm
from .models import Image, UserImageAffiliation
from .message import Message
import utilities

def get_user_image_affiliation(username, imageUrl):

	try:
		instance = UserImageAffiliation.objects.get(username = username, imageUrl = imageUrl)
	except UserImageAffiliation.DoesNotExist:
		instance = UserImageAffiliation(username = username, imageUrl = imageUrl)

	#print username, imageUrl, instance.enable
	return instance

def handle_authenticate(request):
	if request.user.is_authenticated():
		isLogged = True
	else:
		isLogged = False
	return {"message" : Message.SUCCESS, "isLogged" : isLogged, "username" : request.user.username}

def handle_login(request):
	logout(request)
	if request.POST:
		username = escape(request.POST['username'])
		password = escape(request.POST['password'])
		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return {"message" : Message.SUCCESS, "isLogged" : True, "username" : request.user.username}
			else:
				return {"message" : Message.LOGIN_USER_DISABLED, "isLogged" : False, "username" : request.user.username}
		else:
			return {"message" : Message.LOGIN_WRONG_USERNAME_OR_PASSWORD,
				"isLogged" : False, "username" : request.user.username}
	else:
		return {"message" : Message.POST_NOT_FOUND, "isLogged" : False, "username" : request.user.username}

def handle_logout(request):
	logout(request)
	return {"message" : Message.SUCCESS, "isLogged" : False, "username" : request.user.username}

def handle_registration(request):
	logout(request)

	if request.POST:
		username = escape(request.POST['username'])
		password = escape(request.POST['password'])
		email = escape(request.POST['email'])

		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None

		if user is None:
			user = User.objects.create_user(username, email, password)
			user.save()
			return {"message" : Message.SUCCESS, "isLogged" : False, "username" : request.user.username}
		else:
			return {"message" : Message.REGISTRATION_USER_ALREADY_EXISTS, "isLogged" : False,
                    "username" : request.user.username}
	else:
		return {"message" : Message.POST_NOT_FOUND, "isLogged" : False, "username" : request.user.username}

"""
	for new upload
	upload single image
	tag and category are returned as response
"""
def handle_add_image(request):
	if request.user.is_authenticated():
		isLogged = True
	else:
		isLogged = False

	if not isLogged:
		return {"message": Message.USER_NOT_LOGGED_IN, "isLogged": False, "username": request.user.username}
	form = ImageForm()
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			image = request.FILES.getlist('file')[0]
			img_aid = utilities.upload_image(image)
			category = utilities.category(image, img_id = img_aid)
			tags = utilities.tag(image, img_id = img_aid)
			return {"message": Message.SUCCESS, "isLogged": isLogged, "form": form, "username": request.user.username, "category": category, "tags": tags}
		else:
			return {"message": Message.UPLOAD_IMAGES_FORM_ERROR, "isLogged": isLogged, "form": form, "username": request.user.username}
	else:
		return {"message": Message.POST_NOT_FOUND, "isLogged": isLogged, "form": form, "username": request.user.username}

"""
	for new upload
	add image description
"""
def handle_add_image_description(request):

	if request.user.is_authenticated():
		isLogged = True
	else:
		isLogged = False

	if not isLogged:
		return {"message" : Message.USER_NOT_LOGGED_IN, "isLogged" : False, "username" : request.user.username}

	form = ImageDetailedForm()

	if request.POST:
		form = ImageDetailedForm(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('file')
			for f in files:
				newImage = Image(
					file = f,
					author = request.user.username,
					description = request.POST['description'],
					category = request.POST['category'],
					tags = request.POST['tags'],
					likeNumber = 0)
				newImage.save()
			return {"message" : Message.SUCCESS, "isLogged" : isLogged, "form" : form,
                    "username" : request.user.username}
		else:
			return {"message" : Message.UPLOAD_IMAGES_FORM_ERROR, "isLogged" : isLogged, "form" : form, "username" : request.user.username}
	else:
		return {"message" : Message.POST_NOT_FOUND, "isLogged" : isLogged, "form" : form,
                "username" : request.user.username}

"""
	for old upload
"""
def handle_upload_images(request):

	if request.user.is_authenticated():
		isLogged = True
	else:
		isLogged = False

	if not isLogged:
		return {"message" : Message.USER_NOT_LOGGED_IN, "isLogged" : False, "username" : request.user.username}

	form = UploadImageForm()

	if request.POST:
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('file')
			for f in files:
				newImage = Image(
					file = f,
					author = request.user.username,
					description = request.POST['description'],
					likeNumber = 0)
				newImage.save()
			return {"message" : Message.SUCCESS, "isLogged" : isLogged, "form" : form,
                    "username" : request.user.username}
		else:
			return {"message" : Message.UPLOAD_IMAGES_FORM_ERROR, "isLogged" : isLogged, "form" : form,
                    "username" : request.user.username}
	else:
		return {"message" : Message.POST_NOT_FOUND, "isLogged" : isLogged, "form" : form,
                "username" : request.user.username}

def handle_list_images(request):

	DEFAULT_LIMIT = 10

	if request.user.is_authenticated():
		isLogged = True
	else:
		isLogged = False

	imageList = []

	if request.POST:
		condition = request.POST["condition"]
		limit = request.POST["limit"]
		images = Image.objects.all()
		import random
		import math
		random.shuffle(images)
		imageList = images[:math.min(limit, len(images))]
	else:
		limit = DEFAULT_LIMIT
		images = list(Image.objects.all())
		import random
		random.shuffle(images)
		imageList = images[:min(limit, len(images))]


	return {"message" : Message.SUCCESS, "isLogged" : isLogged, "imageList" : imageList,
            "username" : request.user.username}

def handle_click_like(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			username = request.user.username
			imageUrl = request.POST['imageUrl']
			image = Image.objects.get(file = imageUrl)
			userImageAffiliation = get_user_image_affiliation(username, imageUrl)
			if userImageAffiliation.enable:
				print "from enable to disable"
				image.likeNumber -= 1
				userImageAffiliation.enable = False
			else:
				print "from disable to enable"
				image.likeNumber += 1
				userImageAffiliation.enable = True
			image.save()
			userImageAffiliation.save()
			return {"message" : Message.SUCCESS, "isLogged" : True, "username" : request.user.username}
		else:
			print "Bad"
			return {"message" : Message.POST_NOT_FOUND, "isLogged" : True, "username" : request.user.username}

	else:
		return {"message" : Message.USER_NOT_LOGGED_IN, "isLogged" : False, "username" : request.user.username};
