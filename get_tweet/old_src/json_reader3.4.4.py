#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, json
import csv, sqlite3

conn = sqlite3.connect("./sqlite.db")
cur = conn.cursor()
line_id = 1

try:
    cur.execute("""CREATE TABLE tweet(id serial,tweet text,fav serial,ret serial);""")
except sqlite3.OperationalError:
    pass
    # print("---table predev already exist---")
    # cur.execute("""DROP TABLE tweet;""")
    # cur.execute("""CREATE TABLE tweet(id serial,tweet text,fav serial,ret serial);""")

#cur.execute("""CREATE TABLE tweet(post_id serial,comment_id serial,post text,comment text);""")
#flag = False # comment or not

post_id = 0
post = []
comment_id = 0
comment =[]
i = 0

for line in sys.stdin:
    line_id += 1
    flag = True
    try:
        tweets = json.loads(line)
    except(ValueError):
        continue
    for tweet in tweets:
        if 'text' in tweet:
            tweet_id = tweet['id']
            tweet_str = '\\n'.join(tweet['text'].split('\n'))
            tweet_fav = tweet['favorite_count']
            tweet_ret = tweet['retweet_count']
            cur.execute("""INSERT INTO tweet(id,tweet,fav,ret) VALUES(%d,'%s',%d,%d)""" %(tweet_id,tweet_str,tweet_fav,tweet_ret))              
            print(tweet['id'])
#cur.execute("""SELECT post_id,comment_id,post,comment FROM tweet;""")
# for post_id,comment_id,post,comment in cur.fetchall():
#     print(u"%d %d %s %s" % (post_id,comment_id,post,comment))
conn.commit()
conn.close()
