#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
u"""Docomoの雑談対話APIを使ってチャットできるスクリプト
"""
 
import sys
import urllib2
import json
import datetime

todaydetail  =    datetime.datetime.today()
date = (str(todaydetail.month) + "_" + str(todaydetail.day) + "_" + str(todaydetail.hour) + "_" + str(todaydetail.minute))

APP_URL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue'
fw = open("taiwalog_" + date + ".txt","w")
 
class DocomoChat(object):
    u"""Docomoの雑談対話APIでチャット"""
 
    def __init__(self, api_key):
        super(DocomoChat, self).__init__()
        self.api_url = APP_URL + '?APIKEY=%s'%(api_key)
        self.context, self.mode = None, None
 
    def __send_message(self, input_message='', custom_dict=None):
        req_data = {'utt': input_message}
        if self.context:
            req_data['context'] = self.context
        if self.mode:
            req_data['mode'] = self.mode
        if custom_dict:
            req_data.update(custom_dict)
        request = urllib2.Request(self.api_url, json.dumps(req_data))
        request.add_header('Content-Type', 'application/json')
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            sys.exit()
        return response
 
    def __process_response(self, response):
        resp_json = json.load(response)
        self.context = resp_json['context'].encode('utf-8')
        self.mode    = resp_json['mode'].encode('utf-8')
        return resp_json['utt'].encode('utf-8')
 
    def send_and_get(self, input_message):
        response = self.__send_message(input_message)
        received_message = self.__process_response(response)
        return received_message
 
    def set_name(self, name, yomi):
        response = self.__send_message(custom_dict={'nickname': name, 'nickname_y': yomi})
        received_message = self.__process_response(response)
        return received_message
 
 
def main():
    api_key = '564f5a7a34756c7a422f31644633622e6e64327169326c452f2f433045332e6c3559727351307763656a42'
    chat = DocomoChat(api_key)
    resp = chat.set_name('pau', 'ぱう')
    print '相手　 : %s'%(resp)
    fw.write("s:" + resp + "\n")
    message = ''
    while (message != 'バイバイ' or message != "ばいばい" or message != "exit"):
        message = raw_input('あなた : ')
        fw.write("u:" + message + "\n")
        resp = chat.send_and_get(message)
        print '相手　 : %s'%(resp)
        fw.write("s:" + resp + "\n")
 
 
if __name__ == '__main__':
    main()