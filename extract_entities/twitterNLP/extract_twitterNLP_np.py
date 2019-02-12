"""
Program to extract noun phrases and named entities using the TwitterNLP module
Lang: py3
"""

import csv
import os
import sys
import time
import datetime
import subprocess
from queue import Queue
from threading import Thread
import threading

OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
BASE_DIR = os.path.join(os.getcwd(), 'twitter_nlp')
NUM_THREADS = 6
lst = []

if 'TWITTER_NLP' in os.environ:
    BASE_DIR = os.environ['TWITTER_NLP']

sys.path.append('%s/python' % (BASE_DIR))
sys.path.append('%s/python/ner' % (BASE_DIR))
sys.path.append('%s/python/pos_tag' % (BASE_DIR))
sys.path.append('%s/hbc/python' % (BASE_DIR))

import extractEntities as extEnt
import Features
from Dictionaries import Dictionaries
from Vocab import Vocab

sys.path.append('%s/python/cap' % (BASE_DIR))
sys.path.append('%s/python' % (BASE_DIR))
import cap_classifier
import pos_tagger_stdin
import chunk_tagger_stdin
import event_tagger_stdin

def GetNer(ner_model, memory="1024m"):
    return subprocess.Popen('java -Xmx%s -cp %s/mallet-2.0.6/lib/mallet-deps.jar:%s/mallet-2.0.6/class cc.mallet.fst.SimpleTaggerStdin --weights sparse --model-file %s/models/ner/%s' % (memory, BASE_DIR, BASE_DIR, BASE_DIR, ner_model),
                           shell=True,
                           close_fds=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           bufsize=1,
                           universal_newlines=True)

def GetLLda():
    return subprocess.Popen('%s/hbc/models/LabeledLDA_infer_stdin.out %s/hbc/data/combined.docs.hbc %s/hbc/data/combined.z.hbc 100 100' % (BASE_DIR, BASE_DIR, BASE_DIR),
                           shell=True,
                           close_fds=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           bufsize=1,
                           universal_newlines=True)
start = None

def extract_np_and_entities(q):
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
	#print("Loaded models..Current thread id:", threading.current_thread().getName(), "Time diff:", (datetime.datetime.now() - start))

	while True:
		if(q.qsize() == 0):
			if(checkCounts == 5):
				break

			checkCounts += 1
			time.sleep(0.5)
			continue

		checkCounts = 0

		count, tweet_id, text = q.get()
		entsStr, npsStr = extEnt.getEntandNP(text, posTagger, chunkTagger, None, llda, ner_model, ner, fe, capClassifier, vocab,\
			dictMap, dict2index, dictionaries, entityMap, dict2label)
		lst.append([tweet_id, entsStr, npsStr])

		if(count > 0 and count % 1000 == 0):
			print("Processed", count, "tweets...")
		q.task_done()

#Function to write the extracted noun phrases and named entities to file
def writeToFile(writer):
	global lst
	for elem in lst:
		writer.writerow(elem)
	lst = []

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 3)):
		print("Usage: extract_twitterNLP_np_entities.py <INPUT_FILEPATH> <COLUMN_NUMBER_CONTAINING_TEXT>")
		sys.exit()

	if(not(sys.argv[2].isdigit())):
		print("ERROR: The column number must be a digit.")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#Column number of the text
	col_num_text = int(sys.argv[2])

	#If the input file is X/Y/input_file.csv, then output filename is input_file_spacyNP.csv
	output_filepath = OUTPUT_DIR + input_filepath.split("/")[-1].split(".")[0] + "_twitterNLP.csv"

	#Initialize the queue
	q = Queue()

	for i in range(NUM_THREADS):
		worker = Thread(target=extract_np_and_entities, args=(q, ))
		#worker.setDaemon(True)
		worker.start()

	start = datetime.datetime.now()
	with open(input_filepath, "r") as csvfile:
		datareader = csv.reader(csvfile)
		next(datareader)
		count = 0

		for row in datareader:
			try:
				q.put((count, row[0], row[2]))
			except Exception as e:
				print(e)
			count += 1
		print("All items to be processed are in queue...")
		q.join()

	#Write the extracted noun phrases to a csv
	with open(output_filepath, "w") as g:
		#Initialize CSV writer object
		writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

		#Write the CSV column names
		writer.writerow(["tweet_id", "twitterNLP_ents", "twitterNLP_np"])

		#Write all the noun_phrases to a file
		writeToFile(writer)

	print("Time taken to extract noun phrases and named entities for the given dataset:", datetime.datetime.now() - start)
