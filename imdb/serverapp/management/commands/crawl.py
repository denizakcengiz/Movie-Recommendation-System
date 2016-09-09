# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.core.management.base import BaseCommand
from scrapy.cmdline import execute

class Command(BaseCommand):
    def handle(self, *args, **options):
        # execute(['scrapy', 'runspider', 'crawler.py', '-s', 'LOG_ENABLED=0'])
        execute(['scrapy', 'runspider', 'crawler.py', '-s', 'LOG_ENABLED=0'])