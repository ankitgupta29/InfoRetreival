Author: Ankit Gupta
UIN: 621009649
email: ankitgupta@tamu.edu
Homework 1: Mini Search Engine
Course: CSCE 670 Spring 2013
Instructor: Prof. James Caverlee, CSE Deptt, Texas A&M University
Date: 09 Feb, 2013

File (homework1.py) will build a functioning text-based mini search engine using python.
Search engine will support both single term queries and phrase queries,as well as wild-card queries.


Input: 
a .On command line argument, enter directory path, within which you want to search for query
b .Enter Query when it promts you to enter on stdinput
c. 'quit' is used as a termination word. If you type quit on stdin, then program will terminate.

How to Run ?

cmd:> python homwork1.py <directory path of files to get indexed>

It create indexes of the files in about 25 Seconds and ask you if you want to save them in a file.If yes, then it stores the indexes in file: "indexfile.csv"
of size about 71 MB.if no,you can directly search for query on prompt.


Cases handled:
a. empty query is considered as invalid and have to re enter the query
b. if query contains missing quote, its considered invalid also
c. Can handle mutiple * in wildquery
d. Cannot handle wildquery within phrase query
e. words like (I've) are stored as (I've) and not (I) and (ve). No words are splitted on (').



**********************************************************************************************************
Three type of dictionaries are used to store indexes,positions and permuterm of the words in files.

dictPermu: store the permuterm of each word in files
dictBoo	 : store the word and files in which word exists
dictPos  : store the word and for each word there is dictionary that has filename containing it and index of that word in file
*****************************************************************************************************************************

This file has following functions:

#This function generate all the permuterms of the
#each word and save corresponding to word in dictionary
def createPermuterm(word):

***********************************************************
#This function takes input of wildquery and 
#return the corresponding word/words list from the dictionary
def SearchPermuKey(string,dictBoo):
***********************************************************

#This function takes input of each file and generates the 
#inverted and positional index of all the words and return
#two dictionaries each corresponding to boolean and positional indexes
def createIndex(path):
*****************************************************************

#This function returns the indexlist of a word from a particular file
def getIndexlist(word,filename,dictPos):
****************************************************************

#This function takes phrase query as input and return the 
#documents list that contains that phrase.
def IntersectPhraseQuery(string,dictBoo,dictPos):
******************************************************************

#Starting of Code
def main():
*******************************************************************


