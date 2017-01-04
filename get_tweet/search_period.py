#!/usr/bin/python
# -*- coding: utf-8 -*-
# python_twitter 1.1
import twitter
from twitter import Api
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from collections import defaultdict
import time,sqlite3
import datetime

output_db = "tweet_period_725.db"

# since:2012-10-01 until:2012-10-31 をリクエストにして送ると、期間指定のツイートを取得できる

maxcount=100000
maxid =0
period = " since:2016-7-18 until:2016-7-25"
terms=["これ","ここ",\
"こっち","こいつ","この","こう","こんな"\
"それ","そこ","そっち","そいつ","その","そう","そんな"\
"あれ","あそこ","あっち","あいつ","あの","ああ","あんな"\
"どれ","どこ","どっち","どいつ","どの","どう","どんな"\
]
search_str = terms
search_str = " OR ".join(terms)
search_str = search_str + " " + period
conn = sqlite3.connect(output_db)
cur = conn.cursor()

api1 = Api(base_url="https://api.twitter.com/1.1",
                  consumer_key='1liwbSXAMkK2NnKrpG3kjdUIj',
                  consumer_secret='olprToxz6nmyhWWGOamAx195NDPFusJC9Kph825RpH6Ddc8886',
                  access_token_key='4326378622-rQ6EIWlRar9EBH6vqos742d36lmf0iszmLyNnU5',
                  access_token_secret='y76haBJQCdtatkGPAdzfHmwTYcrEgEhlIOSfCB8UmQWKN')
api2 = Api(base_url="https://api.twitter.com/1.1",
                  consumer_key='abdSqsCIFP0hkRBnjnqz6taLV',
                  consumer_secret='uOqiCNL7bp9F8azFqi1QXLWMaKSvW5jPqfqCFsbflIBrIfhvYw',
                  access_token_key='2920831586-aUN1viWkEoNpVxa2JuJwvtpyJuZJcWWp2NNNEvv',
                  access_token_secret='wWc8uu9h9HMYN7Ebfl3war1EOgRM4AGFQ8oLcXnLCEghw')
api_list = [api1,api2]
def make_vector(tweet):
  tweet_id = tweet.id
  tweet_str = '\\n'.join(tweet.text.split('\n'))
  user = tweet.user
  user_id = user.id
  tweet_lang = tweet.lang
  tweet_rep = tweet.in_reply_to_status_id
  if((tweet_rep) == None):
    tweet_rep = 0
  return [tweet_id,tweet_str,user_id,tweet_lang,tweet_rep]



if __name__ == '__main__':
  partition_num = 1
  try:
    cur.execute("""CREATE TABLE tweet(tweet_id serial,sentence text,\
      user_ID serial,lang text,in_reply_to_status_id serial);""")
  except sqlite3.OperationalError:
    cur.execute("DROP TABLE tweet")
    cur.execute("""CREATE TABLE tweet(tweet_id serial,sentence text,\
      user_ID serial,lang text,in_reply_to_status_id serial);""")
  rate = api1.GetRateLimitStatus()
  print ("Limit %d / %d" % (rate['resources']['search']['/search/tweets']['remaining'],rate['resources']['search']['/search/tweets']['limit']))
  d = datetime.datetime.now()
  tm = time.localtime(rate['resources']['search']['/search/tweets']['reset'])
  print ("Reset Time  %d:%d" % (tm.tm_hour , tm.tm_min))
  print ("-----------------------------------------\n")
  i = 0
  ins_num = 0
  while True:
    time.sleep(6)
    for api in api_list:
      try:
        found = api.GetSearch(term=search_str,count=100,result_type='recent',max_id=maxid-1)
      except twitter.error.TwitterError as e:
        print "twitter error occured:" + str(e.message)
        if(int(e[0][0]['code']) == 88):
          temp_tm = (tm.tm_hour * 60) + tm.tm_min
          d_tm = (int(d.strftime("%H")) * 60) + int(d.strftime("%M"))
          sleep_time = (int(temp_tm) - int(d_tm))*60 + 10
          print str(sleep_time) + "sec sleep..."
          time.sleep(sleep_time)
        continue
      for f in found:
        if maxid > f.id or maxid == 0:
          maxid = f.id
          [tweet_id,tweet_str,user_id,tweet_lang,tweet_rep] = make_vector(f)
          if(tweet_rep == 0):
            continue
          tweet_str = tweet_str.replace("'","")
          tweet_str = tweet_str.replace("' ","")
          try:
            cur.execute("""INSERT INTO \
            tweet(tweet_id,sentence,user_ID,lang,in_reply_to_status_id) \
            VALUES(%d,'%s',%d,'%s',%d)""" \
            %(tweet_id,tweet_str,user_id,tweet_lang,tweet_rep))
            ins_num = ins_num + 1
          except sqlite3.OperationalError as e:
            print "sqlite3 OperationalError occured:" + str(e.message)
            continue
        i = i + 1
        if len(found) == 0:
          print "found == 0"
          break
        if maxcount <= i:
          print "maxcount <= i"
          print "process end"
          exit()
        #print (maxid)
        if(i > 100 * partition_num):
          conn.commit()
          print ("commit")
          partition_num = partition_num + 1
      print str(ins_num) + " element were found"

  print ("-----------------------------------------\n")
  rate = api.GetRateLimitStatus()
  print ("Limit %d / %d" % (rate['resources']['search']['/search/tweets']['remaining'],rate['resources']['search']['/search/tweets']['limit']))
  tm = time.localtime(rate['resources']['search']['/search/tweets']['reset'])
  print ("Reset Time  %d:%d" % (tm.tm_hour , tm.tm_min))