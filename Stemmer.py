import nltk
from nltk.stem import SnowballStemmer

def get_tokens():
	tokens = ['cats', 'catlike', 'catty', 'cat', 'stemmer', 'stemming', 'stemmed', 'stem', 'fishing', 'fished', 'fisher', 'argue', 'argued', 'argues', 'arguing', 'argus', 'argu', 'argument']
	return tokens

def do_stemming(filtered):
	stemmed = []
	for f in filtered:
		stemmed.append(SnowballStemmer('english').stem(f))
	return stemmed
