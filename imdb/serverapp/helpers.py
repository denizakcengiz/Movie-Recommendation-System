from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

NUM_OF_MOVIE_IN_PAGE = 9


def paginate_movies(request, movies):

	showed_movies = []
	paginator = Paginator(movies, NUM_OF_MOVIE_IN_PAGE)
	page = request.GET.get('page')
	
	try:
		showed_movies = paginator.page(page)
	except PageNotAnInteger:
		showed_movies = paginator.page(1)
	except EmptyPage:
		showed_movies = paginator.page(paginator.num_pages)

	return showed_movies