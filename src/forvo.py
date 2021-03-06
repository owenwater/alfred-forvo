#!/usr/bin/python

import sys
from workflow import web
from config import options
from error import GatewayException
from types import ListType

url_tem = "http://apifree.forvo.com/key/%s/format/json"
lang_tem = "/language/%s"
action_tem = "/action/%s"
pagesize_tem = "/pagesize/%s"
search_tem = "/search/%s"

word_search_action = "pronounced-words-search"

LOG = None


class ForvoGateway(object):

    expire_time = 7200
    timeout = 7

    def __init__(self, config, wf):
        key = config['key']
        self.lang = config.get('lang', options['lang']['default'])
        self.num = config.get('num', options['num']['default'])
        self.url = self._generate_url(key, self.lang, self.num)

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

        if int(pagesize) < int(self.num) and int(total) > int(pagesize):
            # not enough entry be loaded and there're more remaine
            response = self._send_word_search_request(word)
            self.wf.cache_data(name_key, response)

        return self._parse_json(response['items'])

    def _parse_json(self, items):
        def parse(item):
            parsed_item = {}
            parsed_item['word'] = item['original']
            parsed_item['word_link'] = item['word']
            parsed_item['num'] = item['num_pronunciations']
            pronunciation = item['standard_pronunciation']
            parsed_item['language'] = pronunciation['langname']
            parsed_item['sound'] = pronunciation['pathmp3']
            parsed_item['country'] = pronunciation['country']
            parsed_item['rank'] = str(pronunciation['num_positive_votes']) + " up votes"
            return parsed_item
        return [parse(item) for item in items]
            
    def _send_word_search_request(self, word):
        count = 0
        error_msg = ""
        while count < 3:
            count += 1

            try:
                search = search_tem %(word)
                action = action_tem %(word_search_action)

                request_url = self.url + action + search

                response = self._send_request(request_url).json()
                if type(response) == ListType:
                    error_msg = response[0]
                    raise GatewayException(error_msg)
                total = response['attributes']['total']
                if total is None:
                    LOG.debug("ERROR: total is None")
                else:
                    return response
            except GatewayException:
                raise
            except Exception as e:
                LOG.exception(e)
                error_msg = str(e)

        raise GatewayException(error_msg)

    def _generate_name_key(self, key, search):
        return key + "_" + search + "_" + self.lang

    def _send_request(self, url):
        LOG.debug("sending url: " + url)
        response = web.get(url, timeout=ForvoGateway.timeout)
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
    from config_loader import ConfigLoader
    config = ConfigLoader("config/user.json")
    #config = {
        #'lang':'all',
        #'num':'10',
        #'key':'6d47687b9aa5ee0354a4b37bef25f570',
    #}
    gw = ForvoGateway(config, Workflow())
    r = gw.word_search(unicode(sys.argv[1], 'utf-8'))
    print r
