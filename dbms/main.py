from pymongo import MongoClient
from utils import prompt as default_prompt
from database_utils import *
from rich import print as pprint
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
import requests
import redis
import os


def list_something(db, username, r):
    answer = default_prompt("What do you wanna list ?\n1. Users\n2. Articles", ["1", "2"])
    if answer == "1":
        users = list_users(db, r)
        for i in users:
            display_user(i)
    if answer == "2":
        articles = list_articles(db, r)
        for i in articles:
            display_article(i)

def search_for_something(db, username, r):
    answer_t = default_prompt("What do you wanna search ?\n1. User\n2. Article\n3. Top articles", ["1", "2", "3"])
    if answer_t == "1":
        obj = db.user
    if answer_t == "2":
        obj = db.article
    if answer_t == "3":
        gran = default_prompt("Select granularity:\nmonthly\nweekly\ndaily", ["monthly", "weekly", "daily"])
        date = input("Date: ")
        call = lambda: db.popularRank.find({"_id.date": date, "granularity": gran}).limit(5)
        article = cache_redis(call, "popularRank"+str({"_id.date": date, "granularity": gran}), r)
        for i in article:
            display_top_ranked(i)
        return

    params = {}
    while True:
        answer = default_prompt("What do you wanna do ?\n1. Define a filter\n2. Search", ["1", "2"])
        if answer == "1":
            param_name = input("Enter the parameter name: ")
            if param_name == "id":
                param_name = "_id"
            param_value = input("Enter the parameter value: ")
            params[param_name] = param_value
        if answer == "2":
            break

    call = lambda: obj.find(params)
    result = cache_redis(call, answer_t + str(params), r)

    if obj == db.user:
        display_user_table(result)
    if obj == db.article:
        display_article_table(result)

def update_something(db, username, r):
    while True:
        answer = default_prompt("What do you wanna update ?\n1. A user e-mail\n2. An article abstract", ["1", "2"])
        if answer == "1":
            change_username = input("What is the username: ")
            change_email = input("What is the new email: ")
            db.user.update_many({"name": change_username}, {"$set": {"email": change_email}})
            break
        if answer == "2":
            change_title = input("What is the article title: ")
            change_abstract = input("What is the new abstract: ")
            db.article.update_many({"title": change_title}, {"$set": {"abstract": change_abstract}})
            break

def display_specific_article(db, username, r):
    id = input("Enter article ID: ")
    article = db.article.find({"_id":id})
    call = lambda: db.user.find({"name":username})
    user = cache_redis(call, username, r)[0]

    for i in article:
        print("Title: " + i["title"])
        pprint(Panel(Text(requests.get(os.environ["DBMS_OBJECT_STORAGE_PREFIX"] + "bbc_news_texts/" + i["text"]).text, justify="full")))
        if "image" in i.keys():
            print("Image link: " + os.environ["DBMS_OBJECT_STORAGE_PREFIX"] + "image/" + i["image"])
        if "video" in i.keys():
            print("Video link: " + os.environ["DBMS_OBJECT_STORAGE_PREFIX"] + "video/" + i["video"])
        read_row = {'uid':user["_id"], 'aid': id, 'region':user["region"], 'category':i["category"], 'readTimeLength': 96, 'agreeOrNot': True, 'commentOrNot': False,'shareOrNot': False, 'commentDetail': 'comments to this article: (' + user["_id"] + "," + id + ')'}
        db.read.insert_one(read_row)

        call = lambda: db.beRead.find({"_id":id})
        br = cache_redis(call, "br"+id, r)[0]
        new_readUidList = br["readUidList"]
        if user["_id"] not in new_readUidList:
            new_readUidList.append(user["_id"])
        db.beRead.update_many({"_id":id}, {"$set": {"readNum":br["readNum"]+1, "readUidList":new_readUidList}})


def loop_action(db, username, r):
    while True:
        answer = default_prompt("Select an action:\n1. List\n2. Search\n3. Modify\n4. Display an article\n5. Disconnect", ["1", "2", "3", "4", "5"])
        if answer == "1":
            list_something(db, username, r)
        if answer == "2":
            search_for_something(db, username, r)
        if answer == "3":
            update_something(db, username, r)
        if answer == "4":
            display_specific_article(db, username, r)
        if answer == "5":
            return

if __name__ == "__main__":
    mongo_address = os.environ["DBMS_MONGO_URL"]
    mongo_client = MongoClient(mongo_address)
    db = mongo_client.get_database("thu-ddbs")

    r = redis.Redis(host=os.environ["DBMS_REDIS_URL"].split("//")[1].split(":")[0], port=int(os.environ["DBMS_REDIS_URL"].split(":")[-1]), db=0)

    while True:
        answer = default_prompt("Who are you ?\n1. List all users\n2. Enter a username\n3. Quit", ["1", "2", "3"])
        if answer == "1":
            users = list_users(db, r)
            for i in users:
                display_user(i)
        if answer == "2":
            username = input("Enter your username: ")
            users = list_users(db, r)
            for i in users:
                if i["name"] == username:
                    loop_action(db, username, r)
        if answer == "3":
            exit(0)
