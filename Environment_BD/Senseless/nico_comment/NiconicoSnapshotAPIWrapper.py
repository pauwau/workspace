# -*- coding: utf-8 -*-

import requests
import json
import time
import collections

class NiconicoSnapshotAPIWrapper(object):
    endpoint = 'http://api.search.nicovideo.jp/api/snapshot/'
    endpoint_last_modified = 'http://api.search.nicovideo.jp/api/snapshot/version'
    
    Result = collections.namedtuple('NiconicoSnapshotAPIResult', 'total hits errid')
    default_result = Result(None, None, None)
    
    def __init__(self, issuer, **default_parameter):
        self.default_parameter = {
            'service': ['video'],
            'search': ['title', 'description', 'tags'],
            'join': 'cmsid title description tags start_time thumbnail_url view_counter comment_counter mylist_counter last_res_body length_seconds'.split()
        }
        self.default_parameter.update(default_parameter)
        self.default_parameter['issuer'] = issuer
        
    def getLastModified(self):
        return requests.get(self.endpoint_last_modified).json()['last_modified']
    
    def makeFilterEqual(self, field, value):
        ret = {}
        ret['type'] = 'equal'
        ret['field'] = field
        ret['value'] = value
        return ret
    
    def makeFilterRange(self, field, start = None, end = None, include_lower = True, include_upper = True):
        ret = {}
        ret['type'] = 'range'
        ret['field'] = field
        if start is not None:
            ret['from'] = start
        if end is not None:
            ret['to'] = end
        ret['include_lower'] = include_lower
        ret['include_upper'] = include_upper
        return ret
    
    def query(self, query, retry = 1, wait = 1, **kwargs):
        parameter = self._makeQueryParameter(query, kwargs)
        for i in xrange(retry):
            r = requests.post(u'http://api.search.nicovideo.jp/api/snapshot/', json=parameter)
            if r.status_code == requests.codes.ok:
                break
            else:
                time.sleep(wait)
        if r.status_code != requests.codes.ok:
            print r
        return self._parseResponse(r.text)
    
    def _makeQueryParameter(self, query, kwargs):
        parameter = self.default_parameter.copy()
        parameter['query'] = query
        parameter.update(kwargs)
        
        return parameter
    
    def _parseResponse(self, response):
        ret = {}
        for i, line in enumerate(response.splitlines()):
            data = json.loads(line)
            if 'endofstream' in data:
                continue
            if 'errid' in data:
                return self.default_result._replace(errid = data['errid'])
            if 'type' not in data:
                return self.default_result._replace(errid = -1)
            if data['type'] == 'stats':
                ret['total'] = data['values'][0]['total']
            if data['type'] == 'hits':
                ret['hits'] = data['values']
        return self.default_result._replace(**ret)
