# -*- coding: utf-8 -*-
import os 

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.http import require_GET, require_POST

from serverapp import models
from serverapp.helpers import paginate_movies
from django.conf import settings
from serverapp.lib.searcher import SearchFiles
from serverapp.lib.recommendation import RecommendationUnit

@require_GET
def index(request):
	movies = models.Movie.objects.all()
	paginated_movies = paginate_movies(request, movies)
	return render(request, "serverapp/index.html", {"movies": paginated_movies})

@require_GET
def search(request):
	keyword = request.GET.get("keyword")
	if not keyword:
		return redirect("serverapp:index")
	searcher = SearchFiles(keyword, 20)
	synopsis_ids = searcher.search(settings.SYNOPSIS_INDEX)
	doc_index = {id: synopsis_ids.index(id) for id in synopsis_ids}
	movies = models.Movie.objects.filter(id__in=doc_index.keys())
	ranked_movies = [0] * len(movies)
	for movie in movies:
		new_index = doc_index[movie.id]
		ranked_movies[new_index] = movie

	paginated_movies = paginate_movies(request, movies)	
	return render(request, "serverapp/index.html", {"movies": paginated_movies})

@require_GET
def show(request, movie_id):
	movie = models.Movie.objects.get(pk=movie_id)
	try:
		storyline_path = os.path.join(settings.STORYLINE, "{0}".format(movie.id))
		storyline = open(storyline_path).read()
	except Exception as e:
		storyline = ""
	try:
		synopsis_path = os.path.join(settings.SYNOPSIS, "{0}".format(movie.id))
		synopsis = open(synopsis_path).read()
	except Exception as e:
		synopsis = ""
	recommendations = RecommendationUnit.get_similar_movies(movie, 1, 1, 1, 1, 1, 1)
	# print "recommendations: ", recommendations
	recommended_movies = []
	for recommendation in recommendations:
		movie_title = models.Movie.objects.get(id=recommendation[0]).title
		new_tuple = (movie_title,) + recommendation
		recommended_movies.append(new_tuple)
	# print "recommended_movies :", recommended_movies

	content = {
		"movie": movie,
		"storyline": storyline,
		"synopsis": synopsis,
		"recommended_movies": recommended_movies[:4],
		"genre_weight": 1,
		"actor_weight": 1,
		"director_weight": 1,
		"storyline_weight": 1,
		"synopsis_weight": 1,
		"feedback_weight": 1,
	}
	return render(request, "serverapp/show.html", content)

@require_GET
def updateRecommendations(request, movie_id):
	movie = models.Movie.objects.get(pk=movie_id)
	print request.GET
	genre_weight = int(request.GET.get("genre"))
	actor_weight = int(request.GET.get("actors"))
	director_weight = int(request.GET.get("director"))
	storyline_weight = int(request.GET.get("storyline"))
	synopsis_weight = int(request.GET.get("synopsis"))
	feedback_weight = int(request.GET.get("feedback"))

	recommendations = RecommendationUnit.get_similar_movies(movie, genre_weight, actor_weight, director_weight, synopsis_weight, storyline_weight, feedback_weight)
	# print "recommendations: ", recommendations
	recommended_movies = []
	for recommendation in recommendations:
		movie_title = models.Movie.objects.get(id=recommendation[0]).title
		new_tuple = (movie_title,) + recommendation
		recommended_movies.append(new_tuple)
	# print "recommended_movies :", recommended_movies

	content = {
		"movie": movie,
		"recommended_movies": recommended_movies[:4],
		"genre_weight": genre_weight,
		"actor_weight": actor_weight,
		"director_weight": director_weight,
		"storyline_weight": storyline_weight,
		"synopsis_weight": synopsis_weight,
		"feedback_weight": feedback_weight,
	}
	return render_to_response('serverapp/recommendation.html', content)

