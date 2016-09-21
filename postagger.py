#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Imports
import re
import operator
from nltk import word_tokenize
from nltk.corpus import brown
import ast

mainDict = {}
tagcount = {}
startEnd = {}

#Open the file having word and its tags
f = open('a', 'r')
a = f.readlines()
f.close()

#Train on the data
for i in a:
    line = i.split('{')
    word = line[0].strip()
    tags = '{' + line[1].strip()
    newTags = ast.literal_eval(tags)
    if word in mainDict.keys():
        for tag in newTags.keys():
    	    if tag in mainDict[word].keys():
    	        mainDict[word][newTags[tag]] += 1
    	    else:
    	        mainDict[word][newTags[tag]] = 1
    else:
    	mainDict[word] = newTags
for word in mainDict.keys():
    for tag in mainDict[word].keys():
        if tag not in tagcount.keys():
            tagcount[tag] = mainDict[word][tag]
        else:
            tagcount[tag] += mainDict[word][tag]

#Open the file having bigrams
g = open('b', 'r')
b = g.readlines()
g.close()

for i in b:
    line = i.split(') ')
    bigram = line[0].strip() + ')'
    count = int(line[1].strip())
    startEnd[ast.literal_eval(bigram)] = count

cnt=0
tagindex = {}
for i in tagcount.keys():
    tagindex[i] = cnt
    cnt += 1
newDict = {}
for i in tagcount.keys():
    newDict[i] = 1

#Implementing Viterbi
while True:
    inp = raw_input("Input:")
    if inp == 'q':
        break
    #words = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", inp)
    words = word_tokenize(inp)
    fin = []
    for i in words:
        if i in mainDict.keys():
            fin.append(i)
        else:
            mainDict[i] = newDict
            print i,'OOV'
    
    n=len(words)
    finaltags = [0 for i in range(n)]
    viterbiarray = [[0 for i in range(500)] for i in range(n)]
    bparray = [[0 for i in range(500)] for i in range(n)]
    
    for j in mainDict[words[0]].keys():
        if ('#', j) not in startEnd.keys():
            startEnd[('#', j)] = 1
        viterbiarray[0][tagindex[j]]=startEnd[('#', j)]*(mainDict[words[0]][j]/tagcount[j])/20000
    
    for k in range(1,len(words)):#k loop
        for j in mainDict[words[k]].keys():#u loop
            maxv = -1
            newTag = ''
            for i in mainDict[words[k-1]].keys(): #wloop
                if (i, j) not in startEnd.keys():
                    startEnd[(i, j)] = 1
        	val=viterbiarray[k-1][tagindex[i]] * 1.0 *(startEnd[(i, j)]/tagcount[i]) * (mainDict[words[k]][j] / tagcount[j])
        	if (maxv < val):
        	    maxv = val
        	    newTag = i
            viterbiarray[k][tagindex[j]] = maxv
            bparray[k][tagindex[j]] = newTag
    
    maxv = -1
    newTag = ''
    for j in mainDict[words[n-1]].keys():
        if (j, '##') not in startEnd.keys():
            startEnd[(j, '##')] = 1
        val=viterbiarray[n-1][tagindex[j]] * startEnd[(j, '##')] / tagcount[j]
        if (maxv < val):
    	    maxv = val
    	    newTag = j
    
    finaltags[n-1] = newTag
    for i in range(n-2, -1, -1):
        finaltags[i] = bparray[i+1][tagindex[finaltags[i+1]]]
    
    print finaltags
