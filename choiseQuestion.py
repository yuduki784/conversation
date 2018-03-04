#encoding=utf-8

import sys
from extractNoun import ExtractNoun
from gensim import corpora, matutils
import numpy
from fileObject import FileObj

class ChoiseQuestion():
	def __init__(self):
		self.questions = []

	def __init__(self, filepath):
		self.readQuestionList(filepath)

	def calculateCosignSimilarity(self, vec1, vec2):
		if len(vec1) != len(vec2):
			print("Warn: Invalid Demension.")
			print("	length vec1=[%s] vec2=[%s]" % (len(vec1), len(vec2)))
			return 0
		norm1 = numpy.linalg.norm(vec1)
		norm2 = numpy.linalg.norm(vec2)
		if (norm1 * norm2 == 0.0):
			return 0
		else:
			return numpy.dot(vec1, vec2)/ (norm1 * norm2)

	def readQuestionList(self, filepath):
		file_obj = FileObj(filepath)
		self.questions = file_obj.read_line()
	
	def convertFeatherSpace(self, teststr):
		ext_noun = ExtractNoun()
		nouns = ext_noun.extract(self.questions, teststr)

		dictionary = corpora.Dictionary(nouns)

		self.denses = []
		for noun in nouns:
			vec = dictionary.doc2bow(noun)
			dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
			self.denses.append(dense)

	def recomendSimilarQuestion(self, teststr=""):
		if len(teststr) > 0:
			self.convertFeatherSpace(teststr)

		num_inputstr = len(self.denses)
		max_val = 0.0
		recomend_id = 0
		for idx in range(1, num_inputstr-1):
			sim = self.calculateCosignSimilarity(self.denses[idx-1], self.denses[num_inputstr-1])
			print("line=[%d] sim=[%f] question=[%s]" % (idx, sim, self.questions[idx-1]))

			if max_val < sim :
				max_val = sim
				recomend_id = idx

		print("Similar Question on line %d : %s" % (recomend_id, self.questions[recomend_id-1]))
		return max_val, self.questions[recomend_id-1]

