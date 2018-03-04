#encoding=utf-8

from choiseQuestion import ChoiseQuestion 
import sys

cq = ChoiseQuestion(sys.argv[1])
sim, question = cq.recomendSimilarQuestion(sys.argv[2])

print("sim=[%f] question=[%s]" % (sim,question))
