"""
"""
import requests
import json
import traceback
import sys

WIKIPEDIA_URI_BASE = u"https://{}.wikipedia.org/wiki/{}"

#Convert wiki title to page link
def normalize_title(title):
    title = title.strip().replace(" ", "_")
    return title[0].upper() + title[1:]

def extractEnts(text, key, lp, rho):
	# api-endpoint
	URL = "https://tagme.d4science.org/tagme/tag"

	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'gcube-token': key,
				'text': text,
				'lang': 'en'
	}

	# sending get request and saving the response as response object
	r = requests.get(url=URL, params=PARAMS)

	# extracting data in json format
	data = ""
	try:
		data = r.json()
	except Exception as e:
		print("--->", e)
		print >> sys.stderr, traceback.format_exc()
		return "ERROR"

	ents = []
	try:
		spots = data['annotations']
		for spot in spots:
			#Ignore the entity if it doesn't have title (Title of the wikipage for the entity)
			if(not('title' in spot)):
				continue

			#Title of the wikipage for the entity
			title = spot['title']
			rho = spot['rho']
			spot_name = spot['spot']
			
			#categ = spot['dbpedia_categories']
			#prim_categ = categ[0]

			#Get the wikipedia link for the entity
			wikiLink = WIKIPEDIA_URI_BASE.format("en", normalize_title(title))
			link_prob = spot['link_probability']

			if(link_prob > lp):
				ents.append((title, spot_name, link_prob, spot['rho'], wikiLink))
	except Exception as e:
		print >> sys.stderr, traceback.format_exc()
		return "ERROR"
	return ents