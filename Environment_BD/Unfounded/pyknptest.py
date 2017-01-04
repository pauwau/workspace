#-*- encoding: utf-8 -*-
from pyknp import KNP
import sys
import codecs
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# Use KNP in subprocess mode
knp = KNP()
# if you don't need case analysis
# knp = KNP(option='-dpnd -tab')
result = knp.parse(u"太郎は歌舞伎町の風俗街で豪遊しているので、夜の帝王と呼ばれている。")

f = open("test.txt","w")

print ("##########bunsetsu###########")
# print(dir(result.bnst_list()[0]))
# print(dir(result.tag_list()[0]))
# print(dir(result.mrph_list()[0]))
# ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_mrph_list', '_tag_list', 'bnst_id', 'children', 'dpndtype', 'fstring', 'mrph_list', 'parent', 'parent_id', 'push_mrph', 'push_tag', 'repname', 'spec', 'tag_list']
# childrenの返り値はlist
# parentの返り値はbnst
# ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_mrph_list', 'children', 'dpndtype', 'fstring', 'mrph_list', 'parent', 'parent_id', 'push_mrph', 'repname', 'spec', 'synnodes', 'tag_id']
# ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'bunrui', 'bunrui_id', 'doukei', 'fstring', 'genkei', 'hinsi', 'hinsi_id', 'imis', 'katuyou1', 'katuyou1_id', 'katuyou2', 'katuyou2_id', 'midasi', 'mrph_id', 'push_doukei', 'push_imis', 'repname', 'repnames', 'spec', 'yomi']


# # loop for bunsetsu
for bnst in result.bnst_list():
    # print u"ID:%s, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%s, 素性:%s" \
    # % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring)
    # print u"ID:%s, 見出し:%s,children:%s"\
    # %(bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()),"".join(str(x.bnst_id) for x in bnst.children))
    # print u"ID:%s, 見出し:%s,parent:%s"\
    # %(bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()),bnst.parent.bnst_id)
    for mrph in bnst.mrph_list():
        print (u"sent:%s, hinsi:%s"%(mrph.midasi,mrph.hinsi))

# print ("##########tag###########")
# # loop for tag (kihonku, basic phrase)
# for tag in result.tag_list():
#     print u"ID:%s, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%s, 素性:%s" \
#     % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring)

# print ("##########mrph###########")
# # loop for mrph
# for mrph in result.mrph_list():
#     print u"見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
#     % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname)

# Read from file
# data = ""
# with open("result.knp") as file_in:
#     for line in file_in:
#         data += line.decode('utf-8')
#         if line.strip() == "EOS":
#             result = knp.result(data)
#             print ",".join(mrph.genkei for mrph in result.mrph_list())
#             data = ""