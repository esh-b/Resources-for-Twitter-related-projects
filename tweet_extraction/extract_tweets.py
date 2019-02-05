"""
Program to extract the tweets given the tweet IDs
Lang: py3
"""

from twarc import Twarc
import json
import sys

#Twarc credentials
CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_TOKEN=""
ACCESS_TOKEN_SECRET=""

if(__name__ == "__main__"):	
	if(not(len(sys.argv) == 3)):
		print("Usage: extract_tweets.py <INPUT_FILEPATH>")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.txt, then output filename is input_file_tweet_dump.jsonl
	output_filename = input_filepath.split("/")[-1].split(".")[0] + "_tweet_dump.jsonl"

	try:
		t = Twarc(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	except Exception as e:
		print(e)
		sys.exit()

	with open(input_filepath) as f:
		count = 0
		with open(output_filename, "w") as g:
			for tweet in t.hydrate(f):
				if(tweet["lang"] == "en"):				#Save only english tweets
					g.write(json.dumps(tweet))
					g.write("\n")
					count += 1

					if(count % 5000 == 0):
						print("Retrieved", count, "english tweets..")