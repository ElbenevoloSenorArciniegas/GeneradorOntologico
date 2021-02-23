from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import string

languages = {
	"spa" : {'name':'spanish','lgCode':'ES'},
	'eng' : {'name':'english','lgCode':'EN'},
	'fre' : {'french','FR'},  #problemas al descargar con WN
	'ita' : {'italian','IT'},
	'por' : {'portuguese','PT'},
	'fin' : {'finnish','FI'},
	'dan' : {'danish','DA'}
}

def setLanguage(l):
	global lang
	lang = l

def obtenerSinonimos_BabelNet(word, lemas):
	from py_babelnet.calls import BabelnetAPI
	api = BabelnetAPI('eebba5eb-276a-44b8-87ca-555d8567e722')
	senses = api.get_senses(lemma=word, searchLang=languages[lang]['lgCode'])
	for sense in senses:
		lemma = sense["properties"]["simpleLemma"]
		if not lemma in lemas:
			lemas.append(lemma)
	return lemas

def obtenerSinonimos_WN(word, lemas):
	import wn
	synsets = wn.synsets(word, lgcode=languages[lang]['lgCode'])
	for s in synsets:
		for lemma in s.lemmas():
			if not lemma in lemas:
				lemas.append(lemma)
	return lemas

def obtenerSinonimos_NLTK_WN(word, lemas):
	for syn in wordnet.synsets(word):
		for lemma in syn.lemmas(lang):
			lemma = lemma.name()
			if not lemma in lemas:
				lemas.append(lemma)
	return lemas

def obtenerSinonimos(keyWords):
	#Sinónimos de wordnet
	sinonimos = []
	lemas = []
	for word in keyWords:
		lemas.append(word)
		lemas = obtenerSinonimos_NLTK_WN(word, lemas)
		#sinonimos = obtenerSinonimos_WN(word, sinonimos)
		lemas = obtenerSinonimos_BabelNet(word, lemas)

	for lemma in lemas:
		lemma = lemma.lower()
		tokens = limpiarLabels(lemma.split("_"))
		for token in tokens:
			if not token in sinonimos:
				sinonimos.append(token)

	#print(sinonimos)
	return sinonimos

def tokenizar(label):
	return word_tokenize(label,languages[lang]['name'])

def limpiarStopWords(tokens):
	#Limpieza de stopWords:
	clean_tokens = tokens[:]

	all_stops = set(stopwords.words(languages[lang]['name'])) | set(string.punctuation)
	for token in tokens:
	    if token in all_stops:
	        clean_tokens.remove(token)
	return clean_tokens

def DerivacionRegresiva(tokens):
	rtn = []
	#Derivación regresiva
	stemmer = SnowballStemmer(languages[lang]['name'])
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