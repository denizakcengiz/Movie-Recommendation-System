from serverapp.models import Movie, Similarities
import itertools

class FindSimilarities():

	def fill_similarities(self):

		all_movie_ids = Movie.objects.values_list('id', flat=True)
		all_movie_ids = all_movie_ids[:5]
		two_combinations = list(itertools.combinations(all_movie_ids, 2))

		for first_movie_id, second_movie_id in two_combinations:
			print('\n\n\n\nNew Movie Pair')
			print('id1: ' + str(first_movie_id))
			print('id2: ' + str(second_movie_id))
			first_movie = Movie.objects.get(id=first_movie_id)
			second_movie = Movie.objects.get(id=second_movie_id)
			similar_movies = Similarities()
			similar_movies.first_movie = first_movie
			similar_movies.second_movie = second_movie
			similar_movies.genre = self.findGenreSimilarity(first_movie, second_movie)
			similar_movies.actor = self.findActorSimilarity(first_movie, second_movie)
			similar_movies.director = self.findDirectorSimilarity(first_movie, second_movie)

			first_movie_genres = [str(genre) for genre in first_movie.genres.all()]
			second_movie_genres = [str(genre) for genre in second_movie.genres.all()]
			
			first_movie_actors = [str(actor) for actor in first_movie.actors.all()]
			second_movie_actors = [str(actor) for actor in second_movie.actors.all()]
			print('Movie %s %s: ' % (first_movie.id, second_movie.id))
			print('Genre: %s %s %f' % (first_movie_genres, second_movie_genres, similar_movies.genre))
			print('Actor: %s %s %f' % (first_movie_actors, second_movie_actors, similar_movies.actor))
			print('Director: %s %s %d' % (first_movie.director_id, second_movie.director_id, similar_movies.director))	


	def findGenreSimilarity(self, first_movie, second_movie):

		first_movies_genres = [str(genre) for genre in first_movie.genres.all()]
		second_movies_genres = [str(genre) for genre in second_movie.genres.all()]
		intersection_of_genres = set(first_movies_genres).intersection(second_movies_genres)
		union_of_genres = set(first_movies_genres).union(second_movies_genres)
		return float(len(intersection_of_genres))/len(union_of_genres)

	def findActorSimilarity(self, first_movie, second_movie):

		first_movies_actors = [str(actor) for actor in first_movie.actors.all()]
		second_movies_actors = [str(actor) for actor in second_movie.actors.all()]
		intersection_of_actors = set(first_movies_actors).intersection(second_movies_actors)
		union_of_actors = set(first_movies_actors).union(second_movies_actors)
		return float(len(intersection_of_actors))/len(union_of_actors)		
	
	def findDirectorSimilarity(self, first_movie, second_movie):

		return 1 if first_movie.director_id == second_movie.director_id else 0
		

