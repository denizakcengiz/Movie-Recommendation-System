from serverapp.models import Similarities
from django.db.models import Max

class NormalizeSimilarityFields(object):

	@staticmethod
	def normalize(storyline=True, synopsis=True):
		if synopsis:
			NormalizeSimilarityFields.normalize_synopsis()
		if storyline:
			NormalizeSimilarityFields.normalize_storyline()

	@staticmethod
	def normalize_synopsis():
		max_synopsis = Similarities.objects.all().aggregate(Max('synopsis'))['synopsis__max']
		normalization_factor = 1/max_synopsis 

		for similarity in Similarities.objects.all():
			similarity.synopsis *= normalization_factor
			similarity.save()

	@staticmethod
	def normalize_storyline():
		max_storyline = Similarities.objects.all().aggregate(Max('storyline'))['storyline__max']
		normalization_factor = 1/max_storyline 

		for similarity in Similarities.objects.all():
			similarity.storyline *= normalization_factor
			similarity.save()		