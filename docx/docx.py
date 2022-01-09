# This file is part of osint.py program
# @lymbin 2021-2022

from .templates.test import TestTemplate

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'


class Docx:
    """
    Docx used for generate docs from results
    """
    def __init__(self):
        self.templates = {
            'test': TestTemplate
        }
        
    def generate(self, template: str, json):
        if template not in self.templates.keys():
            print("No template with name %s found in templates directory." % template)
            return
        else:
            print('Using template %s' % template)
            self.templates[template]().generate(template, json)
