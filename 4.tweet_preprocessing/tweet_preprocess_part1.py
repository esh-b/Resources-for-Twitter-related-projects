"""
Part 1 of the tweet preprocessing phase
Lang: py3
"""

import json
import re
import csv
import sys

OUTPUT_DIR = os.path.join(os.getcwd(), 'part1_output')

EMOJI_PATTERN = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
URL_PATTERN = re.compile('http\S+')

#Method to replace usermentions with actual username
def replaceMentions(token, user_mentions):
	username = None
	for user in user_mentions:
		if(user['screen_name'] == token[1:]):
			username = user['name']
			break
	return username

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 2)):
		print("Usage: tweet_preprocess_part1.py <TWEET_DUMP_FILEPATH>")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.csv, then output filename is input_file_spacyNP.csv
	output_filepath = OUTPUT_DIR + input_filepath.split("/")[-1].split(".")[0] + "_part1_results.csv"

	try:
		g = open(output_filepath, "w")
	except IOError:
		print("Error while creating new file!!!")
		sys.exit()

	writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(["tweet_id", "actual_text", "preprocess_part1_results"])


	#with open("news_outlets_234h.jsonl") as f:
	with open(input_filepath) as f:
		count = 0
		for line in f:
			#Load the tweet info from the tweet dump
			json_line = json.loads(line)

			#Get the tweet full_text
			text = json_line['full_text']

			#Replace all the newlines with spaces
			text = text.replace("\n", ' ')

			#Remove all the emojis from the tweet
			text = EMOJI_PATTERN.sub('', text)

			#Remove all the URLs from the tweet
			text = URL_PATTERN.sub('', text)

			#Split the text into words (filter removes the empty strings after split)
			text = list(filter(None, text.split(" ")))

			#Get all the usermentions in the tweet which are then replaced by the actual username
			user_mentions = json_line['entities']['user_mentions']

			#If the last word in the tweet starts with #, then lastPP is True
			if(text[len(text) - 1].startswith("#") or text[len(text) - 1].startswith("@")):
				lastPP = True
			else:
				lastPP = False

			#Check:  If tweet is just "#something"
			#Iterate from the last word till the first word of the tweet
			for i in range(len(text) - 1, 0, -1):
				if(text[i].startswith("@") or text[i].startswith("#") and lastPP):
					if(text[i - 1].startswith(("#", "@"))):
						text[i] = ""
					else:
						lastPP = False

			#Remove all the empty strings (incase any) obtained from the previous loop
			text = filter(None, text)

			#Join the words of the text
			text = ' '.join(text)

			#Write to file
			writer.writerow([json_line["id_str"], json_line['full_text'], text])
			count += 1

			if(count % 5000 == 0):
				print("Part1: Processed", count, "tweets...")
	g.close()
	print("Part1 of preprocessing done....you can now run the part2 code to further preprocess your tweet text.")
