# This file is part of osint.py program
# @lymbin 2021-2022

import datetime
import os
import random
import datetime
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm, Inches, Mm, Emu


class TestTemplate:
    """
    Test template used for generate docs from results with test.docx template
    """

    def __init__(self):
        pass

    def generate(self, template: str, json):
        path = template
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '%s.docx' % template)
        template = DocxTemplate(path)

        # Declare template variables
        context = {
            'title': title,
            'day': datetime.datetime.now().strftime('%d'),
            'month': datetime.datetime.now().strftime('%b'),
            'year': datetime.datetime.now().strftime('%Y'),
            'risk ': table_contents,
            'image': image
        }
