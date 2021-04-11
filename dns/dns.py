# This file is part of osint.py program
# @lymbin 2021

import json
from .dnsdumpster import DnsDumpster

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'

class Dns:
    """
    Dns is a tool for getting dns records
    """
    def __init__(self):
        self.engines = {
            'DnsDumpster': DnsDumpster
        }
        
    def analyze(self, target: str, type = "hostsearch") -> str:
        """
        Method to get info from dns. 
        
        :param url: URL
        :Return: 
            `str`. json.dumps of `Wappalyzer.analyze_with_versions_and_categories`.
        """
        self.target = target
        results = ''
        for engine_name in self.engines.keys():
            print ('Using %s' % (engine_name))
            results = self.engines[engine_name]().dump(target, type)
        return (results)
        