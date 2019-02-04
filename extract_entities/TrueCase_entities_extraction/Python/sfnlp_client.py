"""
Lang: Py3
"""

import requests
import json
import traceback
import sys
import csv
import time
import queue
from threading import Thread

lst = []
NUM_THREADS = 20

def extractEnts(q):
	URL = "http://localhost:1337"
	props={'annotators': 'tokenize, ssplit, truecase, ner, entitylink',
		'parse.model': "edu/stanford/nlp/models/srparser/englishSR.ser.gz",
		'truecase.overwriteText':'true',
		'ner.applyNumericClassifiers': 'false'
	}

	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'properties': props}
	checkCounts = 0
	while True:
		if(q.qsize() == 0):
			if(checkCounts == 5):
				break

			checkCounts += 1
			time.sleep(0.5)
			continue

		checkCounts = 0

		# api-endpoint
		count, tweet_id, text, count = q.get()

		# sending get request and saving the response as response object
		r = requests.post(url=URL, params=PARAMS, data=text)

		#threading.current_thread().name

		# extracting data in json format
		data = ""
		try:
			data = r.json()
			trueText, entsStr = "", ""
			for sent in data['sentences']:
				for ent in sent['entitymentions']:
					word, ner = ent['text'], ent['ner']
					entsStr += word + "#$#" + ner + "$$$"
				for token in sent['tokens']:
					trueText += token['truecaseText'] + " "
		except Exception as e:
			print >> sys.stderr, traceback.format_exc()
			return

		global lst
		lst.append([tweet_id, trueText, entsStr])

		if(count % 5000 == 0):
			print("Extracted entities for", count, "tweets...")
		q.task_done()

def writetoFile(writer):
	global lst
	for i in range(len(lst)):
		writer.writerow([lst[i][0].encode('utf-8'), lst[i][1].encode('utf-8'), lst[i][2].encode('utf-8'), lst[i][3].encode('utf-8'), lst[i][4].encode('utf-8')])
	lst = []

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 2)):
		print("Usage: sfnlp_client.py")
		return

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.csv, then output filename is input_file_spacyNP.csv
	output_filename = input_filepath.split("/")[-1].split(".")[0] + "_sf_truecase_ents.csv"

	q = queue.Queue()

	for i in range(NUM_THREADS):
		worker = Thread(target=extractEnts, args=(q, ))
		#worker.setDaemon(True)
		worker.start()

	with open(input_filepath, "rt") as csvfile:
		datareader = csv.reader(csvfile)
		next(datareader)

		count = 0
		for row in datareader:
			if(len(lst) == 10000):
				q.join()
				writetoFile(writer)
			q.put((count, row[0], row[2], count))
			count += 1
		q.join()

	#Write the extracted entities to csv
	with open(output_filename, "w") as g:
		#Initialize CSV writer object
		writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

		#Write the CSV column names
		writer.writerow(["tweet_id", "processed_text", "true_text", "entities"])

		#Write all the extracted entities to a file
		writeToFile(writer)

	print("Time taken to extract entities for the given dataset:", datetime.datetime.now() - start)