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


FIELD_CONTENTS = "contents"
FIELD_PATH = "name"

class SearchFiles(object):
	def __init__(self, query, index_dir):
		self.search(query, index_dir)

	def search(self, query, index_dir):
		lucene.initVM(vmargs=['-Djava.awt.headless=true'])

		# Get handle to index directory
		directory = SimpleFSDirectory(File(index_dir))

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

		# Create the query
		query = queryParser.parse(query)

		# Run the query and get top 50 results
		topDocs = searcher.search(query, 5)

		# Get top hits
		scoreDocs = topDocs.scoreDocs
		print "%s total matching documents." % len(scoreDocs)

		for scoreDoc in scoreDocs:
			doc = searcher.doc(scoreDoc.doc)
			print doc.get(FIELD_PATH)