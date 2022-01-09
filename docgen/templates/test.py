# This file is part of osint.py program
# @lymbin 2021-2022

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

    def __init__(self, version, path, filename: str = ''):
        self.path = path
        self.filename = filename
        self.version = version

    def check_path(self, host):
        if self.filename == '' or os.path.exists(os.path.join(self.path, self.filename)):
            self.filename = '%s-%s.docx' % (host, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

    def generate(self, template: str, json):
        self.check_path(json['host'])

        path = template
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '%s.docx' % template)
        template = DocxTemplate(path)

        all_tech = []
        for tech in json['technologies']:
            all_tech.append(
                {
                    'tech_name': '%s %s' % (tech['name'], tech['version'])
                }
            )

        subdomains = []
        for domain in json['domains']:
            tech_domain = []
            for tech in domain['technologies']:
                tech_domain.append(
                    {
                        'tech_name': '%s %s' % (tech['name'], tech['version'])
                    }
                )
            subdomains.append(
                {
                    'subdomain_risk': domain['risk_level']['level'],
                    'subdomain_ip': domain['ip'],
                    'all_tech': tech_domain
                }
            )

        # Declare template variables
        context = {
            'version': self.version,
            'title': json['host'],
            'day': datetime.datetime.now().strftime('%d'),
            'month': datetime.datetime.now().strftime('%m'),
            'year': datetime.datetime.now().strftime('%Y'),
            'risk': json['risk_level']['level'],
            'cve_count': len(json['cve_list']),
            'critical_count': json['risks']['critical'],
            'high_count': json['risks']['high'],
            'medium_count': json['risks']['medium'],
            'exploits_count': json['risks']['exploits'],
            'all_tech': all_tech,
            'subdomains': subdomains,
            'image': ''
        }
        if json['risks']['exploits'] > 0:
            context['exploits'] = 'true'

        # Render automated report
        template.render(context)
        print(os.path.join(self.path, self.filename))
        template.save(os.path.join(self.path, self.filename))
