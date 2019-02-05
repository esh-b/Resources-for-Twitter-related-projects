"""
Program to extract the tweets given the tweet IDs
Lang: py2
"""

import json
import sys
from twarc import Twarc
import twitter_app_config as conf

OUTPUT_DIR = "./output/"

if(__name__ == "__main__"):	
	if(not(len(sys.argv) == 2)):
		print("Usage: extract_tweets.py <INPUT_FILEPATH>")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.txt, then output filename is input_file_tweet_dump.jsonl
	output_filepath = OUTPUT_DIR + input_filepath.split("/")[-1].split(".")[0] + "_tweet_dump.jsonl"

	try:
		t = Twarc(conf.CONSUMER_KEY, conf.CONSUMER_SECRET, conf.ACCESS_TOKEN, conf.ACCESS_TOKEN_SECRET)
	except Exception as e:
		print(e)
		sys.exit()

	with open(input_filepath) as f:
		count = 0
		with open(output_filepath, "w") as g:
			for tweet in t.hydrate(f):
				if(tweet["lang"] == "en"):				#Save only english tweets
					g.write(json.dumps(tweet))
					g.write("\n")
					count += 1

					if(count % 5000 == 0):
						print("Retrieved", count, "english tweets..")