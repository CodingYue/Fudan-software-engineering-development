from django import forms
from taggit import forms as tagforms

"""
	for old upload
"""
class UploadImageForm(forms.Form):
	description = forms.CharField(widget = forms.Textarea)
	category = forms.CharField(widget = forms.Textarea)
	# tags = forms.CharField(widget = forms.Textarea)
	tags = tagforms.TagField()
	file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

"""
	for new upload
	add description
"""
class ImageDetailedForm(forms.Form):
	description = forms.CharField(widget = forms.Textarea)
	category = forms.CharField(widget = forms.Textarea)
	tags = tagforms.TagField()
	file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

"""
 	for new upload
	upload single image
"""
class ImageForm(forms.Form):
	file = forms.ImageField()
