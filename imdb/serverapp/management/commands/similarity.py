# -*- coding: utf-8 -*-

from django.conf import settings
from serverapp.lib.docsimilarity import DocSimilarity
from serverapp.lib.fill_similarities import FindSimilarities
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
		db = FindSimilarities()
		db.fill_similarities()
		print "DB values completed"
		DocSimilarity()
		print "Documents values completed"
