# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from serverapp import models
from django.conf import settings
from serverapp.lib.searcher import SearchFiles

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
	return render(request, "serverapp/show.html", {"movie": movie})

