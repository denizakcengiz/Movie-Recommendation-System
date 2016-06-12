# -*- coding: utf-8 -*-

from django.db import models

class Writer(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return u"{0}".format(self.name)

class Actor(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return u"{0}".format(self.name)

class Director(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return u"{0}".format(self.name)

class Genre(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return u"{0}".format(self.name)
	
class Movie(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	year = models.CharField(max_length=4)
	director = models.ForeignKey(Director)

	writers = models.ManyToManyField(Writer, through="MovieWriter")
	genres = models.ManyToManyField(Genre, through="MovieGenre")
	actors = models.ManyToManyField(Actor, through="MovieActor")

	class Meta:
		unique_together = ("title", "year")

	def __unicode__(self):
		return u"{0} ({1})".format(self.title, self.year)


class MovieWriter(models.Model):
	id = models.AutoField(primary_key=True)
	movie = models.ForeignKey(Movie)
	writer = models.ForeignKey(Writer)

	class Meta:
		unique_together = ("movie", "writer")

	def __unicode__(self):
		return u"Movie: {0} Writer: {1}".format(self.movie.title, self.writer.name)

class MovieGenre(models.Model):
	id = models.AutoField(primary_key=True)
	movie = models.ForeignKey(Movie)
	genre = models.ForeignKey(Genre)

	class Meta:
		unique_together = ("movie", "genre")

	def __unicode__(self):
		return u"Movie: {0} Genre: {1}".format(self.movie.title, self.genre.name)

class MovieActor(models.Model):
	id = models.AutoField(primary_key=True)
	movie = models.ForeignKey(Movie)
	actor = models.ForeignKey(Actor)

	class Meta:
		unique_together = ("movie", "actor")

	def __unicode__(self):
		return u"Movie: {0} Actor: {1}".format(self.movie.title, self.actor.name)

class Similarities(models.Model):
	id = models.AutoField(primary_key=True)
	first_movie = models.ForeignKey(Movie, related_name='+')
	second_movie = models.ForeignKey(Movie, related_name='+')
	genre = models.DecimalField(max_digits=5, decimal_places=4, default=0)
	actor = models.DecimalField(max_digits=5, decimal_places=4, default=0)
	director = models.DecimalField(max_digits=5, decimal_places=4, default=0)
	synopsis = models.DecimalField(max_digits=5, decimal_places=4, default=0)
	storyline = models.DecimalField(max_digits=5, decimal_places=4, default=0)

	class Meta:
		unique_together = ("first_movie", "second_movie")

	def __unicode__(self):
		return u"Movie1: {0} Movie2: {1}".format(self.movie1.title, self.movie2.title)





