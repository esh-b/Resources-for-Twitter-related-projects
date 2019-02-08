"""
Lang: Py3
"""

import sys
import csv
import time
import spacy
import queue
import random
import datetime
import tagme_API
import tagme_config
from threading import Thread

#List where all results are stored and later written to file
lst = []

#Number of worker threads
NUM_THREADS = 10

#Link probability
LINK_PROB = 0.1

#RHO
RHO = 0.15

OUTPUT_DIR = "./output/"

#Function to extract tagme entities for a given text
def annotateTagme(index, text, key, LINK_PROB, RHO):
	res = tagme_API.extractEnts(text, key, LINK_PROB, RHO)

	if(res == "ERROR"):
		print("TagMe returned error for the text at index:", index,"!!!")
		return

	finalEntsStr = ""
	if(len(res) > 0):
		#Every entity returned is a tuple of type (ENTITY_TITLE, SPOT_NAME - entity name in text, LINK_PROB, RHO, WIKILINK)
		for ent in res:
			if(ent[3] >= RHO):
				finalEntsStr += ent[1] + "#$#" + ent[0] + "#$#" + ent[4] + "$$$"
	return finalEntsStr

#Function executed by all the worker threads
def get_entities(q, LINK_PROB, RHO):
	checkCounts = 0
	while True:
		if(q.qsize() == 0):
			if(checkCounts == 5):
				break

			checkCounts += 1
			time.sleep(0.5)
			continue

		checkCounts = 0

		index, tweet_id, text = q.get()

		#Get the keys from the config file
		keys = tagme_config.tagme_keys

		#Randomly choose one so that we don't query too much per second with single token
		key = random.choice(keys)

		#Get the entity and wikilink in str format
		resStr = annotateTagme(index, text, key, LINK_PROB, RHO)

		#Write the results to list
		global lst
		lst.append([tweet_id, text, resStr])

		if(index > 0 and index % 5000 == 0):
			print("Extracted named entities for", index, "tweets...")
		q.task_done()

#Write all the elements in the list to file
def writeToFile(writer):
	global lst
	for elem in lst:
		writer.writerow(elem)
	lst = []

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 3)):
		print("Usage: extract_tagme_entities.py <INPUT_FILEPATH> <COLUMN_NUMBER_CONTAINING_TEXT>")
		sys.exit()

	if(not(sys.argv[2].isdigit())):
		print("ERROR: The column number must be a digit.")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#Column number of the text
	col_num_text = int(sys.argv[2])

	#If the input file is X/Y/input_file.csv, then output filename is input_file_spacyNP.csv
	output_filepath = OUTPUT_DIR + input_filepath.split("/")[-1].split(".")[0] + "_tagme_ents.csv"

	q = queue.Queue()

	#Initialize the threads
	for i in range(NUM_THREADS):
		worker = Thread(target=get_entities, args=(q, LINK_PROB, RHO))
		#worker.setDaemon(True)
		worker.start()

	start = datetime.datetime.now()
	with open(input_filepath, "rt") as csvfile:
		datareader = csv.reader(csvfile)
		next(datareader)
		count = 0

		for row in datareader:
			q.put((count, row[0], row[col_num_text - 1]))
			count += 1
		print("All items to be processed are in queue..")
		q.join()

	#Write the extracted entities to a csv
	with open(output_filepath, "w") as g:
		#Initialize CSV writer object
		writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

		#Write the CSV column names
		writer.writerow(["tweet_id", "preprocessed_text", "tagme_entities"])

		#Write all the noun_phrases to a file
		writeToFile(writer)

	print("Time taken to extract named entities for the given dataset:", datetime.datetime.now() - start)

