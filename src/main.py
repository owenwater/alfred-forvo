#!/usr/bin/python

import sys
from forvo import ForvoGateway as Gateway
from workflow import Workflow
from config_loader import ConfigLoader
from config import user_file
from cache import Cache
from history import History

LOG = None
LINE = unichr(0x2500) * 20

forvo_url = u"http://www.forvo.com/"


class Main(object):
    def __init__(self, args):
        self.args = unicode(args.strip(), 'utf-8')
        self.config = ConfigLoader(user_file, True)

    def execute(self):
        global LOG
        wf = Workflow()
        self.wf = wf
        LOG = wf.logger
        sys.exit(wf.run(self.main))

    def main(self, wf):
    
        history = History(wf)
        if self.args == u'':
            self._show_history(history.get_history())
            return

        try:
            gateway = Gateway(self.config, wf)
            items = gateway.word_search(self.args)
            self._add_items(items)
            self._add_logo()
        except Exception as e:
            self.wf.add_item("Forvo API seems down, please try again later",
                             subtitle="Error: " + str(e),)

        self.wf.send_feedback()

        # cleanup
        cache = Cache()
        cache.clean()

    def _add_logo(self):
        self.wf.add_item(LINE,
                         subtitle="Pronunciations by Forvo",
                         arg=forvo_url,
                         valid=True,
                         icon="image/blank.png")

    def _add_items(self, items):
        for item in items:
            self.wf.add_item(
                item['word'],
                subtitle=self._generate_subtitle(item),
                arg=self._generate_arg(item['sound'], item['word_link']),
                modifier_subtitles={'cmd':'open ' + self._generate_word_url(item['word_link'], quote=False)},
                valid=True,
                autocomplete=item['word'])

    def _generate_arg(self, sound_url, word):
        arg = sound_url + u" " + self._generate_word_url(word)
        return arg

    def _generate_word_url(self, word, quote=True):
        import urllib
        url = forvo_url + u"word/" + (urllib.quote(word.encode('utf-8')) if quote else word)
        if self.config.get('lang', 'all') != 'all':
            url += "/#" + self.config['lang']
        return url



    def _generate_subtitle(self, item):
        subtitle = "%s from %s, %s in %s pronunciation%s" %(
            item['language'],
            item['country'],
            item['rank'],
            item['num'],
            "s" if int(item['num']) > 1 else ""
        )
        return subtitle

    def _show_history(self, history_list):
        if not history_list:
            self.wf.add_item('Please enter your words')
        else:
            for history in history_list:
                self.wf.add_item(history, 
                                 valid=False,
                                 autocomplete=history)
                
            self.wf.add_item(u"- History List -",
                             valid=False,
                             icon="image/blank.png")

        self.wf.send_feedback()

if __name__=="__main__":
    m = Main(' '.join(sys.argv[1:]))
    m.execute()
