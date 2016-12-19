"""Base models"""

from django.db import models
from django.forms import Form, ImageField
from taggit.managers import TaggableManager


def upload_path_handler(instance, filename, category):
	import os.path
	import time
	fn, ext = os.path.splitext(filename)
	return "images/{category}/{id}{ext}".format(category=category, id=int(time.time() * 1000), ext=ext)


class Image(models.Model):
	author = models.CharField(max_length=100)
	description = models.CharField(max_length=5000, blank = True)
	category = models.CharField(max_length=100)
	tags = TaggableManager()
	# likedby = models.ManyToManyField()
	likeNumber = models.IntegerField(default=0)
	file = models.FileField(
		upload_to = upload_path_handler)

	def __unicode__(self):
		return self.file.url


class UserImageAffiliation(models.Model):
	username = models.CharField(max_length=100)
	imageUrl = models.CharField(max_length=100)
	enable = models.BooleanField(default=False)

	def __unicode__(self):
		return "User %s, ImageUrl %s, enable %s" % (user, imageUrl, str(enable))
