"""urlconf for the base application"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login_user, name='login_user'),
    url(r'^logout$', views.logout_user, name='logout_user'),
    url(r'^registration$', views.registration_user, name='registration_user'),
    url(r'^upload_images$', views.upload_images, name='update_images'),
    url(r'^click_like$', views.click_like, name='click_like'),
]
