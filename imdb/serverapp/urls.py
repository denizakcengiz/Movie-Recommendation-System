from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^$', views.movie.index, name='index'),
	url(r'^search/$', views.movie.search, name='search'),
	url(r'^show/(?P<movie_id>[0-9]+)/$', views.movie.show, name='show'),
	url(r'^show/(?P<movie_id>[0-9]+)/update/$', views.movie.updateRecommendations, name='update_recommendation'),
]