#!/usr/bin/python

import sys
from forvo import ForvoGateway as Gateway
from workflow import Workflow
from config_loader import ConfigLoader
from config import user_file
from cache import Cache

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
                valid=True,
                autocomplete=item['word'])

    def _generate_arg(self, sound_url, word):
        import urllib
        arg = sound_url + u" " + forvo_url + u"word/" + urllib.quote(word.encode('utf-8'))
        if self.config.get('lang', 'all') != 'all':
            arg += "/#" + self.config['lang']
        return arg

    def _generate_subtitle(self, item):
        subtitle = "%s from %s, %s in %s pronunciation%s" %(
            item['language'],
            item['country'],
            item['rank'],
            item['num'],
            "s" if int(item['num']) > 1 else ""
        )
        return subtitle


if __name__=="__main__":
    m = Main(' '.join(sys.argv[1:]))
    m.execute()
