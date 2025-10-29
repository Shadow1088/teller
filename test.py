import spacy
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('gtr-t5-base')
nlp = spacy.load('en_core_web_lg')

sentences = [
    "Did you think we were cooked?",
    "Were you under the conclusion we were cooked?"
]
lem_sentences = [
    " ".join([token.lemma_ for token in nlp("Did you think we were cooked?")]),
    " ".join([token.lemma_ for token in nlp("Were you under the conclusion we were cooked?")])
]

embeddings = model.encode(sentences, convert_to_tensor=True)
cosine_scores = util.cos_sim(embeddings, embeddings)

print(cosine_scores)

embeddings1 = model.encode(lem_sentences, convert_to_tensor=True)
cosine_scores1 = util.cos_sim(embeddings1, embeddings1)

print(cosine_scores1)
print(" ".join([token.lemma_ for token in nlp("Did you think we were cooked?")]))
print(" ".join([token.lemma_ for token in nlp("Were you under the conclusion we were cooked?")]))

s1 = nlp("Did you think we were cooked?")
s2 = nlp("Were you under the conclusion we were cooked?")

print(s1.similarity(s2))
print(nlp(lem_sentences[0]).similarity(nlp(lem_sentences[1])))
