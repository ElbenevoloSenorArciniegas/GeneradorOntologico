
def tokenizar(label):
	from nltk.tokenize import word_tokenize
	return word_tokenize(label)  #ejemplo para oraciones: sent_tokenize(mytext,"french") 

def limpiarStopWords(tokens):
	#Limpieza de stopWords:
	from nltk.corpus import stopwords
	import string
	clean_tokens = tokens[:]

	all_stops = set(stopwords.words('english')) | set(string.punctuation)
	for token in tokens:
	    if token in all_stops:
	        clean_tokens.remove(token)
	return clean_tokens

def obtenerSinonimos(keyWords):
	#Sinónimos de wordnet
	from nltk.corpus import wordnet

	synonyms = []
	for word in keyWords:
		for syn in wordnet.synsets(word):
			for lemma in syn.lemmas(): #ojo con los idiomas, eso va aquí 'spa'    ~/nltk_data/corpora/omw$ ls
				sinonimo = DerivacionRegresiva([lemma.name()])[0]
				if len(sinonimo) <= 3:
					sinonimo = lemma.name()
				if not sinonimo in synonyms + keyWords:
					synonyms.append(sinonimo)
	return synonyms

def lematizar(token):
	#Palabras lematizadoras
	from nltk.stem import WordNetLemmatizer
	lemmatizer = WordNetLemmatizer()
	#lemmatizer.lemmatize('playing', pos="v")) Verbo, sustaNtivo, Adjetivo, adveRbio
	return lemmatizer.lemmatize(token, pos="n")

def DerivacionRegresiva(tokens):
	rtn = []
	#Derivación regresiva
	from nltk.stem import SnowballStemmer
	#Ojo con los idiomas: 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish'
	#print(SnowballStemmer.languages)
	stemmer = SnowballStemmer('english')
	for token in tokens:
		rtn.append(stemmer.stem(token))
	return rtn

def limpiarLabels(labels):
	rtn = []
	for label in labels:
		tokens = tokenizar(label.lower())
		tokens = limpiarStopWords(tokens)
		tokens = DerivacionRegresiva(tokens)
		for token in tokens:
			if not token in rtn:
				rtn.append(token)
	return rtn