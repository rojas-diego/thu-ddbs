from pymongo import MongoClient
from rich import print as pprint
from rich.table import Table
from rich.console import Console
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
    a = {"id":i["_id"], "name":i["name"], "email":i["email"], "region":i["region"]}
    pprint(a)

def display_article(i):
    a = {"id":i["_id"], "title":i["title"], "category":i["category"], "abstract":i["abstract"]}
    pprint(a)

def display_top_ranked(i):
    pprint("id: " + i["_id"]["id"] + "\tdate: " + i["_id"]["date"] + "\tcount: " + str(i["count"]))

def display_user_table(users):
    table = Table(title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Region")

    for i in users:
        table.add_row(i["_id"], i["name"], i["email"], i["region"])

    console = Console()
    console.print(table)

def display_article_table(articles):
    table = Table(title="Articles")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Category")

    for i in articles:
        table.add_row(i["_id"], i["title"], i["category"])

    console = Console()
    console.print(table)
