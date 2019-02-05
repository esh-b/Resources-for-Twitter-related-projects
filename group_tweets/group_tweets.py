"""
Program to group the extracted tweets (from Tweet IDs) based on the number of hashtags
Lang: py2
"""

import sys
import json

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 2)):
		print("Usage: group_tweets.py <TWEET_DUMP_FILEPATH>")
		sys.exit()

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.jsonl, then output filename is input_file_<X>h.jsonl
	#Output filename for tweets containing 1 hashtag
	output_0h_filename = input_filepath.split("/")[-1].split(".")[0] + "_0h.jsonl"

	#Output filename for tweets containing 1 hashtag
	output_1h_filename = input_filepath.split("/")[-1].split(".")[0] + "_1h.jsonl"

	#Output filename for tweets containing 2, 3 or 4 hashtags
	output_234h_filename = input_filepath.split("/")[-1].split(".")[0] + "_234h.jsonl"

	#Output filename for tweets containing >=5 hashtags
	output_other_filename = input_filepath.split("/")[-1].split(".")[0] + "_other.jsonl"

	try:
		fp_0h = open(output_0h_filename, "w")
		fp_1h = open(output_1h_filename, "w")
		fp_234h = open(output_234h_filename, "w")
		fp_other = open(output_other_filename, "w")
	except IOError:
		print("Error while creating new files!!!")
		sys.exit()

#./getTweets/news_outlets.jsonl
with open(input_filepath) as f:
	for line in f:
		tweet_json = json.loads(line)
		tags = tweet_json['entities']['hashtags']
		tags_len = len(tags)
		if(tags_len == 0):
			fp_0h.write(line)
			fp_0h.write("\n")
		elif(tags_len == 1):
			fp_1h.write(line)
			fp_1h.write("\n")
		elif(tags_len >= 2 and tags_len <= 4):
			fp_234h.write(line)
			fp_234h.write("\n")
		else:
			fp_other.write(line)
			fp_other.write("\n")

fp_0h.close()
fp_1h.close()
fp_234h.close()
fp_other.close()