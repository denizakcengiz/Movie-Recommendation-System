from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^$', views.movie.index, name='index'),
	url(r'^search/$', views.movie.search, name='search'),
]