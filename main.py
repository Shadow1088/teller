import spacy
import sqlite3
from sentence_transformers import SentenceTransformer, util
import numpy
from numpy import random

model = SentenceTransformer('gtr-t5-base')
nlp = spacy.load('en_core_web_lg')


DB_FILE_NAME = ""
QUESTION_TOLERANCE = 0.9
ANSWER_TOLERANCE = 0.70
QUESTION_MAX_LENGTH = 50
ANSWER_MAX_LENGTH = 12
ENTITIES_TOLERANCE = 0.75

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
def newEntry(table:str, args):
    try:
        keys = ", ".join(args.keys())
        placeholders = ", ".join("?" for _ in args)
        values = tuple(args.values())
        sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        db_conn.commit()
        return
    except Exception as e:
        print(f"newEntry exception: {e}")

#
def loadAllEntries(table):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    return rows

#
def compareEntries():
    pass



#
def questionMode():
    print("Pokud vim, odpovim")
    q = input("Co bys rad vedel?\n: ")

    q_entities = {}


    q_rows = loadAllEntries("question")
    qs = [q_rows[i][1] for i in range(len(q_rows))]
    qs.append(q)


    a_rows = loadAllEntries("answer")
    n_rows = loadAllEntries("note")

    q_ents = {}
    for token in nlp(q).ents:
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
    a = input("Please enlighten me.. What is the answer?\n: ")

    a_ents = {}
    for token in nlp(a).ents:
        a_ents[token.text] = token.label_

    newEntry("answer",{"id":a_rows[-1][0]+1,"text":a, "entities":str(a_ents)})
    n = input("Could you add any additional info to that?\nIt would be beneficial for future learning and others!\n: ")

    n_ents = {}
    for token in nlp(n).ents:
        n_ents[token.text] = token.label_

    newEntry("note",{"id":n_rows[-1][0]+1,"text":n, "entities":str(n_ents)})
    newEntry("question",{"id":q_rows[-1][0]+1,"answer_id":a_rows[-1][0]+1, "note_id":n_rows[-1][0]+1, "text":q, "entities":str(q_ents)})

#
def testMode():

    q_rows = loadAllEntries("question")
    qs = [q_rows[i][1] for i in range(len(q_rows))]

    a_rows = loadAllEntries("answer")
    n_rows = loadAllEntries("note")


    print("Tak si te vyzkousim")
    if input("Chces otazky obecne nebo na nejakou entitu? (O/e)\n: ") == "e":
        pass
    else:
        while len(qs)!=0:
            index = random.randint(len(q_rows))
            q_row = q_rows[index]
            print(q_row[1])
            a = input(": ")
            if a == "\n":
                break
            elif a == "n":
                for note in n_rows:
                    if note[0]==q_row[4]:
                        print(note[1])
            else:
                a_ents = {}
                for token in nlp(a).ents:
                    a_ents[token.text] = token.label_
                for a_row in a_rows:
                    if q_row[3]==a_row[0]:
                        emb1 = model.encode(a, convert_to_tensor=True)
                        emb2 = model.encode(a_row[1], convert_to_tensor=True)
                        score = float(util.cos_sim(emb1, emb2))
                        ent_score = nlp(str(a_ents)).similarity(nlp(a_row[2]))
                        if ent_score > ENTITIES_TOLERANCE or score > ANSWER_TOLERANCE:
                            print("Correct!")
                        else:
                            print("not correct...")
                            print("The answer was: " + a_row[1])

            q_rows.pop(index)


def main():
    try:
        print("Ahoj, ja jsem deda vseveda")
        inpuu = input("Oc si zadas? (Q/t)\n: ").lower()
        if inpuu == 't':
            testMode()
        else:
            questionMode()

    except Exception as e:
        print(f"main exception: {e}")


if __name__ == "__main__":
    main()
