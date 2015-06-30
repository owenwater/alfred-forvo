#!/usr/bin/python

import os
import time
from workflow import Workflow


AGE = 3600 * 24
LOG = None


class Cache(object):
    LAST_CLEAN_TIME = 'last-clean-time'

    def __init__(self):
        global LOG
        self.wf = Workflow()
        LOG = self.wf.logger
        self.cachedir = self.wf.cachedir
        self.wf.cached_data_age = self.cached_data_age

    def cached_data_age(self, name):
        cache_path = self.wf.cachefile(name)
        if not os.path.exists(cache_path):
            return 0
        return time.time() - os.stat(cache_path).st_mtime

    def clean(self):
        if (Cache.LAST_CLEAN_TIME in self.wf.settings) and (time.time() - self.wf.settings[Cache.LAST_CLEAN_TIME] < AGE):
            return
        LOG.debug("cleaning cache file")
        for file in os.listdir(self.wf.cachedir):
            if file.endswith(".log") or file == "history.cpickle":
                continue
            if not self.wf.cached_data_fresh(file, AGE):
                LOG.debug("deleting cache file: " + file)
                os.remove(self.wf.cachefile(file))
        self.wf.settings[Cache.LAST_CLEAN_TIME] = time.time()


if __name__=="__main__":
    cache = Cache()
    cache.clean()
