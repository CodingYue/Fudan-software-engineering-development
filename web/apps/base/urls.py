"""urlconf for the base application"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login_user, name='login_user'),
    url(r'^logout$', views.logout_user, name='logout_user'),
    url(r'^registration$', views.registration_user, name='registration_user'),
    url(r'^upload_images$', views.upload_images, name='update_images'),
    url(r'^search_by_image$', views.search_by_image, name='search_by_image'),
    url(r'^search$', views.search, name='search'),
    url(r'^click_like$', views.click_like, name='click_like'),
	url(r'^add_image$', views.add_image, name='add_images'),
	url(r'^add_image_description$', views.add_image_description, name='add_image_description')
]
