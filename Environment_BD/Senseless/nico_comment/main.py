# -*- coding: utf-8 -*-

import conf
import GetVideoID
import GetComment
import DeleteColumn
import CommentToDeg
import NearCommentCount

# CategoryTagList = [u"エンターテイメント",u"音楽",u"歌ってみた",\
# u"演奏してみた",u"踊ってみた",u"VOCALOID",u"ニコニコインディーズ",\
# u"動物",u"料理",u"自然",u"旅行",u"スポーツ",u"ニコニコ動画講座",u"車載動画",u"歴史",\
# u"科学",u"ニコニコ技術部",u"ニコニコ手芸部",u"作ってみた",u"政治",\
# u"アニメ",u"ゲーム",u"東方",u"アイドルマスター",u"ラジオ",u"描いてみた",\
# u"例のアレ",u"その他",u"ファッション"
# ]

CategoryTagList = [u"アーマードコア",u"R-18",u"RPGツクール",u"アイドル",u"アイドルマスター",
u"iM@S架空戦記シリーズ",u"iM@SコラボPV",u"iM@SノーマルPV",u"アクション",u"あずさ",u"@BGM推奨",
u"アトラス",u"アニソン",u"AV（アニマルビデオ）",u"アニメ",u"アニメ色のない作業用BGM",u"アラド戦記",
u"ARI_PROJECT",u"アンインストール",u"アンケート",u"伊織",u"忙しい人向けシリーズ",u"癒し",
u"Wii",u"ヴィジュアル系",u"ｳｯーｳｯーｳﾏｳﾏ(ﾟ∀ﾟ)",u"歌ってみた",u"ウルトラマン",u"エアーマンが倒せない",
u"映画",u"映画part1集",u"エヴァンゲリオン",u"エースコンバット",u"FF",u"FF5",u"FF6",u"FF7",u"FF11",
u"エロ",u"エロゲ",u"エロゲソング",u"エロゲソングfull",u"演奏してみた",u"エンターテイメント",u"大神",
u"おっさんホイホイ",u"おっぱい",u"音げー",u"音ゲーMAD",u"描いてみた",u"踊ってみた",u"オブリビオン",
u"お笑い",u"音楽",u"カードビルダー"u"カービィ",u"描いてみた",u"替え歌",u"カオス",u"科学",u"鏡音リン",
u"鏡音レン",u"がくっぽいど",u"格闘ゲーム",u"画像",u"家庭教師ヒットマンREBORN！",u"カプコン",u"過保護動画",
u"神回",u"神画質",u"神曲",u"神ゲー",u"神MAD",u"仮面ライダー",u"カラオケ",u"完全に一致",u"ガンダム",u"ガンダム00",
u"ガンダムOO‐OPMADリンク",u"キシメン",u"ギター",u"期待の新人",u"ギタドラ",u"ギャグマンガ日和",u"キャラソン",
u"キングダムハーツ",u"組曲『ニコニコ動画』",u"クラシック",u"クレヨンしんちゃん",u"クロノトリガー",u"グロ注意",
u"ゲーム",u"ゲームOP",u"ゲーム音楽",u"GC",u"ゲームプレイpart1リンク",u"けしからん",u"幻想入りシリーズ",u"高画質",
u"公式が病気",u"コードギアス",u"コスプレ",u"コメント非表示推奨",u"これはひどい",u"サーフィン",u"才能の無駄遣い",
u"Sound_Horizon",u"作業用BGM",u"作者は病気シリーズ",u"サクラ大戦",u"サッカー",u"サドンアタック",u"サムネホイホイ",
u"さよなら絶望先生",u"自然",u"実況プレイ",u"実況プレイpart1リンク",u"実況プレイ動画",u"縛りプレイ",u"車載動画",
u"灼眼のシャナ",u"シュール",u"衝撃のラスト",u"笑撃のラスト",u"ジョジョの奇妙なソング集",u"女性実況part1リンク",
u"人類には早すぎる動画",u"SFC",u"スーパーファミコン",u"スーパープレイ",u"スーパーロボット大戦",u"涼宮ハルヒの憂鬱",
u"スパロボ",u"スポーツ",u"スマブラ",u"スマブラX",u"制限プレイ",u"政治",u"静止画MAD",u"セガ",u"セガサターン",u"ゼルダの伝説",
u"戦場の絆",u"創聖のアクエリオン",u"ソニック",u"その発想はなかった",u"その他",u"対戦動画",u"だいたいあってる",u"太鼓の達人",
u"ダウンタウン",u"TAS",u"弾いてみた",u"田村ゆかり",u"チート",u"地上に降りた天使達",u"千早",u"チャット",u"チャンネル桜",u"中国",
u"中日",u"ツーリング",u"ヅカリンク",u"作ってみた",u"突っ込みどころ満載",u"釣り",u"ツンデレ",u"DS",u"低画質",u"ディシディア",
u"テイルズ",u"出オチ",u"テクノ",u"デジモン",u"テスト",u"テニスの王子様",u"デビルメイクライ",u"天元突破グレンラガン",u"ドアラ",
u"動画",u"投稿者コメント",u"動物",u"東方",u"東方アレンジ",u"東方ヴォーカル",u"東方手書き劇場",u"東方を歌ってみた",
u"ドライブ",u"ドラえもん",u"ドラクエ",u"ドラクエ３",u"ドラクエ５",u"ドラゴンボール",u"トランスフォーマー",u"ドリームキャスト",
u"バイオハザード",u"バイオハザード4",u"バイオハザード5",u"バイク",u"パチスロ",u"パチンコ",u"発想の勝利",u"初音ミク",
u"バトレボ",u"ハヤテのごとく！",u"春香",u"ハレ晴れユカイ",u"ハロプロ",u"パワプロ",u"バンブラ",u"バンブラＤＸ",u"ピアノ",
u"PCエンジン",u"PCゲーム",u"BGM",u"B'z",u"PV",u"ひぐらしのなく頃に",u"必須アモト酸",u"ひとこと動画",u"一人で実況偉いね",
u"ひろくん",u"ファイアーエムブレム",u"ファイナルファンタジー",u"FC",u"ファミコン",u"フィギュアスケート",
u"吹いたら負け",u"風来のシレン",u"復/活BLリンク",u"腹筋崩壊",u"フリーゲーム",u"プレイ動画",u"PS",u"PS2",u"PS3",u"PSP",
u"プロレス",u"プロ野球",u"ベース",u"ヘッドフォン推奨",u"ヘッドホン推奨",u"ペルソナ",u"VOCALOID",u"VOCALOID3D化計画",
u"VOCALOIDカバー曲",u"VOCALOID-PV",u"ボカロオリジナルを歌ってみた",u"北斗の拳",u"ポケモン",u"星のカービィ",u"ポップン",
u"ホラー",u"マクロスF",u"真",u"混ぜるな危険",u"またお前か",u"マッシュアップ",u"ＭＡＤ",u"マリオ",u"マリオカート",u"マリオカートWii",
u"美希",u"ミクオリジナル曲",u"みなみけ",u"ミリしらシリーズ",u"メガドライブ",u"女神転生",u"巡音ルカ",u"メタル",
u"メタルギア",u"メドレー",u"萌えっ娘もんすたぁ",u"モータースポーツ",u"モーニング娘。",u"もっと評価されるべき",
u"モンスターハンター",u"闇のゲーム",u"やよい",u"U.N.オーエンは彼女なのか？",u"雪歩",u"ユーザーニコ割",
u"ライブ",u"らき☆すた",u"ラジオ",u"ランキング",u"リトルバスターズ！",u"料理",u"旅行",
u"リリカルなのは",u"リンオリジナル曲",u"例のアレ",u"歴史",u"レスリングシリーズ",u"レトロゲーム",u"ローゼンメイデン",
u"ロック",u"ロックマン",u"ロマサガ"]

if __name__ == '__main__':
	date = "10_27"
	ex = "ManyTag"
	output_db = "NiconicoComment" + ex + date + ".db"
	EachTagVideoNumber = 100
	index_tablename = "INDEX"
	CountFileName = "WordsCount" + ex + date + ".txt"
	CommentTextTableName = "CommentText"
	print("Begin make VideoID db!")
	GetVideoID.MakeVideoIDdb(output_db,EachTagVideoNumber,index_tablename,CategoryTagList)
	print("Begin make Comment db!")
	GetComment.InsertCommentdb(output_db,index_tablename)
	print("Begin make Delete Column!")
	DeleteColumn.DeleteColumn(output_db,index_tablename)
	print("Begin count comment")
	CommentToDeg.CountComment(output_db,index_tablename,CountFileName)
	print("Begin near comment count")
	NearCommentCount.NearCountComment(output_db,index_tablename,CountFileName,CommentTextTableName)
	print ("Succesed!!")