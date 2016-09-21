#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import operator
from nltk import word_tokenize
from nltk.corpus import brown

dics={}
tagcount={}
startEnd = {}
a = brown.tagged_sents()
num = 0
for i in a[:1000]:
    #print "Sentence ", num
    for j in i:
    	if j[0].encode('utf-8') in dics.keys():
    		if j[1] in dics[j[0]].keys():
    			dics[j[0].encode('utf-8')][j[1].encode('utf-8')]+=1
    		else:
    			dics[j[0].encode('utf-8')][j[1].encode('utf-8')]=1
    	else:
    		dics[j[0].encode('utf-8')]={j[1].encode('utf-8'):1}
    	if j[1].encode('utf-8') in tagcount.keys():
    		tagcount[j[1].encode('utf-8')]+=1
    	else:
    		tagcount[j[1].encode('utf-8')]=1
    newSentence = [('START', '#')] + i + [('STOP', '##')]
    onlyTags = []
    for i in newSentence:
    	  onlyTags.append(i[1].encode('utf-8'))
    bigrams = zip(*[onlyTags[i:] for i in range(2)])
    for w in bigrams:
    	if w not in startEnd.keys():
    		startEnd[w] = 1
    	else:
    	 	startEnd[w] += 1
    num += 1

for i in startEnd.keys():
    print i, startEnd[i]

cnt=0
tagindex={}
#for i in startEnd.keys():
#	print i,startEnd[i]
for i in tagcount.keys():
    tagindex[i]=cnt
    cnt+=1

inp=raw_input()
#words = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", inp)
words = word_tokenize(inp)
fin={}
for i in words:
    if i in dics.keys():
        fin[i]=dics[i]
    else:
        print i,'OOV'

n=len(words)
finaltags=[0 for i in range(n)]
viterbiarray=[[0 for i in range(500)] for i in range(n)]
bparray=[[0 for i in range(500)] for i in range(n)]

for j in dics[words[0]].keys():
	viterbiarray[0][tagindex[j]]=startEnd[('#', j)]*(dics[words[0]][j]/tagcount[j])/1000

for k in range(1,len(words)):#k loop
    for j in dics[words[k]].keys():#u loop
    	maxv=-1
    	tg=''
    	for i in dics[words[k-1]].keys(): #wloop
            if (i, j) not in startEnd.keys():
                startEnd[(i, j)] = 1
    	    val=viterbiarray[k-1][tagindex[i]]*1.0*(startEnd[(i, j)]/tagcount[i])*(dics[words[k]][j]/tagcount[j])
    	    if (maxv<val):
    		maxv=val
    		tg=i
    	viterbiarray[k][tagindex[j]]=maxv
    	bparray[k][tagindex[j]]=tg

maxv=-1
tg=''
for j in dics[words[n-1]].keys():
    if (j, '##') not in startEnd.keys():
        startEnd[(j, '##')] = 1
    val=viterbiarray[n-1][tagindex[j]]*startEnd[(j, '##')]/tagcount[j]
    if (maxv<val):
	maxv=val
	tg=j

finaltags[n-1]=tg
for i in range(n-2, -1, -1):
    finaltags[i]=bparray[i+1][tagindex[finaltags[i+1]]]

print finaltags
