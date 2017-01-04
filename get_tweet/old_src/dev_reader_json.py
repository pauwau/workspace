#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, json
import csv, sqlite3

#cur.execute("""CREATE TABLE tweet(post_id serial,comment_id serial,post text,comment text);""")
conn = sqlite3.connect('./sqlite.db')
cur = conn.cursor()
try:
    cur.execute("""CREATE TABLE predev(post_id serial,comment_id serial,post text,comment text);""")
except sqlite3.OperationalError:
   print("---table predev already exist---")
   # cur.execute("""DROP TABLE predev;""")
   # cur.execute("""CREATE TABLE predev(post_id serial,comment_id serial,post text,comment text);""")

fd = open('../devset/dev.txt', 'r')
fdl = open('../devset/devlist.txt', 'r')

line_id = 1
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
            if (flag == True):  #comment or not
                post_id = tweet['id']
                post = '\\n'.join(tweet['text'].split('\n'))
                # print(post_id,)
                # print(post)
                flag = False
            else:
                comment_id = tweet['id']
                comment = '\\n'.join(tweet['text'].split('\n'))
                # print(comment_id)
                # print(comment)
                cur.execute("""INSERT INTO predev(post_id,comment_id,post,comment) VALUES(%d,%d,'%s','%s')""" %(post_id,comment_id,post,comment))              
    print(post_id)
    conn.commit()
#cur.execute("""SELECT post_id,comment_id,post,comment FROM tweet;""")
# for post_id,comment_id,post,comment in cur.fetchall():
#     print(u"%d %d %s %s" % (post_id,comment_id,post,comment))
conn.close()
