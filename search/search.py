# This file is part of osint.py program
# @lymbin 2021

from pycvesearch import CVESearch
from .setup import Configuration
"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'


class Search:
    """
    Search CVE in cve-search database for package/version or cpe
    """
    def __init__(self):
        self.config = Configuration()
        web_interface = "http://%s:%s"%(self.config.getCVESearch())
        self.cve = CVESearch(web_interface)
        
    def cpe_search(self, cpe: str) -> str:
        return self.cve.cvefor(cpe)

    def search(self, package: str, version: str) -> str:
        pass
