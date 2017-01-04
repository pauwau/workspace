#! /usr/bin/python
# -*- coding:utf-8 -*-

class info:
    def __init__(self,sub,dec):
        """
        文節、基本句、形態素の情報が格納されている
        基本句ごとの情報を格納する
        """
        
        self.sub = sub
        self.dec = dec