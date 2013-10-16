import random,math,sys,os,re
from collections import defaultdict
from collections import Counter
dictTF =  defaultdict(int)
dictIDF = defaultdict()
totaldocs = 0.0

class Classes:
	def __init__(self,documentlist,string):
		self.name = string
		self.wordCount = 0.0
		self.documents = documentlist
		self.doccount = len(documentlist)
		self.dictwords = self.calculateWords()
		self.dictProb = defaultdict(int)
		self.classProb = float(self.doccount)/totaldocs
		
	
	def calculateWords(self):
		global dictTF
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
				#dict1 = {}
				word = str(w)
				wordsDict[word] = wordsDict[word] + freq
				self.wordCount = self.wordCount + freq
				dictTF[word] = dictTF[word] + freq
		return wordsDict

		

cd = os.getcwd()
new = cd+'/part2/'	
		
def main():
	global new,dictTF,totaldocs
	doclist =  os.listdir(new)
	#print doclist
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
	print "totaldocs number are : %s %s %s %s" %(totaldocs,len(entertainment),len(business),len(politics))	
	CategoryObjectlist = []

	entObject = Classes(entertainment,"Entertainment")
	CategoryObjectlist.append(entObject)
	
	busObject = Classes(business,"Business")
        CategoryObjectlist.append(busObject)

	polObject = Classes(politics,"Politics")
        CategoryObjectlist.append(polObject)
	

	UniqueCount = 0.0
	for item in dictTF:
		#print "%s : %s" %(item,dictTF[item])
		UniqueCount = UniqueCount + 1
	
	print "Number of Unique Words in All the Classes: %s" %UniqueCount

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
						probability = probability  + math.log((obj.dictProb)[word],2)
			
	
				if maxVal[0] < probability :
					maxVal = (probability,obj.name)
			dictTraining[val] = maxVal
	
	print "********************************************************************************"
	print "\n				ENTERTAINMENT \n"
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
	#print"==============================================================================\n"
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

	#print "===========================================================================\n"
	#print "tp,fp,fn,tn : %s %s %s %s" %(tp,fp,fn,tn)
	precision = tp /(tp + fp)
	recall = tp /(tp + fn)
	microavg = 2*precision*recall/(precision + recall)
	#print "Precison and Recall are : %s %s" %(precision,recall)	
	#print "MicroAvg F is : %s" %microavg
				

				        
if __name__ == '__main__':
  main()

