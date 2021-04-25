# This file is part of osint.py program
# @lymbin 2021

import os
import configparser

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'
runpath = os.path.dirname(os.path.realpath(__file__))


class Configuration:
    cp = configparser.ConfigParser()
    default = {'local': os.path.join(runpath, 'cve-search')}

    def __init__(self, config='config.ini'):
        self.cp.read(os.path.join(runpath, config))

    @classmethod
    def read(cls, section, item, default):
        result = default
        try:
            if type(default) == bool:
                result = cls.cp.getboolean(section, item)
            elif type(default) == int:
                result = cls.cp.getint(section, item)
            else:
                result = cls.cp.get(section, item)
        except:
            pass
        return result

    @classmethod
    def get_cve_path(cls):
        return cls.read('Local', 'Path', cls.default['local'])


def setup(path, update=True):
    pass
