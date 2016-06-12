# -*- coding: utf-8 -*-

import sys, os, lucene

from string import Template
from datetime import datetime
from getopt import getopt, GetoptError

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from django.conf import settings
from serverapp import models

FIELD_CONTENTS = "contents"
FIELD_PATH = "name"

class DocSimilarity(object):
    def __init__(self, query, index_dir):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        self.similarityOfSynopsis()
        self.similarityOfStoryLine()

    def similarityOfSynopsis(self):
        # Get handle to index directory
        directory = SimpleFSDirectory(File(settings.SYNOPSIS_INDEX))

        # Creates a searcher searching the provided index.
        ireader  = DirectoryReader.open(directory)

        # Implements search over a single IndexReader.
        # Use a single instance and use it across queries
        # to improve performance.
        searcher = IndexSearcher(ireader)

        # Get the analyzer
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

        # Constructs a query parser. We specify what field to search into.
        queryParser = QueryParser(Version.LUCENE_CURRENT, FIELD_CONTENTS, analyzer)
        for root, dirnames, filenames in os.walk(settings.SYNOPSIS):
            for filename in filenames:
                path = os.path.join(root, filename)
                major_movie = models.Movie.objects.get(pk=filename)
                with open(path, 'r') as moviedoc:
                    content = moviedoc.read().replace('\n', ' ')
                    query = queryParser.parse(content)
                    topDocs = searcher.search(query, len(filenames))
                    scoreDocs = topDocs.scoreDocs

                    for scoreDoc in scoreDocs:
                        doc = searcher.doc(scoreDoc.doc)
                        movie_id = doc.get(FIELD_PATH)
                        minor_movie = models.Movie.objects.get(pk=movie_id)
                        similarity = models.Similarities.objects.get(first_movie=major_movie, second_movie=minor_movie)
                        similarity.synopsis = scoreDoc.score
                        similarity.save()

    def similarityOfStoryLine(self):
        # Get handle to index directory
        directory = SimpleFSDirectory(File(settings.STORYLINE_INDEX))

        # Creates a searcher searching the provided index.
        ireader  = DirectoryReader.open(directory)

        # Implements search over a single IndexReader.
        # Use a single instance and use it across queries
        # to improve performance.
        searcher = IndexSearcher(ireader)

        # Get the analyzer
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

        # Constructs a query parser. We specify what field to search into.
        queryParser = QueryParser(Version.LUCENE_CURRENT, FIELD_CONTENTS, analyzer)
        for root, dirnames, filenames in os.walk(settings.STORYLINE):
            for filename in filenames:
                path = os.path.join(root, filename)
                major_movie = models.Movie.objects.get(pk=filename)
                with open(path, 'r') as moviedoc:
                    content = moviedoc.read().replace('\n', ' ')
                    query = queryParser.parse(content)
                    topDocs = searcher.search(query, len(filenames))
                    scoreDocs = topDocs.scoreDocs

                    for scoreDoc in scoreDocs:
                        doc = searcher.doc(scoreDoc.doc)
                        movie_id = doc.get(FIELD_PATH)
                        if movie_id == movie.id:
                            continue
                        minor_movie = models.Movie.objects.get(pk=movie_id)
                        similarity = models.Similarities.objects.get(first_movie=major_movie, second_movie=minor_movie)
                        similarity.storyline = scoreDoc.score
                        similarity.save()