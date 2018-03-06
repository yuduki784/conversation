#encoding=utf-8
import codecs

class FileObj(object):
	def __init__(self,filepath):
		self.filepath = filepath

	def read_line(self):
		self.sentences = []

		file_obj = codecs.open(self.filepath,'r','utf-8')
		while True:
			line = file_obj.readline()
			line = line.lstrip()
			line = line.rstrip()
			if not line:
				break
			self.sentences.append(line)
		file_obj.close()

		return self.sentences

class TrainFileObject(FileObj):
	def __init__(self, filepath, has_colname=True, dep=':'):
		super(TrainFileObject, self).__init__(filepath)
		self.has_colname = has_colname
		self.dep = dep
		self.labels = []
		self.datas = []

	def readTrainFile(self):
		lines = self.read_line()
		for line in lines:
			items = line.split(self.dep)
			self.labels.append(int(items[0]))
			self.datas.append(items[1])

		return self.labels, self.datas	
	
