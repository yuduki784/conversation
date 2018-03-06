#encoding=utf-8

import sys
from extractNoun import ExtractNoun
from gensim import corpora, matutils
import numpy
from fileObject import *
from sklearn.ensemble import RandomForestClassifier

class ChoiseQuestion():
	def __init__(self):
		self.questions = []
		self.data = []
		self.train = []
		self.train_labels = []
		self.label_dic = {}
		self.denses = []

	def readQuestionFile(self, filepath):
		file_obj = FileObj(filepath)
		self.questions = file_obj.read_line()

	def readTrainFile(self, filepath):
		__file_obj = TrainFileObject(filepath, has_colname=False)
		self.train_labels, self.train = __file_obj.readTrainFile()

	def readLabelFile(self, filepath):
		__file_obj = TrainFileObject(filepath, has_colname=False)
		__key, __val = __file_obj.readTrainFile()
		for idx in range(0, len(__key)):
			self.label_dic[__key[idx]] = __val[idx]
	
	def convertFeatherSpace(self, qlist, teststr):
		ext_noun = ExtractNoun()
		nouns = ext_noun.extract(qlist, teststr)

		dictionary = corpora.Dictionary(nouns)

		for noun in nouns:
			vec = dictionary.doc2bow(noun)
			dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
			self.denses.append(dense)



class CQ_CosignSimular(ChoiseQuestion, object):
	def __init__(self, filepath):
		super(CQ_CosignSimular, self).__init__()
		self.readQuestionFile(filepath)

	def __calculateCosignSimilarity(self, vec1, vec2):
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

	def recomendSimilarQuestion(self, teststr=""):
		if len(teststr) > 0:
			self.convertFeatherSpace(self.questions, teststr)

		num_inputstr = len(self.denses)
		max_val = 0.0
		recomend_id = 0
		for idx in range(1, num_inputstr-1):
			sim = self.__calculateCosignSimilarity(self.denses[idx-1], self.denses[num_inputstr-1])
			print("line=[%d] sim=[%f] question=[%s]" % (idx, sim, self.questions[idx-1]))

			if max_val < sim :
				max_val = sim
				recomend_id = idx

		print("Similar Question on line %d : %s" % (recomend_id, self.questions[recomend_id-1]))
		return max_val, self.questions[recomend_id-1]

class CQ_RandomForest(ChoiseQuestion, object):
	def __init__(self, train_filepath, label_filepath):
		super(CQ_RandomForest, self).__init__()
		self.estimator = RandomForestClassifier()
		self.readTrainFile(train_filepath)
		self.readLabelFile(label_filepath)

	def recomendSimilarQuestion(self, teststr=""):
		if len(teststr) > 0:
			self.convertFeatherSpace(self.train, teststr)

		num_inputstr = len(self.denses)

		self.estimator.fit(self.denses[:(num_inputstr - 1)], self.train_labels)

		label_predict = self.estimator.predict([self.denses[num_inputstr - 1],])

		return self.label_dic[label_predict[0]]
