#!/usr/bin/python

import sys
from workflow import web

url_tem = "http://apifree.forvo.com/key/%s/format/json"
lang_tem = "/language/%s"
action_tem = "/action/%s"
pagesize_tem = "/pagesize/%s"
search_tem = "/search/%s"

word_search_action = "pronounced-words-search"

LOG = None

class ForvoGateway(object):

    expire_time = 7200

    def __init__(self, config, wf):
        key = config['key']
        lang = config['lang']
        self.num = config['num']
        self.url = self._generate_url(key, lang, self.num)

        self.wf = wf
        global LOG
        LOG = wf.logger

    def word_search(self, word):
        name_key = self._generate_name_key(word_search_action, word)
        response = self.wf.cached_data(name_key, 
                                       lambda: self._send_word_search_request(word),
                                       max_age=ForvoGateway.expire_time)

        total = response['attributes']['total']
        pagesize = response['attributes']['pagesize']

        if total == None:
            #total is None means there's error in response
            import json
            LOG.debug("ERROR: total is None")
            LOG.debug("response: ")
            LOG.debug(json.dumps(response, indent=2))

            #clean error cache
            self.wf.cache_data(name_key, None) 

            #we still return what we got

        elif int(pagesize) < int(self.num) and int(total) > int(pagesize): 
            #not enough entry be loaded and there're more remaine
            response = self._send_word_search_request(word)
            self.wf.cache_data(name_key, response)

        return response['items']

    def _send_word_search_request(self, word):
        search = search_tem %(word)
        action = action_tem %(word_search_action)

        request_url = self.url + action + search

        response = self._send_request(request_url).json()
        return response

    def _generate_name_key(self, key, search):
        return key + "_" + search


    def _send_request(self, url):
        LOG.debug("sending url: "+url)
        
        response = web.get(url)
        response.raise_for_status()
        return response

    def _generate_url(self, key, lang, num):
        url = url_tem %(key)
        if lang != 'all':
            url += lang_tem %(lang)
        url += pagesize_tem %(num)
        return url
        


if __name__=="__main__":
    from workflow import Workflow
    config = {
        'lang':'all',
        'num':'10',
        'key':'6d47687b9aa5ee0354a4b37bef25f570',
    }
    gw = ForvoGateway(config, Workflow())
    r = gw.word_search(unicode(sys.argv[1], 'utf-8'))
    print r
