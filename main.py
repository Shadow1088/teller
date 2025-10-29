
from numpy import cos, ma
import spacy
import sqlite3
#from sentence_transformers import SentenceTransformer, util
import numpy

#model = SentenceTransformer('gtr-t5-base')
#nlp = spacy.load('en_core_web_lg')


DB_FILE_NAME = ""
QUESTION_TOLERANCE = 0.9
ANSWER_TOLERANCE = 0.70
QUESTION_MAX_LENGTH = 50
ANSWER_MAX_LENGTH = 12
ENTITIES_TOLERANCE =

# Created DB connection
db_conn = sqlite3.connect("db.db")
cursor = db_conn.cursor()

# Removes unnecessary additional tokens in text
def cutTrash():
    pass


# Returns list of entities in text
def getEnts():
    pass


# Puts tokens into their base form
def lemmaText():
    pass

#
def newEntry(table:str, args:dict):
    try:
        keys = ", ".join(args.keys())
        placeholders = ", ".join("?" for _ in args)
        values = tuple(args.values())
        sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        db_conn.commit()
        return
    except Exception as e:
        print(f"exception: {e}")

#
def loadAllEntries(table):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    return rows

#
def compareEntries():
    pass

#
def testMode():
    pass

#
def questionMode():
    print("Pokud vim, odpovim")
    q = input("Co bys rad vedel?: ")

    q_entities = {}


    q_rows = loadAllEntries("question")
    qs = [q_rows[i][1] for i in range(len(q_rows))]
    qs.append(q)


    a_rows = loadAllEntries("answer")
    n_rows = loadAllEntries("note")

    q_ents = {}
    for i, token in enumerate(nlp(q).ents):
        q_ents[token.text] = token.label_


    embeddings = model.encode(qs, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embeddings, embeddings)
    matrix = cosine_scores.tolist()
    for i, sc in enumerate(matrix):
        if sc[-1] > QUESTION_TOLERANCE and i != (len(qs)-1):
            print("I know this!")
            for j, a_row in enumerate(a_rows):
               if a_row[0] == q_rows[i][3]:
                   print(a_row[1])
                   return
    print("I do not carry this knowledge.")
    a = input("Please enlighten me.. What is the answer?")

    a_ents = {}
        for i, token in enumerate(nlp(a).ents):
            a_ents[token.text] = token.label_

    newEntry("answer",{"id":a_rows[-1][0]+1,"text":a, "entities":a_ents})
    n = input("Could you add any additional info to that?\nIt would be beneficial for future learning and others!\n: ")
    newEntry("note",{"id":n_rows[-1][0]+1,"text":q})
    newEntry("question",{"id":q_rows[-1][0]+1,"answer_id":a_rows[-1][0]+1, "note_id":n_rows[-1][0]+1, "text":q, "entities":q_ents})


def main():
    try:
        print("Ahoj, ja jsem deda vseveda")
        if input("Oc si zadas? (T/Q): ").lower == "t":
            testMode()
        else:
            questionMode()

    except Exception as e:
        print(f"exception: {e}")


if __name__ == "__main__":
    main()
