# ARGUMENTS : File name which contains all the queries
# RETURNS : A list of queries from the queries file

def queries(fileName):
	f = open(fileName,'r')

	queryList = []
	for line in f:

		if line[-1] == '\n':				# Remove new line character
			queryList.append(line[0:-1])
		else:
			queryList.append(line)

	#querySet = list(set(queryList))          #If duplicates are to be removed

	return queryList


# ARGUMENTS : A list of queries
# RETURNS : Individual query terms of each query in a dictionary

def queryProcessor(querySet):
	
	queryTerms = {}

	for query in querySet:
		queryTerms[query] = query.split(" ")

	return queryTerms



