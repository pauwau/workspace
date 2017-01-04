#! /usr/bin/python
# -*- coding: utf-8 -*-

import twitter

api = twitter.Api(consumer_key='1liwbSXAMkK2NnKrpG3kjdUIj', consumer_secret='olprToxz6nmyhWWGOamAx195NDPFusJC9Kph825RpH6Ddc8886',
 access_token_key='4326378622-rQ6EIWlRar9EBH6vqos742d36lmf0iszmLyNnU5', access_token_secret='y76haBJQCdtatkGPAdzfHmwTYcrEgEhlIOSfCB8UmQWKN')

search="Python OR Twitter "
tweets = api.GetSearch(term=search, count=100,result_type='recent')
for tweet in tweets:
	print(tweet)