# -*- coding: utf-8 -*-

import sys, os, lucene, re

from string import Template
from datetime import datetime
from getopt import getopt, GetoptError

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from django.conf import settings
from serverapp import models

FIELD_CONTENTS = "contents"
FIELD_PATH = "name"

class DocSimilarity(object):
    def __init__(self):
        # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        self.boolean_query = BooleanQuery()
        self.similarityOfSynopsis()
        self.similarityOfStoryLine()

    def similarityOfSynopsis(self):
        directory = SimpleFSDirectory(File(settings.SYNOPSIS_INDEX))
        ireader  = DirectoryReader.open(directory)
        searcher = IndexSearcher(ireader)
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        queryParser = QueryParser(Version.LUCENE_CURRENT, FIELD_CONTENTS, analyzer)
        for root, dirnames, filenames in os.walk(settings.SYNOPSIS):
            filenames = [int(item) for item in filenames]
            filenames.sort()
            filenames = [str(item) for item in filenames]
            for filename in filenames:
                path = os.path.join(root, filename)
                major_movie = models.Movie.objects.get(pk=filename)
                with open(path, 'r') as moviedoc:
                    content = moviedoc.read().replace('\n', ' ')
                    content = re.sub('[^A-Za-z0-9 ]+', '', content)
                    while True:
                        try:
                            query = queryParser.parse(QueryParser.escape(content))
                        except Exception as e:
                            self.boolean_query.setMaxClauseCount(self.boolean_query.maxClauseCount * 2)
                            print self.boolean_query.maxClauseCount
                            continue
                        break

                    topDocs = searcher.search(query, len(filenames))
                    scoreDocs = topDocs.scoreDocs
                    for scoreDoc in scoreDocs:
                        doc = searcher.doc(scoreDoc.doc)
                        movie_id = int(doc.get(FIELD_PATH))
                        if movie_id <= major_movie.id:
                            continue
                        minor_movie = models.Movie.objects.get(pk=movie_id)
                        try:
                            similarity = models.Similarities.objects.filter(first_movie=major_movie, second_movie=minor_movie).first()
                            if not similarity:
                                similarity = models.Similarities.objects.filter(first_movie=minor_movie, second_movie=major_movie).first()
                            similarity.synopsis = scoreDoc.score
                            similarity.save()
                        except Exception as e:
                            print major_movie.id, minor_movie.id
                            raise e
                print u"{0} completed.".format(major_movie.id)

    def similarityOfStoryLine(self):
        directory = SimpleFSDirectory(File(settings.STORYLINE_INDEX))
        ireader  = DirectoryReader.open(directory)
        searcher = IndexSearcher(ireader)
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        queryParser = QueryParser(Version.LUCENE_CURRENT, FIELD_CONTENTS, analyzer)
        for root, dirnames, filenames in os.walk(settings.STORYLINE):
            filenames = [int(item) for item in filenames]
            filenames.sort()
            filenames = [str(item) for item in filenames]
            for filename in filenames:
                path = os.path.join(root, filename)
                major_movie = models.Movie.objects.get(pk=filename)
                with open(path, 'r') as moviedoc:
                    content = moviedoc.read().replace('\n', ' ')
                    content = re.sub('[^A-Za-z0-9 ]+', '', content)
                    query = queryParser.parse(QueryParser.escape(content))
                    topDocs = searcher.search(query, len(filenames))
                    scoreDocs = topDocs.scoreDocs

                    for scoreDoc in scoreDocs:
                        doc = searcher.doc(scoreDoc.doc)
                        movie_id = int(doc.get(FIELD_PATH))
                        if movie_id <= major_movie.id:
                            continue
                        minor_movie = models.Movie.objects.get(pk=movie_id)
                        try:
                            similarity = models.Similarities.objects.filter(first_movie=major_movie, second_movie=minor_movie).first()
                            if not similarity:
                                similarity = models.Similarities.objects.filter(first_movie=minor_movie, second_movie=major_movie).first()
                            similarity.storyline = scoreDoc.score
                            similarity.save()
                        except Exception as e:
                            print major_movie.id, minor_movie.id
                            raise e
                print u"{0} completed.".format(major_movie.id)