# -*- coding: utf-8 -*-

import lucene
from django.conf import settings
from serverapp.lib.indexer import IndexFiles
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
		# lucene.initVM(vmargs=['-Djava.awt.headless=true'])
		IndexFiles(settings.STORYLINE, settings.STORYLINE_INDEX)
		IndexFiles(settings.SYNOPSIS, settings.SYNOPSIS_INDEX)

