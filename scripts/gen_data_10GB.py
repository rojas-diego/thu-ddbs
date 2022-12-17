import json
import random
import numpy as np
import os

NUM_USERS = 10000
NUM_ARTICLES = 10000
NUM_READS = 1000000

NUM_IMAGES = 600

uid_region = {}
aid_lang = {}
aid_category = {}


def gen_an_user(i):
    """
    Beijing:60%   Hong Kong:40%
    en:20%    zh:80%
    20 depts
    3 roles
    50 tags
    0~99 credits
    """
    timeBegin = 1506328859000
    user = {}
    user["timestamp"] = str(timeBegin + i)
    user["_id"] = 'u'+str(i)
    user["name"] = "user%d" % i
    user["gender"] = "male" if random.random() > 0.33 else "female"
    user["email"] = "email%d" % i
    user["phone"] = "phone%d" % i
    user["dept"] = "dept%d" % int(random.random() * 20)
    user["grade"] = "grade%d" % int(random.random() * 4 + 1)
    user["language"] = "en" if random.random() > 0.8 else "zh"
    user["region"] = "Beijing" if random.random() > 0.4 else "Hong Kong"
    user["role"] = "role%d" % int(random.random() * 3)
    user["preferTags"] = "tags%d" % int(random.random() * 50)
    user["obtainedCredits"] = str(int(random.random() * 100))

    uid_region[user["_id"]] = user["region"]
    return user


def gen_an_article(i):
    """
    science:45%   technology:55%
    en:50%    zh:50%
    50 tags
    2000 authors
    """
    timeBegin = 1506000000000
    article = {}
    article["_id"] = 'a'+str(i)
    article["timestamp"] = str(timeBegin + i)
    article["title"] = "title%d" % i
    article["category"] = "science" if random.random() > 0.55 else "technology"
    article["abstract"] = "abstract of article %d" % i
    article["articleTags"] = "tags%d" % int(random.random() * 50)
    article["authors"] = "author%d" % int(random.random() * 2000)
    article["language"] = "en" if random.random() > 0.5 else "zh"

    categories = ['business', 'entertainment', 'sport', 'tech']
    num_articles_per_category = [510, 386, 511, 401]
    random_category = random.randint(0, 3)
    random_article = random.randint(
        1, num_articles_per_category[random_category])
    article["text"] = categories[random_category] + \
        "/"+str(random_article).zfill(3) + ".txt"

    if random.randint(0, 1) == 1:
        article["image"] = str(random.randint(0, NUM_IMAGES)) + ".jpg"

    if random.randint(0, 3) == 1:
        article["video"] = "video" + str(random.randint(1, 2)) + ".flv"

    aid_lang[article["_id"]] = article["language"]
    aid_category[article["_id"]] = article["category"]
    return article


# user in Beijing read/agree/comment/share an english article with the probability 0.6/0.2/0.2/0.1
# user in Hong Kong read/agree/comment/share an Chinese article with the probability 0.8/0.2/0.2/0.1
p = {}
p["Beijing"+"en"] = [0.6, 0.2, 0.2, 0.1]
p["Beijing"+"zh"] = [1, 0.3, 0.3, 0.2]
p["Hong Kong"+"en"] = [1, 0.3, 0.3, 0.2]
p["Hong Kong"+"zh"] = [0.8, 0.2, 0.2, 0.1]


def gen_an_read(i):
    timeBegin = 1506332297000
    read = {}
    read["timestamp"] = str(timeBegin + i*10000)
    read["_id"] = 'r'+str(i)
    read["uid"] = 'u'+str(int(random.random() * NUM_USERS))
    read["aid"] = 'a'+str(int(random.random() * NUM_ARTICLES))

    region = uid_region[read["uid"]]
    lang = aid_lang[read["aid"]]
    ps = p[region + lang]

    read["region"] = region
    read["category"] = aid_category[read["aid"]]
    if (random.random() > ps[0]):
        return gen_an_read(i)
    else:
        read["readTimeLength"] = int(random.random() * 100)
        read["agreeOrNot"] = True if random.random() < ps[1] else False
        read["commentOrNot"] = True if random.random() < ps[2] else False
        read["shareOrNot"] = True if random.random() < ps[3] else False
        read["commentDetail"] = "comments to this article: (" + \
            read["uid"] + "," + read["aid"] + ")"
    return read


if not os.path.exists('./data'):
    os.mkdir('./data')

with open("data/user.dat", "w+") as f:
    for i in range(NUM_USERS):
        json.dump(gen_an_user(i), f)
        f.write("\n")

with open("data/article.dat", "w+") as f:
    for i in range(NUM_ARTICLES):
        json.dump(gen_an_article(i), f)
        f.write("\n")

with open("data/read.dat", "w+") as f:
    for i in range(NUM_READS):
        json.dump(gen_an_read(i), f)
        f.write("\n")
