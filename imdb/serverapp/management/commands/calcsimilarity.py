# -*- coding: utf-8 -*-

import lucene
from django.conf import settings
from serverapp.lib.docsimilarity import DocSimilarity
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
		DocSimilarity()
