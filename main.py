#!/usr/bin/python

import sys
from forvo import ForvoGateway as Gateway
from workflow import Workflow
from config_loader import ConfigLoader
from config import user_file
from error import GatewayException
from cache import Cache

LOG = None

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
            self.wf.send_feedback()
        except Exception as e:
            self.wf.add_item("Forvo API seems down, please try again later", 
                            subtitle = "Error: " + str(e),)
            self.wf.send_feedback()
        #cleanup

        cache = Cache()
        cache.clean()

    def _add_items(self, items):
        for item in items:
            self.wf.add_item(
                item['word'],
                subtitle = self._generate_subtitle(item),
                arg = item['sound'],
                valid = True,
                autocomplete = item['word']
                )


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

