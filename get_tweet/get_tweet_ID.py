#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys, json
import time,sqlite3

file_name = "temp.txt"
api_array = [###########################################↓hayashi
	['1liwbSXAMkK2NnKrpG3kjdUIj',\
	'olprToxz6nmyhWWGOamAx195NDPFusJC9Kph825RpH6Ddc8886',\
	'4326378622-rQ6EIWlRar9EBH6vqos742d36lmf0iszmLyNnU5',\
	'y76haBJQCdtatkGPAdzfHmwTYcrEgEhlIOSfCB8UmQWKN'\
	],##################################################↓nakano
	['abdSqsCIFP0hkRBnjnqz6taLV',\
	'uOqiCNL7bp9F8azFqi1QXLWMaKSvW5jPqfqCFsbflIBrIfhvYw',\
	'2920831586-aUN1viWkEoNpVxa2JuJwvtpyJuZJcWWp2NNNEvv',\
	'wWc8uu9h9HMYN7Ebfl3war1EOgRM4AGFQ8oLcXnLCEghw'
]]

conn = sqlite3.connect("tweet_anything.db")
cur = conn.cursor()

def get_no(num):
	no = str(range(num,num + 100))
	no = no.replace(" ","")
	no = no.replace("]","")
	no = no.replace("[","")
	return no

def get_tweet(no,api_index):
	#print no
	api_key = api_array[api_index][0]
	api_secret = api_array[api_index][1]
	access_token = api_array[api_index][2]
	access_token_secret = api_array[api_index][3]

	#no = "418033807850496002,418036745247006720"
	p = subprocess.Popen(['php',"tweetid2json.php",no,api_key,api_secret,access_token,access_token_secret],
	                        stdout=subprocess.PIPE,
	                        )
	#print ("num:" + api_key)
	raw_tweet = p.stdout
	return raw_tweet

def json_vector(tweet):
	tweet_id = tweet['id']
	tweet_str = '\\n'.join(tweet['text'].split('\n'))
	tweet_str = tweet_str.replace("\'","")
	tweet_str = tweet_str.replace("’","")
	user = tweet['user']
	user_id = user['id']
	tweet_lang = tweet['lang']
	tweet_rep = tweet['in_reply_to_status_id']
	if((tweet_rep) == None):
		tweet_rep = 0
	return [tweet_id,tweet_str,user_id,tweet_lang,tweet_rep]

if __name__ == '__main__':
	f = open(file_name, 'r')
	linearray = f.readlines()
	begining_num = int(linearray[0][linearray[0].find(":") + 1:].replace("\n",""))
	get_tweet_num = int(linearray[1][linearray[1].find(":") + 1:].replace("\n",""))
	try:
		cur.execute("""CREATE TABLE tweet(tweet_id serial,sentence text,\
			user_ID serial,lang text,in_reply_to_status_id serial);""")
	except sqlite3.OperationalError:
		pass

	num = begining_num
	
	while(1):
		try:
			for api_index,hoge in enumerate(api_array):
				f = open(file_name, 'w')
				no = get_no(num)
				raw_tweets = get_tweet(no,api_index)
				for tag in raw_tweets:
					#print tag
					try:
						tweets = json.loads(tag)
					except(ValueError):
						continue
					for tweet in tweets:
						if 'text' in tweet:
							[tweet_id,tweet_str,user_id,tweet_lang,tweet_rep] = json_vector(tweet)
							cur.execute("""INSERT INTO \
							tweet(tweet_id,sentence,user_ID,lang,in_reply_to_status_id) \
							VALUES(%d,'%s',%d,'%s',%d)""" \
							%(tweet_id,tweet_str,user_id,tweet_lang,tweet_rep))
							print(str(get_tweet_num) + " tweet were found")
				num = num + 100
				print ("id:" + str(num) + " process is finished")
				f.write("begining_num:" + str(num) + "\ntweet_num:" + str(get_tweet_num) + "\n")
				f.close()
			time.sleep(6)
			conn.commit()
		except KeyboardInterrupt:
			print "accept KeyboardInterrupt"
			break
	print "process end"
	conn.close()




