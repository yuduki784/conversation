# coding=utf-8

import MeCab
import sys
import codecs
from fileObject import FileObj


class ExtractNoun():
	def __init__(self):
		self.mecab = MeCab.Tagger("mecabrc")

	def get_nouns(self,node):
		nouns = []
		while node:
			if node.feature.split(',')[0].decode('utf-8') == u'名詞':
				nouns.append(node.surface)
			node = node.next

		return nouns


	def extract(self,sentences,inputtext):
		nouns = []
		for sentence in sentences:
			node = self.mecab.parseToNode(sentence.encode('utf-8'))
			nouns.append(self.get_nouns(node))

		node = self.mecab.parseToNode(inputtext)
		nouns.append(self.get_nouns(node))

		return nouns
			
