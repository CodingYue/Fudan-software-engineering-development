
from django import template
from ..service import get_user_image_affiliation as my_get_user_image_affiliation

register = template.Library()

@register.simple_tag
def get_user_image_affiliation(username, imageUrl):
	return my_get_user_image_affiliation(username, imageUrl).enable