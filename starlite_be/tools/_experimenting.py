import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")

# Initialize wordnet lemmatizer
wnl = WordNetLemmatizer()

example_sentence = "Python programmers often tend like programming in python because it's like english. We call people who program in python pythonistas."

# Remove punctuation
example_sentence_no_punct = example_sentence.translate(str.maketrans("", "", string.punctuation))

word_tokens = word_tokenize(example_sentence_no_punct)

# Perform lemmatization
print("{0:20}{1:20}".format("--Word--","--Lemma--"))
for word in word_tokens:
   print ("{0:20}{1:20}".format(word, wnl.lemmatize(word, pos="v")))
   
pass