# -*- coding: utf-8 -*-

from NiconicoSnapshotAPIWrapper import *
import time

CategoryTagList = [\
u"エンターテイメント",u"音楽",u"歌ってみた",\
u"演奏してみた","踊ってみた","VOCALOID","ニコニコインディーズ",\
u"動物",u"料理",u"自然",u"旅行",u"スポーツ",u"ニコニコ動画講座",u"車載動画",u"歴史",\
u"科学",u"ニコニコ技術部",u"ニコニコ手芸部",u"作ってみた",u"政治",\
u"アニメ",u"ゲーム",u"東方",u"アイドルマスター",u"ラジオ",u"描いてみた",\
u"例のアレ",u"その他",u"ファッション"]
# if __name__ == '__main__':
# #issuer(アプリ名)を指定してください
#     api = NiconicoSnapshotAPIWrapper('NiconicoSnapshotAPIWrapper')#
# #単純な使い方(検索結果の内1件だけ取得)
#     result = api.query(u'東方', size = 1)
#     print u'件数: {}, 結果: {}'.format(result.total, result.hits)
# #件数だけ取得
#     print api.query(u'東方', size = 0).total
# #5回までリトライする(リトライの間には1秒開ける)
#     api.query(u'東方', retry = 5, wait = 1, size = 0).total
# #パラメータを指定する
#     print api.query(u'東方', size = 1, sort_by = 'mylist_counter').hits[0]['last_res_body']
# #フィルタのパラメータはJSONを与えないといけない
#     print api.query('東方', size = 0, filters=[{'type': 'range', 'field': 'start_time', 'from': '2014-01-01 00:00:00'}])
# #フィルタの指定のヘルパー関数
#     print api.query('東方', size = 0, filters=[api.makeFilterRange('start_time', '2014-01-01 00:00:00')])
# #データの更新日時の取得(AM5:00の時点のスナップショットをその日の何時に切り替えたか)
#     print api.getLastModified()

if __name__ == '__main__':
	api = NiconicoSnapshotAPIWrapper('NiconicoSnapshotAPIWrapper')
	for CategoryTag in CategoryTagList:
		time.sleep(1)
		response  = api.query(CategoryTag,size = 1, sort_by = 'comment_counter')
		print response[1][0][u"cmsid"]