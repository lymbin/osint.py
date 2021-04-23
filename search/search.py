# This file is part of osint.py program
# @lymbin 2021

import subprocess
import os
from .setup import Configuration
"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'
cve_bin = os.path.join('bin', 'search.py')


class Search:
    """
    Search CVE in cve-search database for package/version or cpe
    """
    def __init__(self):
        self.config = Configuration()

    def cve_search(self, cve_search_str: str) -> str:
        pass

    def search(self, package: str, version: str) -> str:
        pass
