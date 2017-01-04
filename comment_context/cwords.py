# -*- coding: utf-8 -*-
import MeCab
import re
import unicodedata


class Cleanser():

    def __init__(self):
        self.patUrl = re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")
        self.patXml = re.compile("<(\".*?\"|\'.*?\'|[^\'\"])*?>")
        sep = '[!-/:-@[-`{-~、◞⤴○▿゚д◟。♡٩ωو°！？（）〈〉【】『』／≦＜＼≧＞≪≫《》∀〔〕━──\n¥〜∵∴́ ❤⇒→⇔\│←↑↓┃★☆「」・♪～〓◆◇■□▽△▲●〇▼◎．”“※♥́́́]'

        self.patSep = re.compile(sep)

    def cleanseInput(self, string):
        cleansed = string
        cleansed = unicodedata.normalize('NFKC', cleansed)
        cleansed = cleansed.lower()
        cleansed = re.sub(self.patUrl, " ", cleansed)
        cleansed = re.sub(self.patXml, " ", cleansed)

        # 区切り文字として機能させたいのはこちら
        cleansed = re.sub(self.patSep, u'，', cleansed)

        cleansed = re.sub(re.compile(" +"), " ", cleansed)
        # cleansed = re.sub(re.compile("，+"),"，",cleansed)

        return(cleansed)

    def cleanseOutput(self, string):
        cleansed = string
        cleansed = re.sub(re.compile("[，  ]+"), " ", cleansed)
        # cleansed = re.sub(re.compile("[] +")," ",cleansed)

        return(cleansed)


class CompoundWords(MeCab.Tagger, Cleanser):

    def __init__(self, args='-Ochasen'):
        MeCab.Tagger.__init__(self, args)
        Cleanser.__init__(self)

    def wakati(self, sentence):
        p = self.parseToNode(self.cleanseInput(sentence))
        out = ['']

        while p:
            if p.surface == '，':
                p = p.next
                continue

            feature = tuple(p.feature.rsplit(','))
            if feature[0] == u'動詞' or feature[0] == u'形容詞':
                out.append(feature[6])
            else:
                out.append(p.surface)

            p = p.next

        while True:
            try:
                out.remove(u'')
            except:
                break

        return(out)

    def wakatic(self, sentence, topic=False):
        # if re.match('&lt',sentence):
        #     return()
        #sentence2 = sentence.decode("utf-8")
        p = self.parseToNode(self.cleanseInput(sentence))
        out = ['']

        init = True

        while p:
            # 文頭・文末の処理
            if init:
                print("sss")
                init = False
                out.append(p.surface)
                p = p.next
                if p == None:
                    break
                else:
                    continue

            else:
                print(p.prev.feature)
                feature_p = tuple(p.prev.feature.rsplit(','))
                feature = tuple(p.feature.rsplit(','))
                feature_n = tuple(p.feature.rsplit(','))

            # Skip condition
            if topic and (
                    feature[0] in [u'助詞', u'助動詞'] or
                    feature[1] == u'非自立' or
                    (feature[0] == u'動詞' and feature[1] == u'接尾')):
                p = p.next
                continue

            if p.surface == '，':
                p = p.next
                continue

            # 品詞が直前と同じでちょめちょめならくっつける,汚すぎるので近々メンテ

            cond = []
            cond.append(feature_p[0] == u'接頭詞')
            cond.append(feature[0] == u'名詞')

            cond.append(feature_p[0] == feature[0])
            cond.append(feature[0] not in [u'動詞', u'形容詞', u'接続詞', u'記号'])
            cond.append(feature[1] not in [u'非自立', u'数'])
            cond.append(feature_p[0] not in [u'記号'])
            cond.append(feature_p[1] not in [u'接尾', u'非自立', u'副詞可能'])
            cond.append(feature_p[1] != u'数' or feature[1] == u'接尾')
            cond.append(feature_p[2] != u'人名' or feature[1] == u'固有名詞')
            cond.append(feature_p[2] != u'人名' or feature[2] == u'人名')

            cond.append(feature_p[1] == u'数' and p.surface == u'月')
            cond.append(p.prev.surface in [u'明治',
                                           u'大正',
                                           u'昭和',
                                           u'平成'] and feature[1] == u'数')

            condJoin = (
                (cond[0] and cond[1]) or
                (cond[2] and cond[3] and cond[4] and cond[5] and
                 cond[6] and cond[7] and cond[8] and cond[9]) or
                cond[10] or
                cond[11]
            )

            if condJoin:
                out.append(out.pop() + p.surface)

            else:
                if feature[0] == u'動詞' or feature[0] == u'形容詞':
                    out.append(feature[6])
                else:
                    out.append(p.surface)

            # print(p.surface + ':' + p.feature) #ぷりんとでばっぐ
            # 空白を削除する
            p = p.next

        while True:
            try:
                out.remove(u'')
            except:
                break

        return(out)

if __name__ == '__main__':
    import cwords
    cw = cwords.CompoundWords()
    txt = u'''伊藤 清（いとう きよし、1915年9月7日 - 2008年11月10日）は、日本の数学者。
    確率論における伊藤の補題（伊藤の定理）の考案者として知られる。
    大戦中の1942年に、伊藤の補題で知られる確率微分方程式を生み出した。
    確率積分を計算する上で重要な伊藤の公式（伊藤ルール）
    は米国科学アカデミーによって、以下の様に評価されている[3]。
    '''
    words = cw.wakatic(txt)

    print(words)