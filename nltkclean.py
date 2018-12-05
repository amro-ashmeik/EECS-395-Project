from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import string

def clean(script):

	stop_words = set(stopwords.words('english'))
	substrings = set(['—', '.', '!', '?', '...', '(', ')', '[', ']', '{', '}', ',', ':', "'", '"', ';'])

	tokens  = []

	for word in script:

		token = word.lower()

		if token in stop_words or token in string.punctuation:
			continue

		while True:
			done = 0
			for substring in substrings:
				if substring in token:
					done = 1
					token = token.replace(substring, '')
			if done == 0:
				break

		tokens.append(token)

	print(len(tokens))
	conca = " ".join(x for x in tokens)
	return conca, len(tokens)