# This file is part of osint.py program
# @lymbin 2021-2022

import os
import configparser

runpath = os.path.dirname(os.path.realpath(__file__))

class Configuration:
    cp = configparser.ConfigParser()
    default = {'local': runpath}

    def __init__(self, default_path, config='config.ini'):
        self.default['local'] = default_path
        self.cp.read(os.path.join(runpath, config))

    @classmethod
    def read(self, section, item, default):
        result = default
        try:
            if type(default) == bool:
                result = self.cp.getboolean(section, item)
            elif type(default) == int:
                result = self.cp.getint(section, item)
            else:
                result = self.cp.get(section, item)
        except:
            pass
        return result

    @classmethod
    def get_cve_path(self):
        return self.read('Local', 'Path', self.default['local'])


def setup(path, update=True):
    pass
