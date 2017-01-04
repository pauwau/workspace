# -*- coding: utf-8 -*-

import urllib2, cookielib
from urlparse import parse_qs
import re

class NiconicoCommentGetter:
	def __init__(self,username,password):
		cj = cookielib.CookieJar()              # Cookieを格納するオブジェクト
		cjhdr = urllib2.HTTPCookieProcessor(cj) # Cookie管理を行うオブジェクト
		self.opener = urllib2.build_opener(cjhdr)    # OpenDirectorオブジェクトを返す
		self.opener.open("https://secure.nicovideo.jp/secure/login","mail=%s&password=%s" % (username,password) )

	# return 値はstr_list int_listのzipされたリスト	
	def get(self,smID):
		# smIDからthreadIDの取得
		r = self.opener.open('http://flapi.nicovideo.jp/api/getflv/' + smID)
		html = r.read()
		res = parse_qs(urllib2.unquote(html))		
		
		# threadIDからコメントxmlの取得
		r = self.opener.open("%sthread?version=20090904&thread=%s&res_from=-1000"\
		 % (res['ms'][0],res['thread_id'][0]) )
		xml = r.read()

		# コメントのパース(無理やり，仕様変わってダメになるかも)
		comments = []
		vposs = []
		commentrm = re.compile(">(.*)</chat")
		vposrm = re.compile("vpos=\"(\d+)\"")
		for line in xml.split('><') :
			commentg = commentrm.search(line)
			vposg = vposrm.search(line)
			if( commentg != None ) : comments.append(commentg.group(1))
			if( vposg != None ) : vposs.append(int(vposg.group(1)))
		return zip(comments,vposs)

