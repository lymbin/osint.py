# This file is part of osint.py program
# @lymbin 2021-2022

import subprocess
import os
import json
from .setup import Configuration
from .search_update import SearchUpdater
from .search_optimizer import SearchOptimizer

"""
Changelog:
-- 0.4 --
Optimize search implementation

-- 0.3 --
Implements new update method
Revert 0.2

-- 0.2 --
Change default path of cve-search

-- 0.1 --
Initial release

"""
version = '0.4'
cve_bin = os.path.join('bin', 'search.py')


class CveSearch:
    def __init__(self, cve_search_path: str):
        self.path = cve_search_path

    def search(self, cpe: str):
        if os.path.isabs(self.path):
            cve_search_bin = os.path.join(os.path.realpath(self.path), cve_bin)
        else:
            cve_search_bin = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.path, cve_bin)
        try:
            result = subprocess.run([cve_search_bin, '-p', cpe, '-o', 'json'], stdout=subprocess.PIPE)
        except FileNotFoundError:
            print("cve-search not found on path: %s. "
                  "Install cve-search with \"osint.py --init\" command" % cve_search_bin)
            return ''
        return result.stdout.decode('utf-8')


class Search:
    """
    Search CVE in cve-search database for package/version or cpe
    """
    def __init__(self):
        self.config = Configuration()

    @staticmethod
    def parse(cve_search_result: str):
        result = []
        if cve_search_result != '':
            for cve_search_result_line in cve_search_result.splitlines():
                vuln = {}
                result_json = json.loads(cve_search_result_line)
                vuln['id'] = result_json['id']
                vuln['cvss'] = result_json['cvss']
                # vuln['summary'] = result_json['summary']
                result.append(vuln)
        return result

    def cve_search(self, cve_search_str: str):
        print('Scanning %s' % cve_search_str)
        cve_search_path = self.config.get_cve_path()
        result = CveSearch(cve_search_path).search(cve_search_str)
        result = self.parse(result)
        if not result:
            print('Nothing found')
        else:
            print("Found %d CVE(s)" % len(result))
        return result

    def search(self, package: str, ver: str):
        package = SearchOptimizer.optimize(package)
        cve_search_str = ("%s:%s" % (package, ver))
        return self.cve_search(cve_search_str)

    @staticmethod
    def update():
        SearchUpdater.update(os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def init():
        SearchUpdater.init(os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def clear():
        pass
