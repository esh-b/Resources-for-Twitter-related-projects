"""
Program to filter the metadata of the tweets from the twitter dump and save it in a CSV file
Lang: py2
"""

import json
import csv
import sys

if(__name__ == "__main__"):
	if(not(len(sys.argv) == 2)):
		print("Usage: filter_tweet_metadata.py <TWEET_DUMP_FILEPATH>")
		return

	#Input filepath
	input_filepath = sys.argv[1]

	#If the input file is X/Y/input_file.jsonl, then output filename is input_file_metadata.csv
	output_filename = input_filepath.split("/")[-1].split(".")[0] + "_metadata.csv"

	try:
		g = open(output_filename, "w", encoding="utf-8")
	except IOError:
		print("Error while creating new file!!!")
		return

	#Writer object
	writer = csv.writer(g, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

	#Write the CSV metadata column names to the file
	writer.writerow(["tweet_id", "tweet_date", "tweet_favCount", "tweet_RTCount", "tweet_text", "hashtagsStr", \
					"usermentionsStr(screen_name#$#name)", "urlsStr(url#$#expanded_url)", "hashtags_jsondump", "usermentions_jsondump", "urls_jsondump", \
					"user_id", "user_name", "user_since", "user_utcoffset", "user_description", "user_verified", "user_listedCount", \
					"user_follCount", "user_statusesCount", "user_friendsCount", "user_favoritesCount"])

	#JSON input file
	with open(input_filepath) as f:
		count = 0

		#Every line is a tweet dump (json stored as a string)
		for line in f:
			#Load the json dump of a tweet
			json_line = json.loads(line)

			#Basic tweet details
			tweet_id = json_line['id_str']
			tweet_date = json_line['created_at']
			tweet_favCount = json_line['favorite_count']
			tweet_RTCount = json_line['retweet_count']
			tweet_text = json_line['full_text']

			#User basic details
			user_id = json_line['user']['id_str']
			user_name =  json_line['user']['name']
			user_since = json_line['user']['created_at']
			user_utcoffset = json_line['user']['utc_offset']
			user_desc = json_line['user']['description']

			#Additional user details
			user_verified = json_line['user']['verified']
			user_listedCount = json_line['user']['listed_count']
			user_follCount = json_line['user']['followers_count']
			user_statusesCount = json_line['user']['statuses_count']
			user_friendsCount = json_line['user']['friends_count']
			user_favoritesCount = json_line['user']['favourites_count']

			#Tweet entities
			hashtagsStr, usermentionsStr, urlsStr = "", "", ""

			# Format - hashtag (without hash) delimited by $$$
			for tag in json_line['entities']['hashtags']:
				hashtagsStr += tag['text'] + "$$$"

			# Format - user_name #$# user_screen_name $$$
			for user in json_line['entities']['user_mentions']:
				usermentionsStr += user['screen_name'] + "#$#" + user['name'] + "$$$"

			# Format - url #$# expanded url $$$
			for url in json_line['entities']['urls']:
				urlsStr += url['url'] + "#$#" + url['expanded_url'] + "$$$"

			row = [tweet_id, tweet_date, tweet_favCount, tweet_RTCount, tweet_text, hashtagsStr, usermentionsStr, urlsStr, \
							json.dumps(json_line['entities']['hashtags']), json.dumps(json_line['entities']['user_mentions']), \
							json.dumps(json_line['entities']['urls']), user_id, user_name, user_since, user_utcoffset, user_desc, \
							user_verified, user_listedCount, user_follCount, user_statusesCount, user_friendsCount, user_favoritesCount]
			writer.writerow(row)
			count += 1

			if(count % 5000 == 0):
				print("Filtered the metadata for", count, "tweets...")
	g.close()

