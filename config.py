#!/usr/bin/python

import sys
import math

from workflow import Workflow

LOG = None

lang_file = "lang.json"

options=["lang", "num", "config"]
options_desc = {
    "lang" : u"Set search language",
    "num" : u"Set maximum number of words to be shown",
    "config" : u"Show config file",
}

class Config(object):
    SHOW_PREFIX = "show_"
    SEPARATOR = ":"

    def __init__(self, args):
        self.args = args.strip()

    def execute(self):
        global LOG
        wf = Workflow()
        self.wf = wf
        LOG = wf.logger
        sys.exit(wf.run(self.main))
    
    def main(self, wf):
        if self.args == "":
            self.show_options_menu(options)
        else:
            self.handle_args()
        
        self.wf.send_feedback()

    def handle_args(self):
        argv = self.args.split()
        show_options = filter(lambda option: option.startswith(argv[0]), options)


        if len(show_options) == 0:
            show_options = options
        elif len(show_options) == 1 and hasattr(self, Config.SHOW_PREFIX+argv[0]):
            getattr(self, Config.SHOW_PREFIX+argv[0])(' '.join(argv[1:]))
            return
        self.show_options_menu(show_options)
    
        

    def show_lang(self, arg):
        import json
        arg = unicode(arg, "utf-8")
        with open(lang_file) as fp:
            lang_list = json.load(fp)
        
        arg = arg.strip().lower()
        if arg == "":
            self.wf.add_item("Type to search the language (all for All Languages)")
            return 
        
        def lang_matched(lang):
            if lang["code"].startswith(arg) \
                or lang["lang"].lower().startswith(arg)  \
                or lang["native"].lower().startswith(arg) \
                or lang.get("native2", "").lower().startswith(arg):
                    return True
            return False

        lang_list = filter(lang_matched, lang_list)
        
        for lang in lang_list:
            self.wf.add_item(lang["lang"] + 
                             self._append_name(lang["native"]) + 
                             self._append_name(lang.get("native2", "")),
                             subtitle = lang["code"],
                             arg = self._generate_arg('lang', lang["code"]),
                             valid = True)


    def show_num(self, arg):
        try:
            value = int(arg)
            if value <= 0 or value > 100:
                self.wf.add_item("Value must be between 1 and 100")
            else:
                title = "Set to %d" %(value)
                self.wf.add_item(title, 
                                 arg = self._generate_arg('num', str(value)),
                                 valid = True)
        except ValueError:
            self.wf.add_item(options_desc['num'])

    def show_config(self, arg):
        self.wf.add_item("Open the config file", arg = "config", valid = True)

    def show_options_menu(self, options):
        for option in options:
            self.wf.add_item(options_desc[option],
                             subtitle = u"Current: ", #TODO + get current value
                             autocomplete = option + " ")

    def _append_name(self, str):
        if str == u"":
            return str
        else:
            return u" / " + str

    def _add_all_languages_item(self):
        self.wf.add_item("All Languages",
                        arg = "all",
                        valid = True)
                        
    def _generate_arg(self, key, value):
        return key + Config.SEPARATOR + value


if __name__=="__main__":
    config= Config(' '.join(sys.argv[1:]))
    config.execute()
