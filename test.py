import spacy
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('gtr-t5-base')
nlp = spacy.load('en_core_web_lg')

sentences = [
    "Hans Zimmerman",
    "pan Hans Zimmerman",
    "Byl to Hans Zimmerman",
    "negr",
    "Víš co je deset metrů dlouhé?",
    "Co je deset metrů dlouhé?"
]

embeddings = model.encode(sentences, convert_to_tensor=True)
cosine_scores = util.cos_sim(embeddings, embeddings)

print(cosine_scores)


args = {
    "text": "Who invented the light bulb?",
    "entities": '[{"text":"light bulb","label":"OBJECT"}]'
}
keys = ", ".join(args.keys())
values = str(", ".join(args.values()))
sql = f"INSERT INTO test ({keys}) VALUES ({values})"
print(sql)


txt = nlp('First answer is P. Diddy.')
print(txt.ents)
