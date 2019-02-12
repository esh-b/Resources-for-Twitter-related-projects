"""
Part 2 of the tweet preprocessing phase
Lang: py3
"""

import sys
import csv
import spacy
import contractions
from wordseg import segment
from spacy.tokenizer import Tokenizer

def replaceMentions(token, user_mentions):
	username = None
	for user in user_mentions:
		if(user['screen_name'] == token[1:]):
			username = user['name']
			break
	return username

#Tokenizer instructions
def create_tokenizer(nlp):
	prefix_re = spacy.util.compile_prefix_regex(nlp.Defaults.prefixes)
	suffix_tuple = list(nlp.Defaults.suffixes)
	suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)
	infix_tuple = (r'''[~-~]''')
	infix_re = spacy.util.compile_infix_regex(infix_tuple)
	tokenizer = Tokenizer(nlp.vocab,
			rules={},
			prefix_search=prefix_re.search,
			suffix_search=suffix_re.search,
			infix_finditer=infix_re.finditer)
	return tokenizer

nlp = spacy.load("en")
nlp.tokenizer = create_tokenizer(nlp)

OUTPUT_DIR = os.path.join(os.getcwd(), 'part2_output')

CONTR_THRESH = 1e-7
POSS_TAGS = ["SCONJ", "PART", "DET", "CCONJ", "CONJ", "AUX", "ADP", "ADJ", "VERB", "INTJ", "PRON", "ADV"]

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 2)):
		print("Usage: tweet_preprocess_part2.py <PART1_RESULTS_FILEPATH>")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.csv, then output filename is input_file_part2_results.csv
	output_filepath = OUTPUT_DIR + input_filepath.split("/")[-1].split(".")[0] + "_part2_results.csv"

	try:
		g = open(output_filepath, "w")
	except IOError:
		print("Error while creating new file!!!")
		sys.exit()

	writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(["tweet_id", "actual_text", "preprocess_part1_results", "preprocessed_text"])

	with open(input_filepath, "r") as csvfile:
		datareader = csv.reader(csvfile)
		next(datareader)
		count = 0

		for row in datareader:
			#Split the text into words
			text = row[2].split(" ")

			#Fix all the contractions in the text (don't --> do not)
			for i in range(len(text)):
				if("'" in text[i]):
					text[i] = contractions.fix(text[i])
			text = ' '.join(text)

			#Get the POS of all the words in the text
			#NOTE: Spacy splits the symbols even while finding POS (e.g. #hash becomes [[#], [hash])
			doc = nlp(text)
			tags = []
			for token in doc:
				tags.append([token.text, token.pos_])

			#Map tokens to its pos type
			tagList = []
			try:
				for i in range(len(tags)):
					if(tags[i][0] == "#"):
						tags[i + 1][0] = "#" + tags[i + 1][0]
					else:
						tagList.append(tags[i])
			except:
				continue

			#last element (hashtag or usermention in this case) of the sentence has to be removed incase its NOT part of the sentence
			remove_last_elem = False

			#If the last word is either usermention or hashtag and the previous word to it is not a preposition, remove that hashtag or usermention
			if(tagList[len(tagList) - 1][0].startswith("#") or tagList[len(tagList) - 1][0].startswith("@") and tagList[i - 1][1] in POSS_TAGS):
				remove_last_elem = True

			for i in range(len(tagList) - 1, -1, -1):
				if((i == (len(tagList) - 1)) and remove_last_elem):
					pass
				elif(tagList[i][0].startswith("#")):
					#Segment the last hashtag's word if possible (e.g. #DonaldTrump becomes 'Donald<SPACE>Trump')
					#If the confidence of split (res[1]) > CONTR_THRESH, then split the word (like #DonaldTrump becomes 'Donald Trump')
					#If not, do not split the hashtag word (like #DonaldTrump becomes DonaldTrump)
					res = segment(tagList[i][0][1:].lower())
					if(res[1] > CONTR_THRESH):
						tagList[i][0] = ' '.join(res[0])
					else:
						tagList[i][0] = tagList[i][0][1:]
				elif(tagList[i][0].startswith("@")):
					#Replace usermentions with the corresponding username
					text[i] = replaceMentions(text[i], user_mentions)

			#Remove last element incase its not part of the sentence
			if(remove_last_elem):
				del tagList[len(tagList) - 1]

			#Assemble all the words to get the text
			text_pp = ""
			for i in range(len(tagList)):
				text_pp += tagList[i][0] + " "
			text_pp = text_pp[:-1]

			#Write to file
			writer.writerow([row[0], row[1], row[2], text_pp])
			count += 1

			if(count % 5000 == 0):
				print("Part2: Processed", count, "tweets...")
	g.close()
	print("Part2 of preprocessing done....You can see the final preprocessed text under the column 'preprocess_part2_results' in the generated file.")