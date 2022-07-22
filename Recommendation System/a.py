from bson import ObjectId
from gridfs import Database
from pymongo import MongoClient
import pandas as pd
client = MongoClient(host='localhost', port=27017)
database = client['anime']
collection = database['showDB']

def makeRecord(show:dict) -> list:
    record = show.values()
    return record


def displayDict(d:dict) -> None:
    for i in d:
        print(i, ": ", d[i])

anime = collection.find({})
i = 0
rows = []
for a in anime:
    record = [a['_id']]
    keys = a.keys()
    record.append(len(keys))
    rows.append(record)

res = pd.DataFrame(rows, columns=['id', 'columns'])
res.sort_values(by = ['id'], inplace = True)
res.to_csv('problem.csv', index = False)