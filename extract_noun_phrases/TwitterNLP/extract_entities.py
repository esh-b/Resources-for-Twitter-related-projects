#!/usr/bin/python

import sys
import os
import re
import subprocess
import time
import csv
import datetime
from signal import *

import argparse

BASE_DIR = 'twitter_nlp.jar'

if os.environ.has_key('TWITTER_NLP'):
    BASE_DIR = os.environ['TWITTER_NLP']

sys.path.append('%s/python' % (BASE_DIR))
sys.path.append('%s/python/ner' % (BASE_DIR))
sys.path.append('%s/hbc/python' % (BASE_DIR))

import Features
import twokenize
from LdaFeatures import LdaFeatures
from Dictionaries import Dictionaries
from Vocab import Vocab

sys.path.append('%s/python/cap' % (BASE_DIR))
sys.path.append('%s/python' % (BASE_DIR))

def groupNP(chunk, words):
    np_index, cur_ind_list, progress, nps = [], [], False, []

    for i in range(len(chunk)):
        if(progress):
            if(chunk[i] == "I-NP"):
                cur_ind_list.append(i)
            else:
                if(len(cur_ind_list) > 1):
                    np_index.append(cur_ind_list)
                cur_ind_list = []
                if(chunk[i] == 'B-NP'):
                    cur_ind_list.append(i)
                    progress = True
                else:
                    progress = False
        else:
            if(chunk[i] == "B-NP"):
                cur_ind_list.append(i)
                progress = True
            else:
                progress = False

    for i in range(len(np_index)):
        nps.append(' '.join([words[j] for j in np_index[i]]))
    nps = list(set(nps))

    npsStr = ""
    for np in nps:
        npsStr += np + "$$$"
    return npsStr

def groupEnts(tags, words):
    ents_index, cur_ind_list, progress, ents = [], [], False, []
    for i in range(len(tags)):
        if(progress):
            if(tags[i].startswith("I")):
                cur_ind_list.append(i)
            else:
                ents_index.append(cur_ind_list)
                cur_ind_list = []
                if(tags[i] == 'O'):
                    progress = False
                else:
                    cur_ind_list.append(tags[i])
                    cur_ind_list.append(i)
                    progress = True
        else:
            if(not(tags[i] == 'O')):
                cur_ind_list.append(tags[i])
                cur_ind_list.append(i)
                progress = True
            else:
                progress = False

    for i in range(len(ents_index)):
        ents.append((' '.join([words[j] for j in ents_index[i][1:]]), ents_index[i][0][2:]))
    ents = list(set(ents))

    entsStr = ""
    for ent in ents:
        entsStr += ent[0] + "#$#" + ent[1] + "$$$"
    return entsStr

def getEntandNP(text, posTagger, chunkTagger, eventTagger, llda, ner_model, ner, fe, capClassifier, vocab,\
            dictMap, dict2index, dictionaries, entityMap, dict2label):
    tweet = text
    line = tweet.encode('utf-8', "ignore")

    #print >> sys.stderr, "Read Line: %s, %s" % (nLines, line),
    words = twokenize.tokenize(line)
    seq_features = []
    tags = []

    goodCap = capClassifier.Classify(words) > 0.9

    if posTagger:
        pos = posTagger.TagSentence(words)
        #pos = [p.split(':')[0] for p in pos]  # remove weights   
        pos = [re.sub(r':[^:]*$', '', p) for p in pos]  # remove weights   
    else:
        pos = None

    # Chunking the tweet
    if posTagger and chunkTagger:
        word_pos = zip(words, [p.split(':')[0] for p in pos])
        chunk = chunkTagger.TagSentence(word_pos)
        chunk = [c.split(':')[0] for c in chunk]  # remove weights      
    else:
        chunk = None

    #Event tags
    if posTagger and eventTagger:
        events = eventTagger.TagSentence(words, [p.split(':')[0] for p in pos])
        events = [e.split(':')[0] for e in events]
    else:
        events = None

    quotes = Features.GetQuotes(words)
    for i in range(len(words)):
        features = fe.Extract(words, pos, chunk, i, goodCap) + ['DOMAIN=Twitter']
        if quotes[i]:
            features.append("QUOTED")
        seq_features.append(" ".join(features))
    ner.stdin.write(("\t".join(seq_features) + "\n").encode('utf8'))
        
    for i in range(len(words)):
        tags.append(ner.stdout.readline().rstrip('\n').strip(' '))

    features = LdaFeatures(words, tags)

    #Extract and classify entities
    for i in range(len(features.entities)):
        type = None
        wids = [str(vocab.GetID(x.lower())) for x in features.features[i] if vocab.HasWord(x.lower())]
        if llda and len(wids) > 0:
            entityid = "-1"
            if entityMap.has_key(features.entityStrings[i].lower()):
                entityid = str(entityMap[features.entityStrings[i].lower()])
            labels = dictionaries.GetDictVector(features.entityStrings[i])

            if sum(labels) == 0:
                labels = [1 for x in labels]
            llda.stdin.write("\t".join([entityid, " ".join(wids), " ".join([str(x) for x in labels])]) + "\n")
            sample = llda.stdout.readline().rstrip('\n')
            labels = [dict2label[dictMap[int(x)]] for x in sample[4:len(sample)-8].split(' ')]

            count = {}
            for label in labels:
                count[label] = count.get(label, 0.0) + 1.0
            maxL = None
            maxP = 0.0
            for label in count.keys():
                p = count[label] / float(len(count))
                if p > maxP or maxL == None:
                    maxL = label
                    maxP = p

            if maxL != 'None':
                tags[features.entities[i][0]] = "B-%s" % (maxL)
                for j in range(features.entities[i][0]+1,features.entities[i][1]):
                    tags[j] = "I-%s" % (maxL)
            else:
                tags[features.entities[i][0]] = "O"
                for j in range(features.entities[i][0]+1,features.entities[i][1]):
                    tags[j] = "O"
        else:
            tags[features.entities[i][0]] = "B-ENTITY"
            for j in range(features.entities[i][0]+1,features.entities[i][1]):
                tags[j] = "I-ENTITY"

    output = ["%s/%s" % (words[x], tags[x]) for x in range(len(words))]

    #Group entities
    entsStr = groupEnts(tags, words)

    #Group noun phrases
    npsStr = groupNP(chunk, words)

    return entsStr, npsStr