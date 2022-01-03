# This file is part of osint.py program
# @lymbin 2021-2022

import re

from .Wappalyzer import Wappalyzer, WebPage
from .updater import Updater

"""
Changelog:

-- 0.3 --
Added function for update file technologies.json

-- 0.2 --
Added schema definition and setter

-- 0.1 --
Initial release

"""
version = '0.3'


class Tech:
    """
    Tech is a modified python-Wappalyzer wrapper.
    """

    def __init__(self, update: bool = False):
        """
        :param update: Download and use the latest ``technologies.json`` file 
            from `AliasIO/wappalyzer <https://github.com/AliasIO/wappalyzer>`_ repository.  
        """
        if update:
            Updater.update()

        self.url = ""

    def analyze(self, url: str):
        """
        Method to analyze a website. 
        
        :param url: URL
        :Return: 
            `str`. json.dumps of `Wappalyzer.analyze_with_versions_and_categories`.
        """
        self.url = url
        schema = re.search(re.compile('^(http|https)://', re.I), self.url)
        if not schema:
            self.url = 'http://' + self.url

        print('Using Wappalyzer')
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(self.url)
        results = wappalyzer.analyze_with_versions_and_categories(webpage)
        return results
