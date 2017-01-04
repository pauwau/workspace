#!/usr/bin/python
# -*- coding: utf-8 -*-
from pytrends.pyGTrends import pyGTrends
import time
from random import randint

google_username = "ii.mmi.twitter@gmail.com"
google_password = "36186954"
path = ""
request_word = "とは,hl='en-US'"

# connect to Google
connector = pyGTrends(google_username, google_password)

# # make request
connector.request_report(request_word)

# # wait a random amount of time between requests to avoid bot detection
time.sleep(randint(3,5))

# # download file
connector.save_csv(path, request_word.decode("utf_8"))

# get suggestions for keywords
# keyword = "もしかして"
# data = connector.get_suggestions(keyword)
# for i in data["default"]["topics"]:
# 	print(i["type"].encode("utf_8") + i["title"].encode("utf_8"))
