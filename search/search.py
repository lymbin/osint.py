# This file is part of osint.py program
# @lymbin 2021-2022

import subprocess
import os
import json
from .setup import Configuration
"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'
cve_bin = os.path.join('bin', 'search.py')


class CveSearch:
    def __init__(self, cve_search_path: str):
        self.path = cve_search_path

    def search(self, cpe: str):
        if os.path.isabs(self.path):
            cve_search_bin = os.path.join(os.path.realpath(self.path), cve_bin)
        else:
            cve_search_bin = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.path, cve_bin)
        result = subprocess.run([cve_search_bin, '-p', cpe, '-o', 'json'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')


class Search:
    """
    Search CVE in cve-search database for package/version or cpe
    """
    def __init__(self):
        self.config = Configuration()

    def normalize(self, package: str) -> str:
        return package.lower()

    def parse(self, cve_search_result: str) -> str:
        result = []
        for cve_search_result_line in cve_search_result.splitlines():
            vuln = {}
            result_json = json.loads(cve_search_result_line)
            vuln['id'] = result_json['id']
            vuln['cvss'] = result_json['cvss']
            # vuln['summary'] = result_json['summary']  
            result.append(vuln)     
        return result

    def cve_search(self, cve_search_str: str) -> str:
        print('Scanning %s' % cve_search_str)
        cve_search_path = self.config.get_cve_path()
        result = CveSearch(cve_search_path).search(cve_search_str)
        result = self.parse(result)
        if not result:
            print('Nothing found')
        else:
            print("Found %d CVE(s)" % len(result))
        return result

    def search(self, package: str, ver: str) -> str:
        cve_search_str = ("%s:%s" % (self.normalize(package), ver))
        return self.cve_search(cve_search_str)

