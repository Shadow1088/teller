import spacy
from sentence_transformers import SentenceTransformer, util


nlp = spacy.load('en_core_web_lg')
text = "I'm the greatest technician widely since 1980"
#print(text)

tokens = [token.text for token in nlp(text)]
#print(tokens)

lemmas = [token.lemma_ for token in nlp(text)]
print(" ".join(lemmas))

entits = {}
for i, token in enumerate(nlp(text).ents):
    entits[token.text] = token.label_
print("".join((entits.keys())), "".join(entits.values()))
print(str(entits))

# for EN
# when checking QUESTION similarity, tolerance: >0.9
# when checking ANSWER similarity, tolerance: >0.7

# for CZ
# we cannot use spacy english model on czech text, obviously
# we can use google's model in SentenceTransformer
# when checking QUESTION similarity, tolerance: >0.8
# when checking ANSWER similarity, tolerance: >0.7
