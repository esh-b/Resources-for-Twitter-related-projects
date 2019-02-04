"""
Program to extract noun phrases using the TwitterNLP module
Lang: py2
"""

import csv
import os
import sys
import time
import datetime
import subprocess
from Queue import Queue
from threading import Thread
import threading
import extract_entities as extEnt

BASE_DIR = 'twitter_nlp.jar'

if os.environ.has_key('TWITTER_NLP'):
    BASE_DIR = os.environ['TWITTER_NLP']

sys.path.append('%s/python' % (BASE_DIR))
sys.path.append('%s/python/ner' % (BASE_DIR))
sys.path.append('%s/hbc/python' % (BASE_DIR))

import Features
import twokenize
from LdaFeatures import LdaFeatures
from Dictionaries import Dictionaries
from Vocab import Vocab

sys.path.append('%s/python/cap' % (BASE_DIR))
sys.path.append('%s/python' % (BASE_DIR))
import cap_classifier
import pos_tagger_stdin
import chunk_tagger_stdin
import event_tagger_stdin

lst = []

def GetNer(ner_model, memory="1024m"):
    return subprocess.Popen('java -Xmx%s -cp %s/mallet-2.0.6/lib/mallet-deps.jar:%s/mallet-2.0.6/class cc.mallet.fst.SimpleTaggerStdin --weights sparse --model-file %s/models/ner/%s' % (memory, BASE_DIR, BASE_DIR, BASE_DIR, ner_model),
                           shell=True,
                           close_fds=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)

def GetLLda():
    return subprocess.Popen('%s/hbc/models/LabeledLDA_infer_stdin.out %s/hbc/data/combined.docs.hbc %s/hbc/data/combined.z.hbc 100 100' % (BASE_DIR, BASE_DIR, BASE_DIR),
                           shell=True,
                           close_fds=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
start = ""

def extractEnts_NPs(q):
	posTagger = pos_tagger_stdin.PosTagger()
	chunkTagger = chunk_tagger_stdin.ChunkTagger()
	#eventTagger = event_tagger_stdin.EventTagger()
	llda = GetLLda()
	ner_model = 'ner.model'
	ner = GetNer(ner_model)
	fe = Features.FeatureExtractor('%s/data/dictionaries' % (BASE_DIR))

	capClassifier = cap_classifier.CapClassifier()
	vocab = Vocab('%s/hbc/data/vocab' % (BASE_DIR))

	dictMap = {}
	i = 1
	for line in open('%s/hbc/data/dictionaries' % (BASE_DIR)):
	    dictionary = line.rstrip('\n')
	    dictMap[i] = dictionary
	    i += 1

	dict2index = {}
	for i in dictMap.keys():
	    dict2index[dictMap[i]] = i

	if llda:
	    dictionaries = Dictionaries('%s/data/LabeledLDA_dictionaries3' % (BASE_DIR), dict2index)
	entityMap = {}
	i = 0
	if llda:
	    for line in open('%s/hbc/data/entities' % (BASE_DIR)):
	        entity = line.rstrip('\n')
	        entityMap[entity] = i
	        i += 1

	dict2label = {}
	for line in open('%s/hbc/data/dict-label3' % (BASE_DIR)):
	    (dictionary, label) = line.rstrip('\n').split(' ')
	    dict2label[dictionary] = label

	checkCounts = 0
	global start
	print("Loaded models..Current thread id:", threading.current_thread().getName(), "Time diff:", (datetime.datetime.now() - start))

	while True:
		if(q.qsize() == 0):
			if(checkCounts == 5):
				break

			checkCounts += 1
			time.sleep(0.5)
			continue

		checkCounts = 0

		count, tweet_id, proc_text = q.get()
		if(count % 1000 == 0):
			print("-->", count)
		entsStr, npsStr = extEnt.getEntandNP(proc_text, posTagger, chunkTagger, None, llda, ner_model, ner, fe, capClassifier, vocab,\
			dictMap, dict2index, dictionaries, entityMap, dict2label)
		lst.append([tweet_id, entsStr, npsStr])
		q.task_done()

def writeToFile(writer):
	global lst
	for elem in lst:
		writer.writerow(elem)
	lst = []

if(__name__ == "__main__"):
	q = Queue()
	num_threads = 6

	for i in range(num_threads):
		worker = Thread(target=extractEnts_NPs, args=(q, ))
		#worker.setDaemon(True)
		worker.start()

	chunk_vals = range(15, 24)
	for val in chunk_vals:
		filename = "../8.82Tweets/3.tagMeForEntities/sf_processed_ent_" + str(val) + ".csv"
		start = datetime.datetime.now()
		with open(filename, "rb") as csvfile:
			datareader = csv.reader(csvfile)
			next(datareader)
			count = 0

			print("Processing chunk", val)
			g = open("../8.82Tweets/3_1.TagMe/sf_processed_ent_" + str(val) + "_twitterNLP.csv", "w")
			writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			writer.writerow(["id", "twitter_nlp_ents", "twitter_nlp_np"])

			for row in datareader:
				try:
					q.put((count, row[0], row[2]))
				except Exception as e:
					print(e)
				count += 1
			q.join()

			writeToFile(writer)
			g.close()
		diff = datetime.datetime.now() - start
		print(diff)
