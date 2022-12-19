from pymongo import MongoClient
from rich import print as pprint
import redis
from bson.json_util import dumps
import json

def cache_redis(cmd, name, r):
    res = r.get(name)
    if res == None:
        r.set(name, dumps(cmd()), ex=60)
        res = r.get(name)
    return json.loads(res)

def list_users(db, r):
    return cache_redis(db.user.find, "user_tot_list", r)

def list_articles(db, r):
    return cache_redis(db.article.find, "article_tot_list", r)

def display_user(i):
    pprint("name: " + i["name"] + "\tid: " + i["_id"] + "\temail: " + i["email"])

def display_article(i):
    pprint("id: " + i["_id"] + "\ttitle: " + i["title"] + "\tcategory: " + i["category"] + "\tabstract: " + i["abstract"])

def display_top_ranked(i):
    pprint("id: " + i["_id"]["id"] + "\tdate: " + i["_id"]["date"] + "\tcount: " + str(i["count"]))
