import operator
from serverapp.models import Movie, Similarities
from django.db.models import Q
import decimal

class RecommendationUnit(object):

	@staticmethod
	def get_similar_movies(movie, genre_weight=0, actor_weight=0, \
		director_weight=0, synopsis_weight=0, storyline_weight=0, feedback_weight=0):

		all_movie_ids = Movie.objects.filter(~Q(id=movie.id)).values_list('id', flat=True)

		movie_weighted_score_pairs = {}

		for second_id in all_movie_ids:

			similarity = Similarities.objects.filter(first_movie=movie.id, second_movie=second_id).first()
			if not similarity:
				similarity = Similarities.objects.get(first_movie=second_id, second_movie=movie.id)

			weighted_score = RecommendationUnit.find_weighted_similarity_score(similarity, genre_weight=genre_weight, actor_weight=actor_weight, director_weight=director_weight, synopsis_weight=synopsis_weight, storyline_weight=storyline_weight, feedback_weight=feedback_weight)
			movie_weighted_score_pairs[second_id] = weighted_score

		sorted_weighted_pairs = sorted(movie_weighted_score_pairs.items(), key=lambda i: float(i[1]), reverse=True)
		top_5_pairs = sorted_weighted_pairs[:5]
		
		top_5_moveids = [item[0] for item in top_5_pairs]
		
		movie_field_pairs = []
		for m_id in top_5_moveids:
			second_movie = Movie.objects.get(id=m_id)
			important_field = RecommendationUnit.find_important_fields(movie, second_movie, genre_weight=genre_weight, actor_weight=actor_weight, director_weight=director_weight, synopsis_weight=synopsis_weight, storyline_weight=storyline_weight, feedback_weight=feedback_weight)	
			movie_field_pairs.append((second_movie.id, important_field))

		return movie_field_pairs
		# return top_5_pairs

	@staticmethod
	def find_weighted_similarity_score(similarity, genre_weight=0, actor_weight=0, \
		director_weight=0, synopsis_weight=0, storyline_weight=0, feedback_weight=0):
		genre_score = (similarity.genre * decimal.Decimal(genre_weight)) * decimal.Decimal(0.1)
		actor_score = similarity.actor * decimal.Decimal(actor_weight)
		director_score = similarity.director * decimal.Decimal(director_weight)
		synopsis_score = similarity.synopsis * decimal.Decimal(synopsis_weight)
		storyline_score = similarity.storyline * decimal.Decimal(storyline_weight)
		feedback_score = decimal.Decimal(similarity.click_percentage) * decimal.Decimal(feedback_weight)

		'''
		field_scores = {'genre': genre_score, 'actor': actor_score, 'director': director_score, 'synopsis': synopsis_score, 'storyline': storyline_score, 'feedback': feedback_score}
		weighted_score = sum(field_scores.values())

		sorted_fields = sorted(field_scores.items(), key=lambda i: float(i[1]), reverse=True)
		print(sorted_fields)
		top_3_fields = [sorted_fields[0][0], sorted_fields[1][0], sorted_fields[2][0]]
		'''
		# return weighted_score, top_3_fields
		
		return genre_score + actor_score + director_score + synopsis_score + storyline_score + feedback_score

	@staticmethod
	def find_important_fields(first_movie, second_movie, genre_weight=0, actor_weight=0, \
		director_weight=0, synopsis_weight=0, storyline_weight=0, feedback_weight=0):
		similarity = first_movie.get_similarity_with_movie(second_movie)
		# print('Similarity : ' + str(similarity.id))
		genre_score = (similarity.genre * decimal.Decimal(genre_weight)) * decimal.Decimal(0.25)
		actor_score = similarity.actor * decimal.Decimal(actor_weight)
		director_score = similarity.director * decimal.Decimal(director_weight)
		synopsis_score = (similarity.synopsis * decimal.Decimal(synopsis_weight)) * decimal.Decimal(0.25)
		storyline_score = similarity.storyline * decimal.Decimal(storyline_weight)
		feedback_score = decimal.Decimal(similarity.click_percentage) * decimal.Decimal(feedback_weight)
		# print('Feedback : ' + str(feedback_score))
		field_scores = {'genre': genre_score, 'actor': actor_score, 'director': director_score, 'synopsis': synopsis_score, 'storyline': storyline_score, 'feedback': feedback_score}
		sorted_fields = sorted(field_scores.items(), key=lambda i: float(i[1]), reverse=True)
		# print(sorted_fields)
		most_important_field = sorted_fields[0][0]

		return most_important_field
