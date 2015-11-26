
import ast 		# import ast module provided with python by default


# ARGUMENTS : File name containing the inverted index along with doc related information
# RETURNS : The index of the appropriate data type, a tuple where the index is found as a Dictionary
# Uses Abstract Syntax Trees of python, converting a string to expression using a safe eval

def converter(fileName):
	f = open(fileName, 'r')
	s = f.read().replace("\n", "")
	d = ast.literal_eval(s)
	return d	