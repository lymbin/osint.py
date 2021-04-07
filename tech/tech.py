"""This File is part osint.py program"""
import argparse
import json
from .Wappalyzer import Wappalyzer, WebPage

class Tech:
    def __init__(self, update: bool = False):
        self.update = update
    
    def analyze(self, url: str) -> str:
        self.url = url
        wappalyzer = Wappalyzer.latest(update=self.update)
        webpage = WebPage.new_from_url(self.url)
        results = wappalyzer.analyze_with_versions_and_categories(webpage)
        return (json.dumps(results))
        