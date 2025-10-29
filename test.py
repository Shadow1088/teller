import spacy
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('gtr-t5-base')
nlp = spacy.load('en_core_web_lg')

# sentences = [
#     "{'USA': 'GPE', 'niggers': 'NORP', 'John Doe': 'PRSN'}",
#     "{'John Doe': 'PRSN', 'USA': 'GPE', 'niggers': 'NORP'}"
# ]
# embeddings = model.encode(sentences, convert_to_tensor=True)
# cosine_scores = util.cos_sim(embeddings, embeddings)

# s1 = nlp("{'USA': 'GPE', 'niggers': 'NORP', 'John Doe': 'PRSN'}")
# s2 = nlp("{'John Doe': 'PRSN', 'USA': 'GPE', 'niggers': 'NORP'}")

# print(cosine_scores)
# print(s1.similarity(s2))

e = {}
print(nlp(str(e)).similarity("{}"))
