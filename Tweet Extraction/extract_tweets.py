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

if(not(len(sys.argv) == 3)):
	pass

t = Twarc(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
if(not t):
	pass

with open(sys.argv[1]) as f:
	count = 0
	with open(sys.argv[2], "w") as g:
		for tweet in t.hydrate(f):
			if(tweet["lang"] == "en"):				#Save only english tweets
				g.write(json.dumps(tweet))
				g.write("\n")
				count += 1

				if(count % 5000 == 0):
					print("Retrieved", count, "english tweets..")
		g.close()