import math 		# math module from python for log operation
import sys          # sys module for handling command line arguments passed to the module

# All locally defined modules with their imported functions
from indexer import invertedIndex
from queryProcessor import queryProcessor
from queryProcessor import queries
from converter import converter

# ARGUMENTS : Dictionary of document lengths of each document
# RETURNS : A dictionary of the K value for individual documents
# Uses k1, k2, b and average document length precomputed previously in the program
def kForDocs(documentLength):
	
	K = {}
	for document in uniqueDocuments:
		K[document] = k1*((1-b) + (b* documentLength[document]/avgDocLength))

	return K


# ARGUMENTS : Maximum number of results as in the command line argument
# RETURNS : Ranked scores as per their bm25 scores along with their DOC_ID and Query_ID
# Implements the BM25 formula as two separate parts with the functions queryTermWeight() and scoringFunction()

def docScore(maximumResults):
	kValues = kForDocs(documentLength)								# K value for each document in a Dictionary
	qid = -1
	
	for query in querySet:
		qid += 1
		docWeights = {}
		for document in uniqueDocuments:
			documentScore = 0
			for queryTerm in list(set(queryTerms[query])):
				termWeight = queryTermWeight (kValues[document], queryTerm, queryTerms[query], document)
				score = scoringFunction (document, queryTerm)
				
				if termWeight != 0: 
					documentScore += math.log(termWeight*score)
			docWeights[document] = documentScore

		rankedScores(docWeights, qid, maximumResults)	
	

# ARGUMENTS : A Dict of document weights, QueryID and maximum no. of arguments in the command line argument
# RETURNS : Ranked score of all documents with theri docID with the QueryID and system_name as per problem statement
def rankedScores(docWeights, qid, maximumResults):
	system_name = "Dinesh.K"
	sortedList = sorted(docWeights, key=docWeights.__getitem__)
	top = sortedList[-(maximumResults):]
	top.reverse()
	rank = 0
	for doc in top:
		rank += 1
		print (qid+1),"Q0"," ", doc," ",rank, " ", docWeights[doc], system_name



# ARGUMENTS : K value, Query term, Query string, document_ID
# RETURNS : Term weight in the given query and document information
# Calculated with the term frequency in the given query and constant values (K, k1, k2)
def queryTermWeight(K, term, query, doc):
	if term in index:
		termFrequency = 0
		docTuple = ()
		for document in index[term]:
			if document[0] == doc:
				docTuple = (doc, document[1])

		if docTuple != ():
			termFrequency = docTuple[1]

		queryFrequency = query.count(term)

		termWeight = (termFrequency*queryFrequency*(k1+1)*(k2+1)) / ((K+termFrequency)*(k2+queryFrequency))

		return termWeight	

	else:
		return 0


# ARGUMENTS : Doc_ID and a term or token in the query
# RETURNS : A partial weight as in the binary indeendence model
# As per the problem statement, relevance information is 0 and hence not included
def scoringFunction(doc, queryTerm):
	
	if queryTerm in index:
		relevantDocs = len(index[queryTerm])
		return (numberOfDocuments - relevantDocs + 0.5)/(relevantDocs + 0.5)
	else:
		return (numberOfDocuments + 0.5) / 0.5


# Main. The program starts from here
if __name__ == "__main__" :

	# Command line arguments all loaded into proper local variables
	indexFile = sys.argv[1]
	queryFile = sys.argv[2]
	maximumResults = int(sys.argv[3])


	# Constant parameters in the problem statement
	k1 = 1.2
	b = 0.75
	k2 = 100


	parameterTuple = converter(indexFile)
	index = parameterTuple[0]
	uniqueDocuments = parameterTuple[1]								# Set of Docs
	numberOfDocuments = len(uniqueDocuments)						# Size of Corpus
	documentLength = parameterTuple[2]								# Size of each document in a Dictionary

	querySet = queries(queryFile)									# Set of Queries
	queryTerms = queryProcessor(querySet)							# Tokenised query terms in a Dictionary

	avgDocLength = sum(documentLength.values())/numberOfDocuments	# Average document length

	docScore(maximumResults)										# Function call which computes document score

