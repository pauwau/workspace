#!/usr/bin/python
# -*- coding: utf-8 -*-
# python_twitter 1.1
import twitter
from twitter import Api
import sys
import time
import re
reload(sys)
sys.setdefaultencoding('utf-8')
from collections import defaultdict
import time,sqlite3
import datetime
import MeCab

low_limit_wordnum = 6
high_limit_wordnum = 30

output_db = "tweet_wordnum_1229_100k.db"

# since:2012-10-01 until:2012-10-31 をリクエストにして送ると、期間指定のツイートを取得できる

maxcount=100000
maxid =0
terms=[\
#格助詞
u"が",u"の",u"を",u"に",u"へ",u"と",u"から",u"より",u"で",u"や"\
#並立助詞
u"か",u"まで",u"だけ",u"ほど",u"くらい",u"など",u"も",\
#係助詞
u"は"
]
PoPOS = ["名詞","動詞","形容詞"]
stop_list = ["n",u"こと"]
search_str=" OR ".join(terms)
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


def atmarkDelete(sentence):
  sentence = re.sub(r'@[0-9a-zA-Z_]+', " ", sentence)
  return sentence

if __name__ == '__main__':
  dicPath = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
  tagger = MeCab.Tagger ("-Owakati -d "+dicPath)
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
          POS_num = 0
          [tweet_id,tweet_str,user_id,tweet_lang,tweet_rep] = make_vector(f)
          if(tweet_rep == 0):
            continue
          tweet_str = tweet_str.replace("'","")
          tweet_str = tweet_str.replace("' ","")
          atmarkDelete_str = atmarkDelete(tweet_str)
          node = tagger.parseToNode(atmarkDelete_str.encode('utf-8'))
          char_flag = True
          while node:
            if node.feature.split(",")[0] in PoPOS and not node.surface in stop_list:
              POS_num = POS_num + 1
            # if node.feature.split(",")[1] == u"固有名詞":
            #   char_flag = False
            node = node.next
          try:
            if(POS_num > low_limit_wordnum and POS_num < high_limit_wordnum and char_flag):
              cur.execute("""INSERT INTO \
              tweet(tweet_id,sentence,user_ID,lang,in_reply_to_status_id) \
              VALUES(%d,'%s',%d,'%s',%d)""" \
              %(tweet_id,tweet_str,user_id,tweet_lang,tweet_rep))
              ins_num = ins_num + 1
          except sqlite3.OperationalError as e:
            print "sqlite3 OperationalError occured:" + str(e.message)
            continue
        if len(found) == 0:
          print "found == 0"
          break
        if maxcount <= ins_num:
          print "maxcount <= ins_num"
          print "process end"
          exit()
        #print (maxid)
        if(ins_num > 100 * partition_num):
          conn.commit()
          print ("commit")
          partition_num = partition_num + 1
      print str(ins_num) + " element were found"

  print ("-----------------------------------------\n")
  rate = api.GetRateLimitStatus()
  print ("Limit %d / %d" % (rate['resources']['search']['/search/tweets']['remaining'],rate['resources']['search']['/search/tweets']['limit']))
  tm = time.localtime(rate['resources']['search']['/search/tweets']['reset'])
  print ("Reset Time  %d:%d" % (tm.tm_hour , tm.tm_min))