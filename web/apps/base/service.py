
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.html import escape
from .forms import UploadImageForm
from .models import Image
from .message import Message

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
					likenumber = 1)
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
