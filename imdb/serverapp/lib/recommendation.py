import operator
from serverapp.models import Movie, Similarities
from django.db.models import Q
import decimal

class RecommendationUnit(object):

	@staticmethod
	def get_similar_movies(movie, genre_weight=0, actor_weight=0, \
		director_weight=0, synopsis_weight=0, storyline_weight=0):

		all_movie_ids = Movie.objects.filter(~Q(id=movie.id)).values_list('id', flat=True)

		movie_weighted_score_pairs = {}

		for second_id in all_movie_ids:

			similarity = Similarities.objects.filter(first_movie=movie.id, second_movie=second_id).first()
			if not similarity:
				similarity = Similarities.objects.get(first_movie=second_id, second_movie=movie.id)

			weighted_score = RecommendationUnit.find_weighted_similarity_score(similarity, genre_weight=genre_weight, actor_weight=actor_weight, director_weight=director_weight, synopsis_weight=synopsis_weight, storyline_weight=storyline_weight)

			movie_weighted_score_pairs[second_id] = weighted_score

		sorted_weighted_pairs = sorted(movie_weighted_score_pairs.items(), key=lambda i: float(i[1]), reverse=True)
		top_5_pairs = sorted_weighted_pairs[:5]
		return [movie_id for movie_id, _ in top_5_pairs]
		# return top_5_pairs

	@staticmethod
	def find_weighted_similarity_score(similarity, genre_weight=0, actor_weight=0, \
		director_weight=0, synopsis_weight=0, storyline_weight=0):

		return (similarity.genre * decimal.Decimal(genre_weight)) + (similarity.actor * decimal.Decimal(actor_weight)) + \
		(similarity.director * decimal.Decimal(director_weight)) + (similarity.synopsis * decimal.Decimal(synopsis_weight)) + \
		(similarity.storyline * decimal.Decimal(storyline_weight))

