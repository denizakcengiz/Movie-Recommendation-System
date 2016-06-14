from serverapp.models import Similarities
from django.db.models import Max
from django.db.models import F, Q

class NormalizeSimilarityFields(object):

	@staticmethod
	def normalize(storyline=True, synopsis=True):
		NormalizeSimilarityFields.normalize_synopsis()

	@staticmethod
	def normalize_synopsis():
		max_synopsis = Similarities.objects.all().aggregate(Max('synopsis'))['synopsis__max']
		max_storyline = Similarities.objects.all().aggregate(Max('storyline'))['storyline__max']
		normalization_factor_synopsis = 1/max_synopsis 
		normalization_factor_storyline = 1/max_storyline 

		Similarities.objects.all().update(synopsis=F("synopsis")*normalization_factor_synopsis, storyline=F("storyline")*normalization_factor_storyline)
		# for similarity in Similarities.objects.all():
		# 	similarity.synopsis *= normalization_factor_synopsis
		# 	similarity.storyline *= normalization_factor_storyline
		# 	similarity.save()