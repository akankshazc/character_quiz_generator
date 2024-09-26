from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy

# Importing Test chapter
text = open('TMBD_Chapters/1_ASR_1.txt', 'r').read()

# Remove Whitespace
text = re.sub(r'\s+', ' ', text)

# Remove Special Characters
text = re.sub(r'[^A-Za-z0-9\s]', '', text)

# Convert text to lowercase
text = text.lower()


# Tokenizing text by word
tokenized_text = word_tokenize(text)

# Remove Stopwords
stop_words = set(stopwords.words('english'))
filtered_text = [token for token in tokenized_text if token not in stop_words]

# Stemming
stemmer = PorterStemmer()

stemmed_text = [stemmer.stem(token) for token in filtered_text]

# Lemmatization with spaCy
nlp = spacy.load('en_core_web_sm')

lemmatized_text = [nlp(token) for token in filtered_text]
