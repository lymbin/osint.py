# This file is part of osint.py program
# @lymbin 2021-2022

import re
import os

from .Wappalyzer import Wappalyzer, WebPage
from .tech_updater import TechUpdater

"""
Changelog:

-- 0.5 --
Implements new method for resolve technology version(need test)

-- 0.4 --
Implements new update method
Revert 0.3 changes

-- 0.3 --
Added function for update file technologies.json. Moved to helper

-- 0.2 --
Added schema definition and setter

-- 0.1 --
Initial release

"""
version = '0.5'


class Tech:
    """
    Tech is a modified python-Wappalyzer wrapper.
    """

    def __init__(self):
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
        webpage = WebPage.new_from_url(self.url, timeout=60)
        results = wappalyzer.analyze_with_versions_and_categories(webpage)
        return results

    @staticmethod
    def update():
        TechUpdater.update(os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def init():
        TechUpdater.init(os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def clear():
        pass
