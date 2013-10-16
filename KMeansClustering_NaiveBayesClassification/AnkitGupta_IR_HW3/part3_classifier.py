import random,math,sys,os,re
from collections import defaultdict
from collections import Counter
dictTF =  defaultdict(int)
dictIDF = defaultdict()
totaldocs = 0.0
gdictTFIDF = defaultdict(int)
class Classes:
	def __init__(self,documentlist,string):
		self.name = string
		self.wordCount = 0.0
		self.documents = documentlist
		self.dictMI = defaultdict(int)
		self.doccount = len(documentlist)
		self.dictTFIDF = defaultdict(int)
		self.dictwords = self.calculateWords()
		self.dictProb = defaultdict(int)
		self.classProb = float(self.doccount)/totaldocs
		
	
	def calculateWords(self):
		global dictTF,gdictTFIDF,totaldocs
		'''
		print "****************************************************************************************************8***********"
		global dictTF
		for key in sorted(dictTF.keys()):
			if key == "music":
				print key, dictTF[key]
		print "****************************************************************"
		'''
		wordsDict = defaultdict(int)
		wordsDict.clear()
		for doc in sorted(self.documents): 
       			f = open(doc,'r')
			text = f.readlines()
			wordlist = re.findall(r"[\w']+",str(text).lower())
			wordfreq = Counter(wordlist)
			#print wordfreq
			for w in wordfreq:
				freq = wordfreq[w]
				dict1 = {}
				word = str(w)
				wordsDict[word] = wordsDict[word] + freq
				self.wordCount = self.wordCount + freq
				dictTF[word] = dictTF[word] + freq

				dict1[doc] = freq
                        	self.dictTFIDF.setdefault(word,[]).append(dict1)
				gdictTFIDF.setdefault(word,[]).append(dict1)

		return wordsDict


cd = os.getcwd()
new = cd+'/part3_classifier/'	
		
def main():
	global new,dictTF,totaldocs
	doclist =  os.listdir(new)
	os.chdir(new)
	entertainment,business,politics = [],[],[]
	for doc in doclist:
		val= int(doc[0:-4])
		if 0 < val < 451:
			entertainment.append(doc)
		if 450 < val < 901:
			business.append(doc)
		if 900 < val < 1351:
			politics.append(doc)
	totaldocs = len(entertainment) + len(business) + len(politics)
	#print "totaldocs number are : %s %s %s %s" %(totaldocs,len(entertainment),len(business),len(politics))	
	CategoryObjectlist = []

	entObject = Classes(entertainment,"Entertainment")
	CategoryObjectlist.append(entObject)
	
	busObject = Classes(business,"Business")
        CategoryObjectlist.append(busObject)

	polObject = Classes(politics,"Politics")
        CategoryObjectlist.append(polObject)
	

	UniqueCount = 0.0
	for word in dictTF:
		#print "%s : %s" %(item,dictTF[item])
		UniqueCount = UniqueCount + 1
	
	#++++++++++++++++++++++++++++++++++++++++++++++++++ Improvement of Naive by Feature Selection ********************************
	#Calculating MI values

	#print "Number of Unique Words in All the Classes: %s" %UniqueCount
	global gdictTFIDF
	# Feature Selection by Mutual Information 
	for word in dictTF:
		#print word
		for obj in CategoryObjectlist:		
			N11,N10,N01,N00 = 0.0,0.0,0.0,0.0
			#print obj.documents
			#print "========================================================="
			if obj.dictwords.has_key(word):
			
				v1 = obj.dictTFIDF[word] # number of documents that has word in class
				v2 = gdictTFIDF[word] # total number of documents that has word in corpus
				if not v1:
					v1len = 0.0
				else:
					v1len = float(len(v1))
				v2len = float(len(v2))

				N10 = v2len - v1len
		                N11 = v1len
		                N01 = float(len(obj.documents) - v1len)
		                N00 = totaldocs - v2len - (float(len(obj.documents))- v1len)
			
				#N00 = totaldocs - float(len(v2)) - (float(len(obj.documents))- v1)
				#print "*************************"
				#print N00,N01,N10,N11
				N = N00 + N01 + N10 + N11
				if not N11:
					N11 = 1.0
				if not N10:
					N10 = 1.0
				if not N01:
					N01 = 1.0
				if not N00:
					N00 = 1.0	
				#print N00,N01,N10,N11
				#print "*************************"
				MI = N11/N * math.log(((N*N11)/(N11+N10)* (N01 + N11)),2) + N01/N * math.log((N*N01)/((N00 + N01) * (N11 + N01)),2) + N10/N * math.log((N*N10)/((N10 + N11) * (N10 + N00)),2) + N00/N * math.log((N*N00)/((N10 + N00) * (N01 + N00)),2)
			
				#print MI
				obj.dictMI[word] = MI
		
	for obj in CategoryObjectlist:
		i = 0
		for key in sorted(obj.dictMI.items(), key=lambda x: x[1],reverse = True):
			#if obj.dictMI[key] < 0.0123:
			#print i,key
			i = i+1
			if i > 4000:
				del obj.dictwords[key[0]]
	
	#*************************************************** Improvement of Naive ends **********************************************	

	for word in dictTF:
		for obj in CategoryObjectlist:
			if obj.dictwords.has_key(word):
				value = float(obj.dictwords[word])
			else:
				value = 0.0
			classcount = obj.wordCount
                        prob = (value +1 )/ (classcount + UniqueCount)
                        obj.dictProb[word] = prob
      
				
	#******************************* TESTING DATA SET *********************************
	dictTraining = defaultdict(int)
	number = 0
	#print len(doclist)
	currentcount = 0.0
	for doc in doclist:
		val = int(doc[0:-4])	
		if 1350 < val < 1801:
			maxVal = (-100000,"Entertainment")
			for obj in CategoryObjectlist:
				#print obj.classProb
				probability = math.log(obj.classProb,2)
				f = open(doc,'r')
        	                text = f.readlines()
                	        wordlist = re.findall(r"[\w']+",str(text).lower())
				#print wordlist
				for word in wordlist:
					
					if (obj.dictProb).has_key(word):
					#if (obj.dictMI).has_key(word):
						probability = probability  + math.log((obj.dictProb)[word],2)			
	
				if maxVal[0] < probability :
					maxVal = (probability,obj.name)
			dictTraining[val] = maxVal
	'''
	for key in sorted(dictTraining.keys()):
		print key, dictTraining[key]
	'''

	print "********************************************************************************"
        print "\n                               ENTERTAINMENT \n"
        print "********************************************************************************\n"
        for key in sorted(dictTraining.keys()):
                if 1351 <= key <= 1500:
                        doc = str(key) + ".txt"
                        f = open(doc,'r')
                        title = f.readline()
                        classval = dictTraining[key]
                        print " %s :  %s "%(classval[1],title)
                        #print key, dictTraining[key]



        print "********************************************************************************"
        print "\n                               BUSINESS \n"
        print "********************************************************************************\n"

        for key in sorted(dictTraining.keys()):
                if 1501 <= key <= 1650:
                        doc = str(key) + ".txt"
                        f = open(doc,'r')
                        title = f.readline()
                        classval = dictTraining[key]
                        print " %s :  %s "%(classval[1],title)
                        #print key, dictTraining[key]


        print "********************************************************************************"
        print "\n                               POLITICS \n"
        print "********************************************************************************\n"

	for key in sorted(dictTraining.keys()):
                if 1651 <= key <= 1800:
                        doc = str(key) + ".txt"
                        f = open(doc,'r')
                        title = f.readline()
                        classval = dictTraining[key]
                        print " %s :  %s "%(classval[1],title)
                        #print key, dictTraining[key]


	print "\n==========================================================================\n"
	tp,tn,fp,fn = 0.0,0.0,0.0,0.0
	#print "Len of Testing data set is %s "%len(dictTraining)
	
	
	for key in sorted(dictTraining):
		#print "Doc ID: %s :: %s" %(key,dictTraining[key])
			
		if ((1350 < key < 1501) and (dictTraining[key][1] == "Entertainment")) or ((1500 < key < 1651) and (dictTraining[key][1] == "Business")) or ((1650 < key < 1801) and (dictTraining[key][1] == "Politics")):
			#print "Increasing TP"
			tp = tp + 1

	
		if ((1350 < key < 1501) and (dictTraining[key][1] != "Entertainment")) or ((1500 < key < 1651) and (dictTraining[key][1] != "Business")) or ((1650 < key < 1801) and (dictTraining[key][1] != "Politics")):
                        fn = fn + 1
			#print "Increasing FN"
                    

		if((key < 1351 or key > 1500) and (dictTraining[key][1] == "Entertainment")) or ((key < 1501 or key > 1650) and (dictTraining[key][1] == "Business")) or ((key < 1651 or key > 1800) and (dictTraining[key][1] == "Politics")):
			fp = fp + 1
			#print "Increasing FP"

		if((key < 1351 or key > 1500) and (dictTraining[key][1] != "Entertainment")) or ((key < 1501 or key > 1650) and (dictTraining[key][1] != "Business")) or ((key < 1651 or key > 1800) and (dictTraining[key][1] != "Politics")):
			tn = tn + 1
			#print "Increasing TN"
		else:
			print "Should Never Come here"

	#print "tp,fp,fn,tn : %s %s %s %s" %(tp,fp,fn,tn)
	precision = tp /(tp + fp)
	recall = tp /(tp + fn)
	microavg = 2*precision*recall/(precision + recall)
	#print "Precison and Recall are : %s %s" %(precision,recall)	
	#print "MicroAvg F is : %s" %microavg
				

				        
if __name__ == '__main__':
  main()

