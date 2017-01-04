#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,string,random
import data_structure

def topic_base(topic):
	if not (topic[0].sub == "null"):
		print (topic[0].sub + "が" + topic[0].dec + "と仰っていましたね。")
	else:
		print (topic[0].dec + "と仰っていましたね。")