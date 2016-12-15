"""Base models"""

from django.db import models
from django.forms import Form, ImageField

def upload_path_handler(instance, filename):
	import os.path
	import time
	fn, ext = os.path.splitext(filename)
	return "images/{id}{ext}".format(id=int(time.time()*1000), ext=ext)

class Image(models.Model):
	author = models.CharField(max_length=100)
	description = models.CharField(max_length=5000)
	file = models.FileField(
		upload_to = upload_path_handler)

	def __unicode__(self):
		return self.file.url