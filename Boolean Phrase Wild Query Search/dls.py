from collections import deque
import sys,types,json,ast 
from pyparsing import OneOrMore, nestedExpr,Word
stack = []
depth = 2

def return_int(value):
    if isinstance(value, list):
        return map(return_int, value)
    elif isinstance(value, str):
        return int(value)
    return value

def main():
	inputdata = sys.argv[1]
	#print inputdata
	test = OneOrMore(nestedExpr()).parseString(inputdata).asList()
	#print test
	#test = [[map(int, x) for x in lst] for lst in test]
	test = return_int(test)
	#print test
	result = dfs(depth,test)
	
def goal(temp1):
	#print "temp1 : ",temp1
	if isinstance(temp1,int):
		if temp1 >= 10:
			print temp1
			print "***************YES !!"
			#return True
		else:
			return False
	else:
		return False

def dfs(depth,data):
	#print "Input for Dfs",data
	print "depth : ",depth,"data : ",data
	
	if (depth >= 0):
		value = (goal(data))
		#print "value",value

		if (value):
			return True
		else:
			#raw_input()
			if not isinstance(data,int):
				for item in data:
					t = (depth, item)
					print "Pushing : ",t
					stack.append(t)
		if stack:
			popItem = stack.pop()
			print "Pop Item : ",popItem[1],"Depth : ",popItem[0]
			dfs(popItem[0]-1,popItem[1])
			print "************ HERE *************\n"
		else:
			print "No Solution Left"

if __name__ == '__main__':
  main()




