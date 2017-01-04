# -*- coding: utf-8 -*-
import urllib2, cookielib
from urlparse import parse_qs
import re

f = open("comment.xml","w")


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
		
		f.write(xml)

		# コメントのパース(無理やり，仕様変わってダメになるかも)
		comments = []
		vposs = []
		threads = []
		commentrm = re.compile(">(.*)</chat")
		vposrm = re.compile("vpos=\"(\d+)\"")
		threadrm = re.compile("thread=\"(\d+)\"")
		for line in xml.split('><') :
			commentg = commentrm.search(line)
			vposg = vposrm.search(line)
			threadg = threadrm.search(line)
			if( commentg != None ) : comments.append(commentg.group(1))
			if( vposg != None ) : vposs.append(int(vposg.group(1)))
			if( threadg != None ) : threads.append(int(threadg.group(1)))
		return zip(comments,vposs,threads)

if __name__ == '__main__':
	commentGetter = NiconicoCommentGetter("ii.mmi.twitter@gmail.com","TOKI8\\nari")
	comment_status = commentGetter.get("sm7")
	comment_status = sorted(comment_status, key=lambda x: x[1])
	for comment,vpos,thread in comment_status:
		print comment + " " + str(vpos) + " " + str(thread)
