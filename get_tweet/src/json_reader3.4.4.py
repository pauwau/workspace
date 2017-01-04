#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, json
import csv, sqlite3

file_name = sys.argv[1]
file_name = file_name.replace(".txt","")
conn = sqlite3.connect("./" + file_name + ".db")
cur = conn.cursor()
line_id = 1

try:
    cur.execute("""CREATE TABLE tweet(tweet_id serial,sentence text,user_ID serial);""")
except sqlite3.OperationalError:
    pass

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
            user = tweet['user']
            user_id = user['id']
            print(tweet_id)
            try:
                cur.execute("""INSERT INTO tweet(tweet_id,sentence,user_ID) VALUES(%d,'%s',%d)""" %(tweet_id,tweet_str,user_id))              
            except:
                print("except")
                cur.execute("""INSERT INTO tweet(tweet_id,sentence,user_ID) VALUES(%d,'%s',%d)""" %(0,"0",0))
conn.commit()
conn.close()
