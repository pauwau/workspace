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
    cur.execute("""CREATE TABLE dialogue(dia_id serial,tweet_array text);""")
except sqlite3.OperationalError:
    pass

for line in open( file_name + ".txt", 'r'):
    #print line
    cur.execute("""INSERT INTO dialogue(dia_id,tweet_array) VALUES(%d,'%s')""" %(line_id,line))
    line_id = line_id + 1	
conn.commit()
conn.close()