#!/usr/bin/python
# -*- coding: utf-8 -*-
# python_twitter 1.1
import twitter,sys
from twitter import Api
reload(sys)
sys.setdefaultencoding('utf-8')
from collections import defaultdict
import time,sqlite3,datetime,subprocess,json,datetime
read_db = "tweet_wordnum_726_100k.db"
output_db = "tweet_wordnum_729_100k_dia.db"
dialogue_num_highlimit = 15

api1 = ['1liwbSXAMkK2NnKrpG3kjdUIj',
        'olprToxz6nmyhWWGOamAx195NDPFusJC9Kph825RpH6Ddc8886',
        '4326378622-rQ6EIWlRar9EBH6vqos742d36lmf0iszmLyNnU5',
        'y76haBJQCdtatkGPAdzfHmwTYcrEgEhlIOSfCB8UmQWKN']
api2 = ['abdSqsCIFP0hkRBnjnqz6taLV',
        'uOqiCNL7bp9F8azFqi1QXLWMaKSvW5jPqfqCFsbflIBrIfhvYw',
        '2920831586-aUN1viWkEoNpVxa2JuJwvtpyJuZJcWWp2NNNEvv',
        'wWc8uu9h9HMYN7Ebfl3war1EOgRM4AGFQ8oLcXnLCEghw']
api_list = [api1,api2]
class tweet:
	def __init__(self):
		self.tweet_ID = 0
		self.sentence = ""
		self.user_ID = 0
		self.repfrom = 0
		self.repto = 0
		#"12345678,23456789,34567890"
		self.idstr = ""
		#reference_flag
		self.ref_flag = False
		self.uttnum = 0

	def initialize():
		self.tweet_ID = 0
		self.sentence = ""
		self.user_ID = 0
		self.repfrom = 0
		self.repto = 0
		self.idstr = ""
		self.ref_flag = False
		self.uttnum = 0

#make class_array
def init_class_array(cur):
	class_array = []
	db_list = cur.fetchmany(100)
	for i in range(0,100):
		new_instance = tweet()
		class_array.append(new_instance)
		[class_array[i].tweet_ID,class_array[i].sentence,\
		class_array[i].user_ID,class_array[i].repfrom,class_array[i].repto,\
		class_array[i].idstr] = \
		[db_list[i][0],db_list[i][1],db_list[i][2],0,db_list[i][4],str(db_list[i][0])]
	#print class_array
	return class_array

def class_array_set(cur,a_class):
	try:
		db_tuple = cur.fetchone()
	except IndexError:
		print next_cur
		print "Error : out of index"
		end_flag = True
		return end_flag
	try:
		[a_class.tweet_ID,a_class.sentence,\
		a_class.user_ID,a_class.repfrom,a_class.repto,\
		a_class.idstr] = \
		[db_tuple[0],db_tuple[1],db_tuple[2],0,db_tuple[4],str(db_tuple[0])]
	except:
		pass
	return False


def get_tweet(get_no,api_index):
	api_key = api_list[api_index][0]
	api_secret = api_list[api_index][1]
	access_token = api_list[api_index][2]
	access_token_secret = api_list[api_index][3]

	#get_no = "418033807850496002,418036745247006720"
	p = subprocess.Popen(['php',"tweetid2json.php",get_no,api_key,api_secret,access_token,access_token_secret],
	                        stdout=subprocess.PIPE,
	                        )
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

def update_class(tweet_id,tweet_str,user_id,tweet_lang,tweet_rep,class_array,cur):
	for a_class in class_array:
		if(tweet_id == a_class.repto):
			insert_db(a_class,cur)
			a_class.repfrom = a_class.tweet_ID
			a_class.tweet_ID = tweet_id
			a_class.sentence = tweet_str
			a_class.user_ID = user_id
			a_class.repto = tweet_rep
			a_class.idstr = a_class.idstr + "," + str(tweet_id)
			a_class.ref_flag = True
			a_class.uttnum = a_class.uttnum + 1
			if(a_class.repto == 0 or a_class.uttnum > dialogue_num_highlimit):
				a_class.repto = 0
				insert_db(a_class,cur)
				a_class.ref_flag = False
				a_class.uttnum = 0
			break
	return

def insert_db(a_class,cur):
	try:
		cur.execute("""INSERT INTO \
		dialogue(tweet_id,sentence,user_ID,repfrom,repto,idstr) \
		VALUES(%d,'%s',%d,%d,%d,'%s')""" \
		%(a_class.tweet_ID,a_class.sentence,a_class.user_ID,\
			a_class.repfrom,a_class.repto,a_class.idstr))
	except sqlite3.OperationalError as e:
		print "sqlite3 OperationalError occured:" + str(e.message)
	except:
		print "something error occured when db insert"

def check_ref(class_array):
	notref_indexes = []
	for i in range(0,100):
		if(class_array[i].ref_flag == False):
			notref_indexes.append(i)
		else:
			class_array[i].ref_flag = False
	return notref_indexes

if __name__ == '__main__':
	#reset_time = time.time
	conn = sqlite3.connect(read_db)
	sconn = sqlite3.connect(output_db)
	cur = conn.cursor()
	scur = sconn.cursor()

	try:
		scur.execute("""CREATE TABLE dialogue(tweet_id serial,sentence text,\
			user_ID serial,repfrom serial,repto serial,idstr text);""")
	except sqlite3.OperationalError:
		scur.execute("DROP TABLE dialogue")
		scur.execute("""CREATE TABLE dialogue(tweet_id serial,sentence text,\
			user_ID serial,repfrom serial,repto serial,idstr text);""")

	#array has 100 tweet class
	cur.execute( "select * from tweet LIMIT 100 OFFSET 0" )	
	class_array = init_class_array(cur)
	next_cur = 100
	end_flag = False
	commit_num = 0
	while(not end_flag or not end2_flag):
		#一つでも取得予定のnumberがあれば、end2_flagはFalse
		end2_flag = True
		for api_index in range(0,len(api_list) - 1 ):
			get_no = ""
			#print class_array[2].sentence
			for a_class in class_array:
				if(get_no == ""):
					get_no = str(a_class.repto)
				elif(not end_flag):
					get_no = get_no + "," + str(a_class.repto)
					end2_flag = False
				else:
					if(a_class.ref_flag == False):
						pass
					else:
						get_no = get_no + "," + str(a_class.repto)
						end2_flag = False
			#print get_no
			raw_tweets = get_tweet(get_no,api_index)
			for tag in raw_tweets:
				try:
					tweets = json.loads(tag)
				except(ValueError):
					continue
				for tweet in tweets:
					if 'text' in tweet:
						[tweet_id,tweet_str,user_id,tweet_lang,tweet_rep] = json_vector(tweet)
						#update class
						update_class(tweet_id,tweet_str,user_id,tweet_lang,tweet_rep,class_array,scur)
			notref_indexes = check_ref(class_array)
			for notref_index in notref_indexes:
				cur.execute( "select * from tweet LIMIT 1 OFFSET " + str(next_cur) )	
				end_flag = class_array_set(cur,class_array[notref_index])
				next_cur = next_cur + 1
####
		# elapsed_time = reset_time - time.clock
		# time.sleep(elapsed_time)
		# reset_time = time.time
####
		time.sleep(6)
		sconn.commit()
		print "next_cur :" + str(next_cur)
	print "process finished"
	try:
		cur.execute("""CREATE TABLE has_reply AS SELECT * FROM tweet WHERE repto = 0 ;""")
	except sqlite3.OperationalError:
		cur.execute("DROP TABLE has_reply")
		cur.execute("""CREATE TABLE has_reply AS SELECT * FROM tweet WHERE repto = 0 ;""")
	exit()