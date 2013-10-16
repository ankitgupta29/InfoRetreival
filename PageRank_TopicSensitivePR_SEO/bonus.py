import sys
import simplejson
import difflib
from collections import defaultdict
import re
from collections import Counter
import math
import unicodedata
import codecs
from  tweet import Tweet
import tweet
from datetime import datetime

tfdict = defaultdict(int)
idfdict = defaultdict(int)
TotalTweets = 0
tweetObjectdict = {}
dictdocIDNormalized = defaultdict(int) # mapping of docid and its normailzed value

def ParseTweet():
	global idfdict,tfdict,tweetObjectdict
        # Loop over all lines
        f = file('mars_tweets_medium.json', "r")
	#f = file('test.json','r')
	i =0
        lines = f.readlines()
	#tweetObjectdict = {}
        for line in lines:
                try:
                        tweet = simplejson.loads(unicode(line),encoding="UTF-8")
                        #print tweet
			t1 = Tweet()
			t1.loadtweet(tweet,tfdict)
			tweetObjectdict[t1.tid] = t1
			
			i = i+1
			
		except ValueError:
			pass
	global TotalTweets
	TotalTweets = i
	return tweetObjectdict



def PageRank(hashtag):

        for key in tweet.dictInlink:
                if not tweet.dictOutlink.has_key(key):
                        tweet.dictOutlink[key] =  set()

        N = len(tweet.dictOutlink)
        #print "NUmber of users %s"%N
        oldRank = {}

        d = 0.9
        for user in tweet.dictOutlink:
		userlist  = tweet.dicthashtag[hashtag]
		if user in userlist:
                	oldRank[user] = 1.00/len(userlist)
		else:
			oldRank[user] = 0.0

        isContinue = True
        i = 0
        while(isContinue):
                newRank = {}
                isContinue = False
                for user in tweet.dictOutlink:
                        rank = (1-d)/N
                        userlist = []
                        userlist = tweet.dictInlink[user]
                        for node in userlist:
                                userlen = len(tweet.dictOutlink[node])
                                if userlen == 0:
                                        userlen = 1
                                rank = rank + d *(oldRank[node]/userlen)
                        newRank[user] = rank
                        if (oldRank[user] - newRank[user] >= 0.00001):
                                isContinue = True
                oldRank = newRank
                i = i+1
        #print "Number of Iteration done : %s "%i
        return newRank





def main():
	ParseTweet()
	topiclistlen = {}
	for element in sorted(tweet.dicthashtag):
		taglist = tweet.dicthashtag[element]
		hlen = len(taglist)
		topiclistlen[element] = hlen
		#print "%s : %s" %(element,tweet.dicthashtag[element])
	k = 0
	global tweetObjectdict
	
	for element in sorted(topiclistlen,key = topiclistlen.get,reverse = True):	
		k = k+1
		if k > 16:
			del tweet.dicthashtag[element]
		else:
			#print "%s : %s\n" %(element,tweet.dicthashtag[element])
				pass
	
	hashkeys = tweet.dicthashtag.keys()
	print hashkeys

	k = 0
	for user in tweet.dictUserNotTag:
		tlist = tweet.dictUserNotTag[user]
		textlist = reduce(set.union,map(set,tlist))
		for word in hashkeys:
			for item in textlist:
				if item in word:
					tweet.dicthashtag.setdefault(word,[]).append(user)

	
	for element in sorted(tweet.dicthashtag):
                taglist = tweet.dicthashtag[element]
                hlen = len(taglist)
                topiclistlen[element] = hlen
                #print "%s : %s" %(element,hlen)
        
	for element in sorted(tweet.dicthashtag,key = tweet.dicthashtag.get,reverse = True):
		print "****************Topic is %s**********************\n\n"%element
		rank = PageRank(element)
		k =0
		for w in sorted(rank,key = rank.get,reverse = True):
                	#print "%s:          %s" %(w,rank[w])
                        k =  k+1
                        #print '{0:5} : {1:15}   ============>> {2:10f}'.format(k,w,rank[w])
                        print 'Rank:{0:2}:  :{1:10}'.format(k,w)
                        if k == 10:
                                break
	
	


if __name__ == '__main__':
 main()
