from django import forms

class UploadImageForm(forms.Form):
	description = forms.CharField(widget = forms.Textarea)
	file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

