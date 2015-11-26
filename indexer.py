# ARGUMENTS : Filename of the stemmed corpus
# RETURNS : A tuple containing InvertedIndex, List of unique docs and Dict of document length

def invertedIndex(fileName):
	f = open(fileName, 'r')
	index = {}
	docTokens = []
	docID = 0
	docList = []
	docLength = {}
	for line in f:
		if line != '\n':
			if line[0] == '#':												# Break which indicates new document
				if len(docTokens) == 0:
					docTokens = []
					docID = int(line[1:])
					docList.append(docID)
				else:
					index = addToIndex(docTokens, docID, index)
					docLength[docID] = len(docTokens)
					docTokens = []
					docID = int(line[1:])
					docList.append(docID)
			else:
				tokens = line.split(' ')
				tokens[-1] = tokens[-1].split('\n').pop(0)
				tokens = [token for token in tokens if not token.isdigit()]  # Ignores all number only tokens 
				docTokens = docTokens + tokens


	index = addToIndex(docTokens, docID, index)
	docList.append(docID)
	docLength[docID] = len(docTokens)
	return (index, list(set(docList)), docLength)  							# Final tuple that is returned



# ARGUMENTS : List of tokens in a document
# RETURNS : Frequency of each term in the document as a Dictionary
def termFrequency(tokens):
	distinctTokens = list(set(tokens))
	freqDict = {}
	for token in distinctTokens:
		freqDict[token] = tokens.count(token)

	return freqDict


# ARGUMENTS : Tokens in a doc, Document ID, InvertedIndex
# RETURNS : An updated inverted index with the doc ID and term frequency
def addToIndex(docTokens, docID, index):
	freqDict = termFrequency(docTokens)
	for token in list(set(docTokens)):
		if token in index:
			index[token].append((docID, freqDict[token]))
		else:
			index[token] = []
			index[token].append((docID, freqDict[token]))
	return index



# print invertedIndex('tokens.txt')