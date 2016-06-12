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

			weighted_score, top_2_fields = RecommendationUnit.find_weighted_similarity_score(similarity, genre_weight=genre_weight, actor_weight=actor_weight, director_weight=director_weight, synopsis_weight=synopsis_weight, storyline_weight=storyline_weight)

			movie_weighted_score_pairs[second_id] = weighted_score

		sorted_weighted_pairs = sorted(movie_weighted_score_pairs.items(), key=lambda i: float(i[1]), reverse=True)
		top_5_pairs = sorted_weighted_pairs[:5]
		return [movie_id for movie_id, _ in top_5_pairs], top_2_fields
		# return top_5_pairs

	@staticmethod
	def find_weighted_similarity_score(similarity, genre_weight=0, actor_weight=0, \
		director_weight=0, synopsis_weight=0, storyline_weight=0):
		genre_score = (similarity.genre * decimal.Decimal(genre_weight)) * decimal.Decimal(0.25)
		actor_score = similarity.actor * decimal.Decimal(actor_weight)
		director_score = similarity.director * decimal.Decimal(director_weight)
		synopsis_score = (similarity.synopsis * decimal.Decimal(synopsis_weight)) * decimal.Decimal(0.25)
		storyline_score = similarity.storyline * decimal.Decimal(storyline_weight)

		field_scores = {'genre': genre_score, 'actor': actor_score, 'director': director_score, 'synopsis': synopsis_score, 'storyline': storyline_score}
		weighted_score = sum(field_scores.values())

		sorted_fields = sorted(field_scores.items(), key=lambda i: float(i[1]), reverse=True)
		top_2_fields = [sorted_fields[0][0], sorted_fields[1][0]]

		return weighted_score, top_2_fields
