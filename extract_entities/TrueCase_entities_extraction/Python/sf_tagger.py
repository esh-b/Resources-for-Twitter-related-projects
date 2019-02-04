from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import csv
import unidecode

from Queue import Queue
from threading import Thread

final_q = Queue(maxsize=0)
entRowsCount = 0

def getEntities(q):
	tknzer = TweetTokenizer()
	st = StanfordNERTagger('./classifiers/english.conll.4class.distsim.crf.ser.gz',
					   'stanford-ner-3.9.1.jar',
					   encoding='utf-8')

	while True:
		row = q.get()
		q.task_done()

		text = row[2]
		tokenized_text = tknzer.tokenize(text)

		#tokenized_text = word_tokenize(text)
		classified_text = st.tag(tokenized_text)

		#Group nearby entities together
		prevEntType = ""
		entsList = []

		for i in range(len(classified_text)):
			Word, Type = classified_text[i][0], classified_text[i][1]
			if(not(Type.decode('utf-8') == 'O')):
				if(prevEntType and Type == prevEntType):
					entsList[-1][0] = entsList[-1][0] + " " + Word
				else:
					entsList.append([Word, Type])
					prevEntType = Type
			else:
				prevEntType = ""

		ents_text = ""	
		if(len(entsList) > 0):
			global entRowsCount
			entRowsCount += 1
			for ent in entsList:
				ents_text += ent[0] + "%$%" + ent[1] + "$$$"
		try:
			row0 = row[0].encode('utf-8')
			row2 = row[2].encode('utf-8')
		except:
			row0 = unidecode.unidecode(row[0].decode("utf-8"))
			row2 = unidecode.unidecode(row[2].decode("utf-8"))
		final_q.put([row0, row2, ents_text])


g = open("chunk_6_stanfordNER.csv", "w")
writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(["Id", "Processed Text", "Entities"])

if(__name__ == "__main__"):
	q = Queue(maxsize=0)
	num_threads = 20

	for i in range(num_threads):
		worker = Thread(target=getEntities, args=(q,))
		worker.setDaemon(True)
		worker.start()

	with open("processedText_chunk_6.csv", 'rb') as f:
		datareader = csv.reader(f)
		next(datareader)
			
		count = 0
		for row in datareader:
			if(not(count == 0) and (count % 100) == 0):
				print(count)
				q.join()
				while(not(final_q.empty())):
					row_write = final_q.get()
					writer.writerow([row_write[0], row_write[1], row_write[2]])
			q.put(row)
			count += 1
	g.close()


