# This file is part of osint.py program
# @lymbin 2021

from .dnsdumpster import DnsDumpster

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'


class Dns:
    """
    Dns is a helpful tool for getting dns records for domains
    """
    def __init__(self):
        self.engines = {
            'DnsDumpster': DnsDumpster
        }
        self.target = ""
        
    def analyze(self, target: str, data_type="hostsearch") -> str:
        """
        Method to get info from dns. 
        
        :param target: URL
        :param data_type: type of data to return (default hostsearch - returns only domains and ips)
        :Return: 
            `str`. row with all subdomains and ips or dns json
        """
        self.target = target
        results = ''
        for engine_name in self.engines.keys():
            print('Using %s' % engine_name)
            results = self.engines[engine_name]().dump(target, data_type)
        return results
