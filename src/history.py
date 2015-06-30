#!/usr/bin/python
# encoding: utf-8

NO_EXPIRE = 0
NUM_OF_HISTORY = 20
HISTORY = "history"

class History(object):

    def __init__(self, wf):
        self.wf = wf
        self._load()
    
    def add_history(self, new_word):
        
        #deduplicate
        try:
            self.history.remove(new_word) 
        except ValueError:
            pass
        
        #add and maintina history length
        self.history.insert(0, new_word)
        self.history = self.history[:NUM_OF_HISTORY]
        self._save()

    def get_history(self):
        return self.history


    def _load(self):
        self.history = self.wf.cached_data(HISTORY,
                                      lambda: [],
                                      NO_EXPIRE)

    def _save(self):
        self.wf.cache_data(HISTORY, self.history)


if __name__ == "__main__":
    import sys
    from workflow import Workflow
    h = History(Workflow())
    print h.get_history()
    h.add_history(sys.argv[1] if len(sys.argv) > 1 else '' )
    print h.get_history()
    print '=' * 20

