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
        print('Scanning %s' % cve_search_str)
        cve_search_bin = os.path.join(os.path.realpath(self.config.get_cve_path()), cve_bin)
        result = subprocess.run([cve_search_bin, '-p', cve_search_str], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def search(self, package: str, ver: str) -> str:
        cve_search_str = ("%s:%s" % (package, ver))
        return self.cve_search(cve_search_str)
