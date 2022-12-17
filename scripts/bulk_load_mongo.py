from pymongo import MongoClient
from pymongo.database import Database
import sys
import json

num = {
    "user": 10000,
    "article": 10000,
    "read": 1000000,
}


def bulk_load(database: Database, coll: str):
    i = 0
    write_ops = []
    for line in open('%s/%s.dat' % (data_directory, coll)).readlines():
        i = i + 1
        json_data = json.loads(line)
        write_ops.append(json_data)
        if len(write_ops) % 1024 == 0:
            database[coll].insert_many(write_ops, ordered=False)
            write_ops.clear()
        if i % (num[coll]/10) == 0:
            print("+", end='', flush=True)
    database[coll].insert_many(write_ops, ordered=False)
    print()


if __name__ == "__main__":
    data_directory = sys.argv[1] if len(sys.argv) == 2 else './data'
    mongo_address = sys.argv[2] if len(
        sys.argv) == 3 else 'mongodb://localhost:27017'

    mongo_client = MongoClient(mongo_address)
    database = mongo_client.get_database("thu-ddbs")

    print("-- Bulk loading users")
    bulk_load(database, "user")
    print("-- Bulk loading articles")
    bulk_load(database, "article")
    print("-- Bulk loading reads")
    bulk_load(database, "read")
