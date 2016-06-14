# -*- coding: utf-8 -*-

import scrapy, os, codecs, urllib

from functools import wraps
from django.conf import settings
from django.db import transaction
from serverapp import models
from scrapy.utils.python import get_func_args

def callback_args(f):
    args = get_func_args(f)[2:]
    @wraps(f)
    def wrapper(spider, response):
        return f(spider, response, 
            **{k:response.meta[k] for k in args if k in response.meta})
    return wrapper

class ImdbSpider(scrapy.Spider):
	name = 'imdb'
	start_urls = ['http://www.imdb.com/search/title?genres=comedy&sort=moviemeter,asc&start=401&title_type=feature']
	
	def parse(self, response):
		for href in response.css('.image a::attr(href)'):
			# print href
			full_url = response.urljoin(href.extract())
			# print full_url
			if not full_url.startswith("?genres"):
				yield scrapy.Request(full_url, callback=self.parse_movie)
			else:
				print "genres"
		
	def parse_movie(self, response):
		sel = scrapy.Selector(response)
		try:
			with transaction.atomic():
				crawled_director = response.css('.credit_summary_item span[itemprop=director] a span::text').extract()[0]
				director, created = models.Director.objects.get_or_create(name=crawled_director)
				crawled_title = response.css('h1::text').extract()[0].replace('\u00a0','')
				crawled_year = response.css('#titleYear a::text').extract()[0]
				crawled_rating = response.css('.ratingValue span[itemprop=ratingValue]::text').extract()[0]
				movie, movie_created = models.Movie.objects.get_or_create(
					title=crawled_title,
					year=crawled_year,
					rating=crawled_rating,
					director=director
				)
				if movie_created:
					crawled_genres = response.css('span[itemprop=genre]::text').extract()
					for crawled_genre in crawled_genres:
						genre, created = models.Genre.objects.get_or_create(name=crawled_genre)
						models.MovieGenre.objects.get_or_create(movie=movie, genre=genre)

					crawled_writers = response.css('.credit_summary_item span[itemprop=creator] a span::text').extract()
					for crawled_writer in crawled_writers:
						writer, created = models.Writer.objects.get_or_create(name=crawled_writer)
						models.MovieWriter.objects.get_or_create(movie=movie, writer=writer)

					crawled_actors = response.css('.cast_list td[itemprop=actor] a span::text').extract()
					for crawled_actor in crawled_actors:
						actor, created = models.Actor.objects.get_or_create(name=crawled_actor)
						models.MovieActor.objects.get_or_create(movie=movie, actor=actor)

		except Exception as e:
			print "Error occured: {0}".format(e)
			return

		if movie_created:
			crawled_poster = sel.xpath("//div[@class='poster']/a/img/@src").extract()[0]
			poster_file = os.path.join(settings.POSTERS, u"{0}.jpg".format(movie.id))
			urllib.urlretrieve(crawled_poster, poster_file)

			crawled_storyline = response.css('#titleStoryLine .inline[itemprop=description] p::text').extract()[0].strip()
			storyline_file_path = os.path.join(settings.STORYLINE, "{0}".format(movie.id))
			storyline_file = codecs.open(storyline_file_path, "a", "utf-8")
			storyline_file.write(crawled_storyline)
			storyline_file.close()

			crawled_synopsis_link = sel.xpath("//div[@id='titleStoryLine']//a[contains(text(), 'Plot Synopsis')]/@href").extract()[0]
			full_url = response.urljoin(crawled_synopsis_link)
			yield scrapy.Request(full_url, callback=self.parse_synopsis, meta={'movie_id': movie.id, 'success': "{0} crawled.".format(movie)})

	@callback_args
	def parse_synopsis(self, response, movie_id, success):
		sel = scrapy.Selector(response)
		synopsis_file_path = os.path.join(settings.SYNOPSIS, "{0}".format(movie_id))
		synopsis_file = codecs.open(synopsis_file_path, "a", "utf-8")
		crawled_synopsis_paragraphs = sel.xpath("//*[@id='swiki.2.1']/text()").extract()
		for crawled_synopsis_paragraph in crawled_synopsis_paragraphs:
			synopsis_file.write(crawled_synopsis_paragraph.strip())
		synopsis_file.close()
		print success
		