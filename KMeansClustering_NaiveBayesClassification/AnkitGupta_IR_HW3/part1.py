import random,math,sys,os,re
from collections import defaultdict
from collections import Counter
dictTF =  defaultdict()
dictIDF = defaultdict()
dictNormalized = defaultdict(int)

class document:
	def __init__(self,text):
		self.content = text
		#self.cosVal = calcualatetfidf(text);



def calculateTFIDF():
	global dictIDF,dictTF
	for key in dictTF.iterkeys():
		#print "Key is %s" %key	
		idfweight  = dictIDF[key]
		doclist = dictTF[key]
		for docid in doclist:
			for item in docid.iterkeys():
				docid[item] = docid[item] * idfweight
	

def calculateIDF(docCount):
	global dictIDF,dictTF
	#print "***************  Now calculate idf *****************\n"
	j = 0
	for key,value in sorted(dictTF.iteritems(),key = lambda(k,v) : (v,k)):
		j = j+1	     
		doclist = value
		docfreq = len(doclist)
		#print "docfreq is: %s and key is : %s" %(docfreq,key)
		try:
			idf = math.log(float(docCount/docfreq),2)
			#print "idf value for word : %s is : %s" %(key,idf)
			dictIDF[key] = idf

		except ValueError:
			print "error in calculating log"	
		j = j+1

def getdocnormalized():
	global dictIDF,dictTF,dictNormalized
        for key in dictTF.iterkeys():
                doclist = dictTF[key]
		#print doclist
		for item in doclist:
			#print item
			for key in item:
				#print key,item[key]
				dictNormalized[key] = dictNormalized[key] + item[key]* item[key]

#centroidNormalized = defaultdict(int)

def getcentroidnormalized(centroid):
	sum1 = 0
        for key in centroid.iterkeys():
        	sum1  = sum1 + centroid[key]* centroid[key]
	return sum1


def updatedictTFNormalized():
	global dictTF
	for word in dictTF:
		doclist = dictTF[word]
		for item in doclist:
			for doc in item:
				item[doc] = float(item[doc])/math.sqrt(dictNormalized[doc])


def similarityScore(doc1,doc2):
	global dictIDF,dictTF,dictNormalized
	f1 = open(doc1,'r')
	f2 = open(doc2,'r')

	wordlist1 = re.findall(r"[\w']+",str(f1.readlines()).lower())

	wordlist2 = re.findall(r"[\w']+",str(f2.readlines()).lower())

	#str1 = str(f1.readlines()).lower()	
	#str2 = str(f2.readlines()).lower()
	#wordlist1 = str1.split()
	#print wordlist1
	resultlist = []
	resultlist.append(wordlist1)

	#wordlist2 = str2.split()
	resultlist.append(wordlist2)
	#print wordlist2
	result = reduce(set.intersection,map(set,resultlist))
	#print result
	sum = 0
	for word in result:
		doclist = dictTF[word]
		for item in doclist:
			if item.has_key(doc1):
				val1 = item[doc1]
			if item.has_key(doc2):
				val2 = item[doc2]
		sum = sum + val1 * val2
	
	#cosVal = sum/((math.sqrt(dictNormalized[doc1]))*(math.sqrt(dictNormalized[doc2])))
	cosVal = sum
	#print cosVal
	return cosVal	


def CentroidDocSimilarity(doc,cluster):
	resultlist = []
	centroid = cluster.centroid
        global dictIDF,dictTF,dictNormalized
	#print "doc is %s :::  " %doc
        f1 = open(doc,'r')
        wordlist1 = re.findall(r"[\w']+",str(f1.readlines()).lower())
        wordlist2 = centroid.keys()
        resultlist.append(wordlist1)

        #wordlist2 = str2.split()
        resultlist.append(wordlist2)
        #print wordlist2
        result = reduce(set.intersection,map(set,resultlist))
        #print result
        sum = 0
        for word in result:
                doclist = dictTF[word]
                for item in doclist:
                        if item.has_key(doc):
                                val1 = item[doc]
				break

                sum = sum + val1 * centroid[word]
	norm2 = getcentroidnormalized(centroid)
        #cosVal = sum/((math.sqrt(dictNormalized[doc]))*(math.sqrt(norm2)))
        #print "CosValue for centroid and doc : %s is %s" %(doc,cosVal)
	cosVal = sum
        return cosVal



#flag : 1 = initial is document list else if 0 its a clusterlist
def classify(initial,doclist,flag):
	cluster = defaultdict()
	cluster.clear()
	change = 0
	clusty = ""
	for doc in doclist:
		#print "doc is %s"%doc
                maxVal = 0
		#print "old value is %s" %clusty
                for item in initial:
			if flag:
                        	simScore = similarityScore(doc,item)
			else:
				simScore = CentroidDocSimilarity(doc,item)
                        if maxVal < simScore:
                                maxVal = simScore
                                clusty = item
		#print "new value is %s" %clusty
		#raw_input()
                cluster.setdefault(clusty,[]).append(doc)
	return cluster


	
	
class Cluster:
	def __init__(self,documents):
		if(len(documents) == 0):
			raise Exception("Empty Cluster\n")
		#self.ID = ID
		self.documents = documents
		self.centroid = self.calculateCentroid()
		self.diff = 0
		self.wordlist = defaultdict()
		self.rssk = self.calculateRSS()


	def updatecluster(self,documents):
		self.oldCentroid = self.centroid
		self.documents = documents
		self.centroid = self.calculateCentroid()
		#print sorted(self.oldCentroid)
		#print "\n*********************************\n"
		#print sorted(self.centroid)
		self.diff = self.getDistance(self.oldCentroid,self.centroid)
		return self.diff

	def getDistance(self,centroid1,centroid2):
		
		wordlist1 = centroid1.keys()
		wordlist2 = centroid2.keys()
        	resultlist = []
	        resultlist.append(wordlist1)
        	resultlist.append(wordlist2)
        
        	result = reduce(set.intersection,map(set,resultlist))
        	sum = 0
        	for word in result:
                	val1 = centroid1[word]
			val2 = centroid2[word]
                	sum = sum + val1 * val2
		norm1 = getcentroidnormalized(centroid1)
		norm2 = getcentroidnormalized(centroid2)
        	#cosVal = sum/(math.sqrt(norm1) * math.sqrt(norm2))
		cosVal = sum
        	#print cosVal
        	return cosVal		

	def calculateCentroid(self):
		os.chdir(new)
		localwordlist = []
		for doc in self.documents:
			f = open(doc,'r')
			text = f.readlines()
                	self.wordlist = re.findall(r"[\w']+",str(text).lower())
			localwordlist.append(self.wordlist)
		localwords = reduce(set.union,map(set,localwordlist))
		self.wordlist = localwords
		#print localwords
		#print "\n**************************************************\n"
		#print self.documents
		#print "\n**************************************************\n"
		centroidwords = defaultdict(int)
		for word in localwords:
			#print word
			sum = {}
			sum[word] = 0
			doclist = dictTF[word]
			#print doclist
			for item in doclist:
				for key in item:
					#print key
					if key in self.documents:
						#print key,item[key]
						sum[word] = sum[word] + item[key]
			centroidwords[word] = sum[word]/len(self.documents)
		return centroidwords


	def calculateRSS(self):
		rssk = 0.0
		for doc in self.documents:
			dist = 0.0
			wlist = [] 
                        f = open(doc,'r')
                        text = f.readlines()
                        self.wordlist = re.findall(r"[\w']+",str(text).lower())
                        wlist.append(self.wordlist)
			wlist.append(self.centroid.keys())
                	currentwords = reduce(set.union,map(set,wlist))
			#print currentwords
			#raw_input()	
			for word in currentwords:
				#print "word is %s"%word
				v1,v2 = 0.0,0.0
				if (self.centroid).has_key(word):
					v1= (self.centroid)[word]

				doclist = dictTF[word]
				#print "doclist is %s"%doclist
                        	for item in doclist:
                        		if item.has_key(doc):
						v2 = item[doc]
					#print "v1,v2 : %s,%s"%(v1,v2)
					#raw_input()
					dist = dist + (v1-v2) * (v1-v2)
				#print dist	
				#print math.sqrt(dist)
			rssk = rssk + math.sqrt(dist)
		return rssk
					
			
	


def getkeybyvalue(doc):
	for key in newcluster:
		doclist = newcluster[key]
		if doc in doclist:
			return key


			
newcluster = defaultdict()			
			

cd = os.getcwd()
new = cd+'/part1/'
	
		
def main():
	docCount = 0
	global new
	doclist =  os.listdir(new)
	os.chdir(new)
	#print doclist
	global dictTF, dictIDF
	for doc in sorted(doclist): 
    		docCount = docCount + 1
    		#print "Current doc is %s"%doc
       		f = open(doc,'r')
		#d[docCount] = document(f.readlines()) # creating document object
		#print doc
		text = f.readlines()

		wordlist = re.findall(r"[\w']+",str(text).lower())
		wordfreq = Counter(wordlist)
		#d[docCount].dict_ltfidf.clear()
		
		for w,freq in wordfreq.items():
			dict1 = {}
			word = str(w)
			#d[docCount].dict_ltfidf[w] = 1+ math.log(freq,2)
			dict1[doc] = 1+ math.log(freq,2)
			dictTF.setdefault(word,[]).append(dict1)

	#print"Total Number of Docs are: %s" %docCount
	calculateIDF(docCount)
	calculateTFIDF()
	getdocnormalized()
	updatedictTFNormalized()

	# ********* USER INPUT K VALUE 
	#print "\nEnter Value of K:",
	#temp  = raw_input()
	#k = int(temp)
	k = 8
	#doclist = 1 clusterlist = 0
	initial = random.sample(doclist,k)
	#print initial
	cluster = classify(initial,doclist,1)
	clusterlist =[]
	i =1
	for item in initial:
                x = Cluster(cluster[item])
		clusterlist.append(x)
		i = i+1


	
	#print clusterlist[0].rssk
	
	i = 0
	oldRSS = 300
        while(1):
		RSS = 0
                cluster = classify(clusterlist,doclist,0)
                for key in cluster: # here keys are cluster objects and values are set of new docs
			key.updatecluster(cluster[key])
                        RSS  =  RSS + key.calculateRSS()
		i = i +1
		#print "RSS : %s" %RSS
		if oldRSS > RSS:
			#print oldRSS
			oldRSS = RSS
			continue
		else:
			#print "Number of iterations: %s"%i
			#print "Converged with RSS Value : %s"%RSS
			break
	
	#newcluster = defaultdict()
	global newcluster
	for key in cluster:
		list1 = cluster[key]
		for item in list1:
			val= int(item[0:-4])
			newcluster.setdefault(key,[]).append(val)
		#print sorted(newcluster[key])
	
	p = 0
	
	for key in newcluster:
		list1 = newcluster[key]
		print "******************************************** CLUSTER %s *****************************************\n"%p
		p = p+1
		for val in list1:
			doc = str(val) + ".txt"
			f = open(doc,'r')
			title = f.readline()
			if val <= 30:
				print "[texas aggies]: %s"%title
			if 30 < val <= 60:
                                print "[texas longhorns]: %s"%title
			if 60 < val <= 90:
                                print "[duke blue devils]: %s"%title
			if 90 < val <= 120:
                                print "[dallas cowboys]: %s"%title
			if 120 < val <= 150:
                                print "[dallas mavericks]: %s"%title
	print "===========================================================================================================\n"				
	#Calculating purity ******************************************************
	psum = 0
	for key in newcluster:
		doclist = newcluster[key]
		list = [0] * 5
		for doc in doclist:
			val = (doc -1)/ 30
			if val == 0: 
				list[0] = list[0]  + 1
			if val == 1: 
				list[1] = list[1]  + 1
			if val == 2:
				list[2] = list[2]  + 1
			if val == 3: 
				list[3] = list[3]  + 1
			if val == 4:
				list[4] = list[4]  + 1								

		mval = max(list)
		#print "max value is : %s" %mval
		psum = psum + mval
	purity = float(psum)/150.0	
	#print "Converged with RSS Value : %s"%RSS
	#print "Purity: %s" %(purity)
	#**************************************************************************
	documentlist = newcluster.keys()
	#print documentlist
	#Calculating Rand Index ***************************************************
	tp,tn,fp,fn = 0.0,0.0,0.0,0.0
	for d1 in range(1,150):
		for d2 in range(1,150):
			if d1 != d2:
				#key1 = [key for (key,value) in newcluster.items() if value == d1]
		                    #key2 = [key for (key,value) in newcluster.items() if value == d2]
				key1 = getkeybyvalue(d1)
				key2 = getkeybyvalue(d2)
				#print key1,key2
				#print d1,d2
				if d1/30 == d2/30:
					#print "if same class"
					if key1 == key2:
						#print "if same cluster "
						tp = tp + 1
					else:
						#print "different cluster"
						fn  = fn + 1
				else:
					#print "different class"
		                        if key1 == key2:
						#print"if same cluster "
		            	        	fp = fp + 1
		                        else:
		                    	   	#print "different cluster"
		                                tn  = tn + 1
			#raw_input()
	
	#print "tp %s : tn  %s : fp %s : fn  %s"%(tp,tn,fp,fn)
	RandIndex = ((tp+tn)/(tp+tn+fp+fn))
	#print "RandIndex: %s" %(RandIndex)
	#*****************************************************************************

	'''
	#Calcuating RSS***************************************************************
	RSS = 0
	for cl in newcluster:
		#print cl.calculateRSS()
		RSS = RSS + cl.calculateRSS()
	print "RSS: %s" %RSS
	'''	

	
				        
if __name__ == '__main__':
  main()




	
