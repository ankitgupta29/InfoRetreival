import requests0 as requests
import json,os
from sys import argv
import shutil

cd = os.getcwd()
new = cd+'/part1/'
if os.path.exists(new):
	shutil.rmtree(new)
os.mkdir(new)
os.chdir(new)

myKey =  "kB8eSPBFGknC34QhpC4UhNhBm/RjPZj1xyYk77M7wio="
gcount = 1;

querylist = ["texas%20aggies","texas%20longhorns","duke%20blue%20devil","dallas%20cowboys","dalas%20mavericksi"]

for query in querylist:
	url1 ="https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27" + query + "%27&$format=json"
	url2 ="https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27" + query + "%27&$format=json&$skip=15"
	url3 ="https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27" + query + "%27&$format=json&$skip=30"
	#print query,gcount
	urllist = []
	r = requests.get(url1, auth=(myKey, myKey)).json
	#print r.status_code
	localcount = 0
	for i in r['d']['results']:
		#ID = str(i['ID'].encode('ascii', 'ignore'))
		url = str(i['Url'].encode('ascii', 'ignore'))	
        	title=str(i['Title'].encode('ascii', 'ignore')) 
		if url  not in urllist:
			urllist.append(url)
			desc =str(i['Description'].encode('ascii', 'ignore'))
			filename = "%d.txt" %gcount     
		        f = open(filename,'a')
	        	f.write(title)
       		 	f.write("\n")
	        	f.write(desc)
        		gcount =gcount + 1
			localcount = localcount + 1
	#print localcount

	r = requests.get(url2, auth=(myKey, myKey)).json
        #print r.status_code
        for i in r['d']['results']:
                #ID = str(i['ID'].encode('ascii', 'ignore'))
		url=str(i['Url'].encode('ascii', 'ignore'))
                title=str(i['Title'].encode('ascii', 'ignore'))
                if url  not in urllist:
			urllist.append(url)
                        desc =str(i['Description'].encode('ascii', 'ignore'))
                        filename = "%d.txt" %gcount
                        f = open(filename,'a')
                        f.write(title)
                        f.write("\n")
                        f.write(desc)
                        gcount =gcount + 1
			localcount = localcount + 1

	#print "after 2nd"
	#print localcount
	if localcount < 30:
		r = requests.get(url3, auth=(myKey, myKey)).json
	        #print r.status_code
        	for i in r['d']['results']:
                	#ID = str(i['ID'].encode('ascii', 'ignore'))
			url=str(i['Url'].encode('ascii', 'ignore'))
	                title=str(i['Title'].encode('ascii', 'ignore'))
        	        if url  not in urllist:
				urllist.append(url)
                	        desc =str(i['Description'].encode('ascii', 'ignore'))
                        	filename = "%d.txt" %gcount
                        	f = open(filename,'a')
	                        f.write(title)
        	                f.write("\n")
                	        f.write(desc)
                        	gcount =gcount + 1
				localcount = localcount + 1
			if localcount == 30:
				#print "done 30"
				break			

	#print "after 3rd"
        #print localcount

os.chdir(cd)


