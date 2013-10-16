
from collections import defaultdict
import collections
import re
import sys
import os
import shlex
import csv

#This function generate all the permuterms of the
#each word and save corresponding to word in dictionary
dictPermu = {}
def createPermuterm(word):
        temp = word + '$'
        alen = len(word)
        i = 0
        dp = collections.deque(temp)
        while(i <= alen):
                dp.rotate(alen)
                tempstr = ''.join(dp)
		dictPermu[tempstr] = word
                i = i +1

#This function takes input of wildquery and 
#return the corresponding word/words list from the dictionary
def SearchPermuKey(string,dictBoo):
	tstring = string + '$'
	index =  tstring.rindex('*')
	rotindex = len(tstring) -index -1
	#print "index is %s and rotindex is %s" %(index,rotindex)
	dp = collections.deque(tstring)
	dp.rotate(rotindex)
	tempstr = ''.join(dp)
	var = tempstr[:-1]
	splitlist = var.split('*')
	
	#mlist = []
	resultlist = []
	glist = []
	for word in splitlist:
		mlist = []
		#print "word to find in key is %s "%word
		for key in dictPermu:
			if  word in key:
				#print "Key find: %s %s" %(key,dictPermu[key])
				if dictPermu[key] not in mlist:
					mlist.append(dictPermu[key])
		#print "mlist is %s " %mlist
		if not mlist:
			#print "list is empty so return"
			return
	
		#print "list of match keys for word :%s  are : %s" %(word,mlist)		
		glist.append(mlist)
	#print "list of words matches glist :  %s" %glist
	result = reduce(set.intersection,map(set,glist))
	#print result
	for word in result:
		resultlist.append(dictBoo[word])
	#print resultlist
	result = reduce(set.union,map(set,resultlist))
	#print result
	return result
	

#This function takes input of each file and generates the 
#inverted and positional index of all the words and return
#two dictionaries each corresponding to boolean and positional indexes
def createIndex(path):
        listing =  os.listdir(path)
        dp = defaultdict(int) # Positional Dict
        db = defaultdict(int) # Boolean Dict
        dict1 = defaultdict(int)
        list2 = []
        list3 = []
        for infile in listing:
                filename = path + infile
                f = open(filename,'r')
                wcount = 0
                for line in f:
                        #list2 = re.findall(r"[\w']+", line)
			listx = re.compile("[^\w'*]|_").sub(" ",line)
			list2 = listx.split()
                        for word in list2:
                                wcount = wcount + 1
                                w = word.lower()
                                dict1 = {}
                                if dp.has_key(w):
                                        list3 = dp[w]
					#print "******* 1 **********"
                                        if infile not in list3:
                                                db.setdefault(w, []).append(infile)
                                        for x in list3:
                                                x.setdefault(infile,[]).append(wcount)
					#print "******** 2 *****"
                                else:
                                        dict1.setdefault(infile,[]).append(wcount)
                                        dp.setdefault(w, []).append(dict1)
                                        db.setdefault(w, []).append(infile)
                                        createPermuterm(w)
        return dp,db


#returns the indexlist of a word from a particular file
def getIndexlist(word,filename,dictPos):
	#print "inside getIndexlist"
	res = {}
	nestedlist = []
	indexlist = []
        if dictPos.has_key(word):
        	nestedlist = dictPos[word]
                for line in nestedlist:
      	        	res.update(line)
                for key in res.iterkeys():
                	if key == filename:
                                indexlist = sorted(res[filename])
				#print "indexlist for file %s for %s is: %s" %(filename,word,indexlist)
				break
				
	return indexlist

#this function takes phrase query as input and return the 
#documents list that contains that phrase.
def IntersectPhraseQuery(string,dictBoo,dictPos):
	#print "Inside IntersectPhraseQuery"
	qlist = []
	qlist = string.split()
	#print qlist
	list5 = []
	list5 = dictBoo[qlist[0]]
	if not list5:
		#print "list5 is empty,returning"
		return
        for word in qlist:
		#print word
		if not dictBoo.has_key(word):
			#print "when word not in dict"
			return
                list4 =  dictBoo[word]
                #print "newlist is %s " % list4
                list6 =  set(list5).intersection(set(list4))
                list5 = list6
                #print "intersected list is %s" % list5

        resultlist = []
	for filename in list5:
		mlist = []
		indexlist = [[]]
		i = 0
		for word in qlist:
			indexlist[i] = getIndexlist(word,filename,dictPos)
			mlist.append(indexlist[i])		
		j = 0
		for item in mlist:
			item[:] = [x - j for x in item]
			j = j+1 
		result = reduce(set.intersection,map(set,mlist))
		if result:
			resultlist.append(filename)	
		i = i +1
	#print "Files that contain phrase is: %s" %resultlist
	return resultlist


def main():
        list1 = []
	path = sys.argv[1]
        dictPos = {}
        dictBoo = {}
	dictPos,dictBoo = createIndex(path)
        resultDict = defaultdict(int)
        oldphrasedict = defaultdict(int)
	print "\n\nDo you want to generate Indexes in separate file ?\n"
	indexTrue = raw_input()
	itrue = indexTrue.lower()
	if(itrue == 'yes' or itrue == 'y'):
		f = csv.writer(open('indexfile.csv','w'))
		print "writing indexes........."
		for key,val in dictPos.items():
			f.writerow([key,val])
		for key,val in dictPermu.items():
			f.writerow([key,val])
		print "\n!! Indexes are saved to file ** indexfile.csv ** in current directory !!\n"
		print "\n\n*************** Enter String to Search ****************\n\n"
	else:
	        print "\n\n*************** Enter String to Search ****************\n\n"
	stdinputa = raw_input()
	stdinput = stdinputa.lower()
	while(stdinput != 'quit'):
		if(stdinput == ''):
			print "\n*************** Invalid Query: Reason:Empty Query ****************\n"
			print "\n\n*************** Enter String to Search ****************\n\n"
			stdinput = raw_input()
			continue
		resultDict.clear()
		try:
                	list1 = shlex.split(stdinput)
       		except ValueError,err:
			print "\n*************** Invalid Query: Reason:Unfinished Quote in Query ****************\n"
                        print "\n\n*************** Enter String to Search ****************\n\n"
                	stdinput = raw_input()
                	continue

		notfind = 0
		j = 0
		wild = re.compile(r'\*')
        	while(j != len(list1)):
                	str1 = list1[j]
			if wild.findall(str1):
                        	#print "Wild Query:Have to do Wild query on:  %s" %(str1)
                                resultDict[str1] = SearchPermuKey(str1,dictBoo)
				#print "resultdict in wildquery is %s" %resultDict[str1]
                                if not resultDict[str1]:
                                        resultDict[str1] = ""

                                #print resultDict[str1]  

			elif ' ' in str1:
				#print "Phrase  Query:Have to do phrase  query on:  %s" %(str1)
                                resultDict[str1] = IntersectPhraseQuery(str1,dictBoo,dictPos)
				#print "resuldict in phrasequery is %s" %resultDict[str1]
				if not resultDict[str1]:
					resultDict[str1] = ""
					
                	else:
				if dictBoo.has_key(str1):
                                        #print "Boolean Query:Have to do Boolean query on:  %s" %(str1)
                                        resultDict[str1] = dictBoo[str1]
                                else:
                                        resultDict[str1] = ""
                                        #print resultDict[str1]
				

               		j = j + 1
		finallist = []
		
		for key in resultDict.iterkeys():
                	#print "%s %s" %(key, resultDict[key])
			finallist.append(resultDict[key])
		#print "Final appended list is %s" %finallist
		finalresult = reduce(set.intersection,map(set,finallist))
		
		if finalresult:
			print "\n\n***************************************************\n\n"
			print "Search Results:\n"
			for word in finalresult:
				print "%s"%word,
			print "\n\n***************************************************\n\n"
		else:
			print "\n\n***************************************************\n\n"
                        print "Search Results:\nsorry no match :("
                        print "\n\n***************************************************\n\n"

		print "\n*************** Enter new String to Search *****************\n"
		stdinputa = raw_input()
		stdinput = stdinputa.lower()


if __name__ == '__main__':
  main()


