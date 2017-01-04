#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,string,random
#import data_structure
#import word2vec

def frame_base(user_ID,topic):
    frame_file = "ex" + str(user_ID) + ".txt"
    f = open(frame_file,"r") # 読み書きモードで開く
    lines = f.readlines() #情報を読み込む    
    #print sum(1 for line in lines)
    sum_readline = sum(1 for line in lines)
    if(sum_readline == 0):
        ran = 0
    else:
        ran = random.randint(0,sum_readline) - 1 # ignore topic frame

    print ran
    select_line = lines[ran]
    dist = 1
    #print select_line
    search_dec = re.search(r"dec:([^\s:;/,]*)",select_line)
    search_sub = re.findall(r",([^\s:;/]*):([^\s:;/,]*)",select_line)
    #print str(search_dec.group(1))
    # for i in search_sub:
    #     print i[0],i[1]
    if not search_dec == None:
        read_dec = search_dec.group(1)
        read_sub = search_sub
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
        for read_element in read_elements:
            if(read_element[1] == "-"):
                continue
            temp_dist = 0
            for topic_element in topic_elements:
                print topic_element
                print read_element
                if(topic_element[1] == "-"):
                    continue
                read_dist = word2vec.distance(read_element[1] + " " + topic_element[1])
                print read_dist
                if(read_dist > temp_dist):
                    temp_dist = read_dist
                    print "temp_dist updated"
            dist = dist * temp_dist
            print "dist = " + str(dist)
    else:
        dist = 0
    print "dist =" + str(dist)
    return dist
