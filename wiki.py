import wikipedia


def search(query):
	search = wikipedia.search(query)
	
	return search
	
def summary(query):
	summary = wikipedia.summary(query)
	
	return summary
