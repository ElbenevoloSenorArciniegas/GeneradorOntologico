
def tokenizarWebPage():
	
	from bs4 import BeautifulSoup
	import urllib.request
	import nltk

	response = urllib.request.urlopen('http://php.net/')
	html = response.read()
	soup = BeautifulSoup(html,"html.parser")
	text = soup.get_text(strip=True)
	tokens = [t for t in text.split()]

def limpiarStopWords(tokens):
	#Limpieza de stopWords:
	from nltk.corpus import stopwords
	clean_tokens = tokens[:]

	sw = stopwords.words('english')

	for token in tokens:
	    if token in sw:
	        clean_tokens.remove(token)
	return clean_tokens

def obtenerFrecuenciadeTokens():
	#Frecuencia de tokens
	freq = nltk.FreqDist(tokens)
	'''
	for key,val in freq.items():

	    print (str(key) + ':' + str(val))
	freq.plot(20, cumulative=False)
	'''

def obtenerSinonimos(keyWords):
	#Sinónimos de wordnet
	from nltk.corpus import wordnet

	synonyms = []
	for word in keyWords:
		for syn in wordnet.synsets(word):
			for lemma in syn.lemmas(): #ojo con los idiomas, eso va aquí 'spa'    ~/nltk_data/corpora/omw$ ls
				sinonimo = DerivacionRegresiva(lemma.name())
				if not sinonimo in synonyms + keyWords:
					synonyms.append(sinonimo)
	return keyWords+synonyms

def lematizar(token):
	#Palabras lematizadoras
	from nltk.stem import WordNetLemmatizer
	lemmatizer = WordNetLemmatizer()
	#lemmatizer.lemmatize('playing', pos="v")) Verbo, sustaNtivo, Adjetivo, adveRbio
	return lemmatizer.lemmatize(token, pos="n")

def DerivacionRegresiva(token):
	#Derivación regresiva
	from nltk.stem import SnowballStemmer
	#Ojo con los idiomas: 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish'
	#print(SnowballStemmer.languages)
	stemmer = SnowballStemmer('english')
	return stemmer.stem(token)


keyWords = obtenerSinonimos(["test"])
print(keyWords)