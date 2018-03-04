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
			print (line)
		file_obj.close()

		return self.sentences

