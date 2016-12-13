"""Base models"""

from django.db import models
from django.forms import Form, ImageField

class Image(models.Model):
	#author = models.CharField(max_length=100)
	#description = models.CharField(max_length=5000)
	file = models.FileField(upload_to='repository/%Y/%m/%d')
