import wikipedia

#query = 'microsoft'

def search(query):
	search = wikipedia.search(query)
	
	return search
	
def summary(query):
	summary = wikipedia.summary(query)
	
	#return print(str([summary][0]))
	return [summary]
	
#summary(query)
