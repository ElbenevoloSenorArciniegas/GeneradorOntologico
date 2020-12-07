from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import string

languages = {
	"spa" : 'spanish',
	'eng' : 'english',
	'fre' : 'french',
	'ita' : 'italian',
	'por' : 'portuguese',
	'fin' : 'finnish',
	'dan' : 'danish'
}

def setLanguage(l):
	global lang
	lang = l

def tokenizar(label):
	return word_tokenize(label,languages[lang])  #ejemplo para oraciones y/o otro idioma: sent_tokenize(mytext,"french")

def limpiarStopWords(tokens):
	#Limpieza de stopWords:
	clean_tokens = tokens[:]

	all_stops = set(stopwords.words(languages[lang])) | set(string.punctuation)
	for token in tokens:
	    if token in all_stops:
	        clean_tokens.remove(token)
	return clean_tokens

def obtenerSinonimos(keyWords):
	#Sinónimos de wordnet

	synonyms = []
	for word in keyWords:
		for syn in wordnet.synsets(word):
			for lemma in syn.lemmas(lang):
				sinonimo = DerivacionRegresiva([lemma.name()])[0]
				if len(sinonimo) <= 3:
					sinonimo = lemma.name()
				if not sinonimo in synonyms + keyWords:
					synonyms.append(sinonimo)
	print(synonyms)
	return synonyms

def DerivacionRegresiva(tokens):
	rtn = []
	#Derivación regresiva
	stemmer = SnowballStemmer(languages[lang])
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