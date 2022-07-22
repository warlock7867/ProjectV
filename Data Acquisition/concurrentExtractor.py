import concurrent.futures as cf
from email.mime import base
from time import perf_counter, sleep
import allAnime as aa
from pymongo import MongoClient
from datetime import datetime

def insertIntoMongo(dbName:str, collectionName:str, bigData:list) -> None:
    client = MongoClient("mongodb://localhost:27017/")
    database = client[dbName]
    collection = database[collectionName]
    x = collection.insert_many(bigData)
    print('inserted into Mongo')

def makeBatches(array:list, n = 50) -> list:
    # accepts a list and makes returns a list of lists whose elements are of the specified batch size
    
    lengthOfArray = len(array)
    extra = lengthOfArray % n
    batches = []
    for i in range(0, lengthOfArray, n):
        try:
            res = [array[i + j] for j in range(n)]
            batches.append(res)
        except:
            extras = [array[i + j] for j in range(extra)]
            batches.append(extras)
    return batches

if __name__ == '__main__':
    start = perf_counter()

    '''
        OBTAIN URLS FOR ALL THE ANIME FROM BASE URL
    '''
    baseURL = r'https://myanimelist.net/topanime.php'
    urls = aa.listOfShows(baseURL, 100)

    batches = makeBatches(urls, 400)
    for urls in batches:
        with cf.ProcessPoolExecutor() as executor:
            bigData = []
            tasks = [executor.submit(aa.APICaller, url) for url in urls]
            for f in cf.as_completed(tasks):
                bigData.append(f.result())
        insertIntoMongo("anime", "showDB", bigData)
        print(f'finished batch...at {datetime.now()}')
    
        sleep(120)

    end = perf_counter() - start
    print(f'Execution time: {round(end, 2)} seconds')