import lucene

from django.apps import AppConfig
from django.conf import settings

class ServerappConfig(AppConfig):
	name = "serverapp"

	def ready(self):
		settings.JVM = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
