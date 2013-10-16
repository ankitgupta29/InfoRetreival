import requests0 as requests
import json,os,re
from sys import argv
import shutil

cd = os.getcwd()
new = cd+'/part3_classifier/'
if os.path.exists(new):
	shutil.rmtree(new)
os.mkdir(new)
os.chdir(new)

myKey =  "kB8eSPBFGknC34QhpC4UhNhBm/RjPZj1xyYk77M7wio="
gcount = 1;

#querylist = ["texas%20aggies","texas%20longhorns","duke%20blue%20devil","dallas%20cowboys","dalas%20mavericksi"]
categorylist = ["&NewsCategory=%27rt_Entertainment","&NewsCategory=%27rt_Business","&NewsCategory=%27rt_Politics"]
querylist = ["bing", 'amazon', 'twitter', 'yahoo','google','beyonce', 'bieber', 'television','movies', 'music','obama', 'america', 'congress', 'senate', 'lawmakers','apple', 'facebook', 'westeros', 'gonzaga', 'banana']

for category in categorylist:
	for query in querylist:
		temp = query + "%27" + category
		url1 ="https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27" + temp + "%27&$format=json"
		url2 ="https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27" + temp + "%27&$format=json&$skip=15"
		url3 ="https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27" + temp + "%27&$format=json&$skip=30"
		
		localcount = 0
		#print query,gcount,url1
        	urllist = []
        	r = requests.get(url1, auth=(myKey, myKey)).json

		for i in r['d']['results']:
	                url = str(i['Url'].encode('ascii', 'ignore'))
        	        title=str(i['Title'].encode('ascii', 'ignore'))
                	if url  not in urllist:
                        	urllist.append(url)
	                        desc =str(i['Description'].encode('ascii', 'ignore'))
	
        	                filename = "%d.txt" %gcount
                	        f = open(filename,'a')
                        	Url =str(i['Url'].encode('ascii', 'ignore'))
	                        wordlist = re.findall(r"[\w']+",str(Url).lower())
        	                url = " ".join(wordlist)
                	        #print url
                        	f.write(url)
	                        f.write("\n")
        	                f.write(title)
                	        f.write("\n")
                        	f.write(title)
	                        f.write("\n")
        	                f.write(desc)
                	        gcount =gcount + 1
                        	localcount = localcount + 1

	        #print localcount

		r = requests.get(url2, auth=(myKey, myKey)).json
		#print r.status_code


                for i in r['d']['results']:
                        url = str(i['Url'].encode('ascii', 'ignore'))
                        title=str(i['Title'].encode('ascii', 'ignore'))
                        if url  not in urllist:
                                urllist.append(url)
                                desc =str(i['Description'].encode('ascii', 'ignore'))

                                filename = "%d.txt" %gcount
                                f = open(filename,'a')
                                Url =str(i['Url'].encode('ascii', 'ignore'))
                                wordlist = re.findall(r"[\w']+",str(Url).lower())
                                url = " ".join(wordlist)
                                #print url
                                f.write(url)
                                f.write("\n")
                                f.write(title)
                                f.write("\n")
                                f.write(title)
                                f.write("\n")
                                f.write(desc)
                                gcount =gcount + 1
                                localcount = localcount + 1

		#print localcount
		if localcount < 30:
		        r = requests.get(url3, auth=(myKey, myKey)).json
	                for i in r['d']['results']:
	                        url = str(i['Url'].encode('ascii', 'ignore'))
        	                title=str(i['Title'].encode('ascii', 'ignore'))
                	        if url  not in urllist:
                        	        urllist.append(url)
                                	desc =str(i['Description'].encode('ascii', 'ignore'))

	                                filename = "%d.txt" %gcount
        	                        f = open(filename,'a')
                	                Url =str(i['Url'].encode('ascii', 'ignore'))
                        	        wordlist = re.findall(r"[\w']+",str(Url).lower())
                                	url = " ".join(wordlist)
	                                #print url
        	                        f.write(url)
                	                f.write("\n")
                        	        f.write(title)
                                	f.write("\n")
	                                f.write(title)
        	                        f.write("\n")
                	                f.write(desc)
                        	        gcount =gcount + 1
                                	localcount = localcount + 1

				if localcount == 30:
					break

os.chdir(cd)
