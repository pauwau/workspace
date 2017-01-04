# -*- coding: utf-8 -*-

from lxml.html import fromstring
from urllib.request import urlopen
from collections import Counter, defaultdict
import MeCab

mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
url = 'http://wc2014.2ch.net/test/read.cgi/sci/1343188288/'
doc = fromstring(urlopen(url).read().decode('cp932', errors='ignore'))


# タイトル
print(doc.head.find('title').text, url, sep='\n')
print()

# IDのカウント
ids = Counter([data.text_content().split('ID:')[-1].split()[0] for data in doc.findall('.//dt')])
print('全レス数：%d, 全ID数：%d' % (len(list(doc.findall('.//dd'))), len(ids)))
for i, id in enumerate(sorted(ids.items(), key=lambda x:x[1], reverse=True)[:10]):
    print('{0:2d}. ID:{1:15s} ({2:3d} 回)'.format(i+1, id[0], id[1]))
print()

# 頻出ワードのカウント
word_count = defaultdict(int)
is_kanji = lambda c: True if '一' <= c <= '龠' else False
ignore_str0 = "ch,彡ﾉｼ丶ﾞﾞﾐll丿,あと，こと,ない"  # ある文字列がこの中に完全に含まれたら無視する
ignore_list2 = ['接尾', '数', 'サ変接続', '代名詞', '非自立']  # 無視する品詞の種類
for comment in doc.findall('.//dd'):
    text = comment.text_content()
    # URLの除去
    for link in comment.iterlinks():
        text = text.replace(link[0].text_content(), '')

    result = mecab.parse(text)
    words = [word.replace('\t',',').split(',') for word in result.split('\n')[:-2]]
    for word in words:
        if word[1] in ['名詞', '形容詞']:
            # 一文字のワードは漢字だけカウントする
            if len(word[0])==1 and not is_kanji(word[0]):
                continue
            if word[0] in ignore_str0 or word[2] in ignore_list2:
                continue
            # print(word)
            word_count[word[0]] += 1

    
for i, word in enumerate(sorted(word_count.items(), key=lambda x:x[1], reverse=True)[:30]):
    print('{0:2d}: {1:s} ({2:d})'.format(i+1, word[0], word[1]), end=('　' if (i+1)%3 else '\n'))

