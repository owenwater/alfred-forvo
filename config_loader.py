#!/usr/bin/python

import json


class ConfigLoader(object):

    def __init__(self, path, create_if_fail=False):
        self.path = path
        try:
            with open(path) as fp:
                self.config = json.load(fp)
        except IOError:
            if create_if_fail:
                self.config = {}
                self.save()

    def __getitem__(self, key):
        return self.config[key]
    
    def __contains__(self, key):
        return key in self.config

    def get(self, key, default_value=None):
        return self[key] if key in self else default_value
    
    def __setitem__(self, key, value):
        self.config[key] = value

    def save(self):
        with open(self.path, "w") as fp:
            json.dump(self.config, fp, indent=2)

    def __str__(self):
        return str(self.config)

    def save_item(self, arg, separator):
        key, _, value = arg.partition(separator)
        self[key] = value
        self.save()


if __name__=="__main__":
    cl = ConfigLoader("config/user.json", True)
    cl.save_item("lang:zh", ":")
    cl.save_item("num 23", ":")
