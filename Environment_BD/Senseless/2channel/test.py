#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twopy
import time

CYBER_CASCADE_KEYWORDS = [u"炎上", u"盗", u"飲酒", u"未成年", u"カンニング"]
WATCH_URLS = {
    u"poverty": u"http://engawa.2ch.net/poverty/",
    u"news4vip": u"http://hayabusa.2ch.net/news4vip/",
    u"news4viptasu": u"http://hayabusa3.2ch.net/news4viptasu/"}

def get_board(url):
    board = twopy.Board(url)
    print dir(board.retrieve.im_class.name.fget.func_name)
    print board.retrieve
    if board.retrieve() == 200:
        return board
    else:
        return None

def main():

    board = get_board(WATCH_URLS[u'poverty'])
    thread_list = [t for t in board if t.retrieve()[0] == 200]
    print thread_list
    for thread in thread_list:
        time.sleep(3)
        if (any([enjou_word in thread.title for enjou_word in CYBER_CASCADE_KEYWORDS])):
            comments = [comment for comment in thread if comment.number != 1001]
            f = open(thread.title + ".dat", "w")
            for comment in comments:
                f.write(comment.render())
                f.write("\n")
            f.close()
        else:
            pass

if __name__ == "__main__":
    main()