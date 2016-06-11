# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from serverapp.lib.searcher import SearchFiles

OPTION_MAP = {
	1: settings.STORYLINE_INDEX,
	2: settings.SYNOPSIS_INDEX
}


class Command(BaseCommand):
	def add_arguments(self, parser):
			parser.add_argument("query", type=str, nargs="+")
			parser.add_argument("option", type=int, nargs="+", help="1:Storyline 2:Synopsis")

	def handle(self, *args, **options):
		query = options["query"]
		query = ' '.join(map(str,query))

		option = int(options["option"][0])
		index_dir = OPTION_MAP[option]

		SearchFiles(query, index_dir)