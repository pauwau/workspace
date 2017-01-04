# -*- coding: utf-8 -*-
'''
Created on 2015/12/19

@author: mori
'''
import sqlite3
import re
from datetime import datetime
import unicodedata

#顔文字除去用パターン
face_pattern = ur'(?:[^0-9A-Za-zぁ-ヶ一-龠]|[ovっつ゜ニノ三二])*[(∩꒰（](?!(?:[0-9A-Za-zぁ-ヶ一-龠]|[ｦ-ﾟ]){3,}).{3,}[)∩꒱）](?:[^0-9A-Za-zぁ-ヶ一-龠]|[ovっつ゜ニノ三二])'
#絵文字除去用パターン
_au         = ur'\ue468-\ue5df\uea80-\ueb88'
_docomo     = ur'\ue63e-\ue6a5\ue6ac-\ue6ae\ue6b1-\ue6ba\ue6ce-\ue757'
_softbank   = ur'\ue001-\ue05a\ue101-\ue15a\ue201-\ue253\ue301-\ue34d\ue401-\ue44c\ue501-\ue537'
_emobile    = ur'%s\ue600-\ue619' % _docomo
_toGetFollower = ur'(.*(拡散|募集|相互|支援|sougo|rt|RT|ＲＴ|follow|フォロ|ﾌｫﾛ|１００|100|％|%)){3,}'
au      = re.compile(u'[%s]' % _au)
docomo  = re.compile(u'[%s]' % _docomo)
softbanck = re.compile(u'[%s]' % _softbank)
emobile = re.compile(u'[%s]' % _emobile)
toGetFollower = re.compile(ur'[%s]'% _toGetFollower)

# createSqlStr = 'create table tweetData (id, id_str, truncated, retweeted, favorite_count, in_reply_to_status_id_str, entities, retweet_count, in_reply_to_user_id, place, favorited, source, contributors, in_reply_to_screen_name, in_reply_to_user_id_str, user, lang, text, created_at, in_reply_to_status_id, is_quote_status, geo, coordinates)'
createSqlStr = 'create table tweetData (id,in_reply_to_status_id,user,text,created_at)'     #作成するDBの構成

# conn = sqlite3.connect("/home/mori/workspace/EvalWillingnessbyCosSim/data/tweetDataTsuji015.db")
conn = sqlite3.connect("/home/mori/workspace/SubUserIDinSqlite/tweetData_withoutBot.db")    #フィルタリングを掛ける対象となるDB
cur = conn.cursor()

conn2 = sqlite3.connect("../tweetData_filtered2.db")    #作成するDB名およびその保存場所
cur2 = conn2.cursor()
cur2.execute(createSqlStr)

# limitNum = 37545
# limitNum = 206551
limitNum = 860000
offset = 0

print datetime.now().strftime('%Y/%m/%d %H:%M:%S')
# maxNum = 37545
# maxNum = 206551
maxNum = 860000
while offset<maxNum:
    cur.execute('''SELECT id,in_reply_to_status_id,user,text,created_at FROM tweetData LIMIT ? OFFSET ?''',(limitNum,offset))
    
    tweetList = []
    cntDel = 0
    for row in cur:
        if re.match(ur'((^[^@].*?)@)|((^[@].+?)@)',row[3]): #複数リプおよびQTの削除?
            cntDel +=1
        else:
            text = re.sub(ur'(@[^\s]+?)\s|(\n)', '', row[3])
            text = unicodedata.normalize('NFKC',text) #NFKC正規化
            text = re.sub(face_pattern, '', text)   #顔文字除去
            text = au.sub('',text)                  #絵文字除去
            text = docomo.sub('',text)              #絵文字除去
            text = softbanck.sub('',text)           #絵文字除去
            text = emobile.sub('',text)             #絵文字除去
            text = re.sub(ur'(https?[\w|/|:|%|#|$|&|\?|\(|\)|~|\.|=|\+|\-]+?)','',text)   #URL除去
#             text = toGetFollower.sub('',text)       #フォロワ獲得系ツイート
            text = re.sub(ur'(\s+?)\s','', text)    #不必要な空白除去
            text = re.sub(ur'(ww+?)w', '', text)  #芝刈り
            text = re.sub(ur'(([!-/:-@[-`{-~]+?)[!-/:-@[-`{-~])', '', text)  #複数記号刈り
            row = list(row)
            row[3] = text
            tweetList.append(row)            
    cur2.executemany('''INSERT INTO tweetData VALUES (?,?,?,?,?)''', tweetList)
    conn2.commit()
#     offset += limitNum - cntDel
    offset += limitNum
    print "DelNum: " + str(cntDel)
    print "OFFSET: " + str(offset)
#     if offset%1000 == 0:
    print datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    
    
conn.close()
conn2.close()


