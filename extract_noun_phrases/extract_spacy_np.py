"""
Program to extract noun phrases for the given text dataset using Spacy module
Lang: py2
"""

import csv
import time
import datetime
import spacy
from Queue import Queue
from threading import Thread

nlp = spacy.load("en")

#Number of threads processing the data on the queue
NUM_THREADS = 20

lst = []

def get_noun_phrases(q):
	checkCounts = 0
	while True:
		#Incase the queue size is 0, the thread will sleep for 5 * 0.5s (2.5s in total) after which they will quit
		if(q.qsize() == 0):
			if(checkCounts == 5):
				break

			checkCounts += 1
			time.sleep(0.5)
			continue

		checkCounts = 0

		index, tweet_id, text = q.get()
		np_text = ""

		#Extract the noun phrase using spacy
		doc = nlp(text.decode('utf-8'))

		#All the noun phrases of given text are separated by "$$$"
		for np in doc.noun_chunks:
			np_text += np.text + "$$$"

		#Add the extracted noun phrases to the list
		global lst
		lst.append([tweet_id, np_text])

		#Print the status for every 5000 processed tweets
		if(index % 5000 == 0):
			print("Extracted noun phrases for", index, "tweets...")
		q.task_done()

#Method to write the extracted noun phrases to file
def writeToFile(writer):
	global lst
	for elem in lst:
		writer.writerow(elem)
	lst = []

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 3)):
		print("Usage: extract_spacy_np.py <INPUT_FILEPATH> <COLUMN_NUMBER_CONTAINING_TEXT>")
		return

	if(not(sys.argv[2].isdigit())):
		print("ERROR: The column number must be a digit.")
		return

	#Input filepath
	input_filename = sys.argv[1]

	#Column number of the text
	col_num_text = int(sys.argv[2])

	#If the input file is X/Y/input_file.csv, then output filename is input_file_spacyNP.csv
	output_filename = output_filename = input_filepath.split("/")[-1].split(".")[0] + "_spacyNP.csv"

	#Initialize the queue
	q = Queue()

	for i in range(NUM_THREADS):
		#Create NUM_THREADS thread workers
		worker = Thread(target=get_noun_phrases, args=(q,))

		#worker.setDaemon(True)
		worker.start()


	start = datetime.datetime.now()
	with open(input_filename, "rt") as csvfile:
		datareader = csv.reader(csvfile)
		next(datareader)
		count = 0

		for row in datareader:
			q.put((count, row[0], row[col_num_text]))
			count += 1
		print("All items to be processed are in queue...")
		q.join()

	#Write the extracted noun phrases to a csv
	with open(output_filename, "w") as g:
		#Initialize CSV writer object
		writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

		#Write the CSV column names
		writer.writerow(["tweet_id", "spacy_np"])

		#Write all the noun_phrases to a file
		writeToFile(writer)

	print("Time taken to extract noun phrases for the given dataset:", datetime.datetime.now() - start)
