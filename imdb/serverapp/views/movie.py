# -*- coding: utf-8 -*-
import os 

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from serverapp import models
from django.conf import settings
from serverapp.lib.searcher import SearchFiles
from serverapp.lib.recommendation import RecommendationUnit

@require_GET
def index(request):
	movies = models.Movie.objects.all()[:9]
	return render(request, "serverapp/index.html", {"movies": movies})

@require_GET
def search(request):
	keyword = request.GET.get("keyword")
	if not keyword:
		return redirect("serverapp:index")
	searcher = SearchFiles(keyword, 20)
	synopsis_ids = searcher.search(settings.SYNOPSIS_INDEX)
	doc_index = {id: synopsis_ids.index(id) for id in synopsis_ids[:9]}
	movies = models.Movie.objects.filter(id__in=doc_index.keys())[:9]
	ranked_movies = [0] * len(movies)
	for movie in movies:
		new_index = doc_index[movie.id]
		ranked_movies[new_index] = movie
	return render(request, "serverapp/index.html", {"movies": ranked_movies})

@require_GET
def show(request, movie_id):
	movie = models.Movie.objects.get(pk=movie_id)
	storyline_path = os.path.join(settings.STORYLINE, "{0}".format(movie.id))
	storyline = open(storyline_path).read()
	synopsis_path = os.path.join(settings.SYNOPSIS, "{0}".format(movie.id))
	synopsis = open(synopsis_path).read()
	movie_ids, important_fields = RecommendationUnit.get_similar_movies(movie, 1, 1, 1, 1, 1, 1)
	doc_index = {id: movie_ids.index(id) for id in movie_ids[:9]}
	print "movie_ids: ", movie_ids
	print "important_fields: ", important_fields
	movies = models.Movie.objects.filter(id__in=doc_index.keys())[:9]
	recommended_movies = [0] * len(movies)
	i = 0
	for movie in movies:
		new_index = doc_index[movie.id]
		# recommended_movies[new_index] = (movie, important_fields[i])
		recommended_movies[new_index] = movie
		i += 1
	content = {
		"movie": movie,
		"storyline": storyline,
		"synopsis": synopsis,
		"recommended_movies": recommended_movies[:4]
	}
	return render(request, "serverapp/show.html", content)

