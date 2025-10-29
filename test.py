import spacy
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('gtr-t5-base')
nlp = spacy.load('en_core_web_lg')

sentences = [
    "John Doe",
    "JON DOE"
]
embeddings = model.encode(sentences, convert_to_tensor=True)
cosine_scores = util.cos_sim(embeddings, embeddings)

print(cosine_scores)
