
from numpy import cos, ma
import spacy
import sqlite3
from sentence_transformers import SentenceTransformer, util
import numpy

model = SentenceTransformer('gtr-t5-base')
nlp = spacy.load('en_core_web_lg')


DB_FILE_NAME = ""
QUESTION_TOLERANCE = 0.9
ANSWER_TOLERANCE = 0.70
QUESTION_MAX_LENGTH = 50
ANSWER_MAX_LENGTH = 12

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
def newEntry(table, args):
    try:
        cursor.execute(f"INSERT INTO {table}")
        keys = ", ".join(args.keys())
        values = tuple(args.values())
        sql = f"INSERT INTO test ({keys}) VALUES {values}"
        cursor.execute(sql, values)
        conn.commit()
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

    q_rows = loadAllEntries("question")
    qs = [q_rows[i][1] for i in range(len(q_rows))]
    qs.append(q)

    embeddings = model.encode(qs, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embeddings, embeddings)
    matrix = cosine_scores.tolist()
    for i, sc in enumerate(matrix):
        if sc[-1] > QUESTION_TOLERANCE and i != (len(qs)-1):
            print("I know this!")
            break
        else:
            print("hmm...")


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
