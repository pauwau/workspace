#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,string,random
import data_structure
import word2vec
frame_file = "text_to_frame/frame/ex2"
text_file = "text_to_frame/text/ex2"

def list_to_dist(read_dec,read_sub,topic):
    dist = 1
    print "selectedline = [dec: " + read_dec + ",",
    for i in read_sub:
        print i[0],"/",i[1],",",
    else:
        print "]"
    read_elements = [["dec",read_dec]]
    for each_sub in read_sub:
        read_elements.append(each_sub)
    topic_elements = [["dec",topic.dec]]
    for each_sub in topic.sub:
        topic_elements.append(list(each_sub))
        #print each_sub
    for topic_element in topic_elements:
        input_w2v = []
        if(topic_element[1] == "-"):
            continue
        temp_dist = 0
        for read_element in read_elements:
            if(read_element[1] == "-"):
                continue
            input_w2v.append(read_element[1] + " " + topic_element[1])
        dist_list = word2vec.distance(input_w2v)
        if(len(dist_list) == 0):
            continue
        #print dist_list
        temp_dist = float(max(dist_list))
        #print "dist = " + str(dist)
        print "read_element: " + str(read_element[1]) + " tempdist = " + str(temp_dist)
        dist = dist * temp_dist
    print "dist =" + str(dist)
    return dist

def frame_base(user_ID,topic):
    
    f = open(frame_file,"r") # 読み書きモードで開く
    lines = f.readlines() #情報を読み込む    
    #print sum(1 for line in lines)
    sum_readline = sum(1 for line in lines)
    max_dist = 0
    s = -1
    for select_line in lines:
        s += 1
        #print select_line
        search_dec = re.search(r"dec:([^\s:;/,]*)",select_line)
        search_sub = re.findall(r",([^\s:;/]*):([^\s:;/,]*)",select_line)
        #print str(search_dec.group(1))
        # for i in search_sub:
        #     print i[0],i[1]
        dist = list_to_dist(search_dec.group(1),search_sub,topic)

        if(dist > max_dist):
            max_dist = dist
            max_line = select_line
            max_s = s
    print "max_dist = " + str(max_dist)
    fl = open(text_file,"r")
    flines = fl.readlines()
    print flines[max_s]
    return max_dist

