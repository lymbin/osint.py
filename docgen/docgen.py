# This file is part of osint.py program
# @lymbin 2021-2022

import os
import datetime
from jinja2 import Template, Environment, FileSystemLoader

"""
Changelog:

-- 0.2 --
Moved to HTML Generation via jinja2

-- 0.1 --
Initial release

"""
version = '0.2'


class Html:
    """
    Html used for generate html from results
    """
    def __init__(self, ver, path, filename: str = ''):
        self.templates = {
            'test': 'test.jinja'
        }
        self.path = path
        self.filename = filename
        self.version = ver
        self.env = Environment(loader=FileSystemLoader('templates'))

    def check_path(self, host):
        if self.filename == '' or os.path.exists(os.path.join(self.path, self.filename)):
            self.filename = '%s-%s.html' % (host, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

    def generate(self, template_name: str, json):
        if template_name not in self.templates.keys():
            print("No template with name %s found in templates directory." % template_name)
            return
        else:
            print('Using template %s' % template_name)

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
        template = self.env.get_template(self.templates[template_name])
        print(os.path.join(self.path, self.filename))
        parsed_template = template.render(context)
        with open(self.filename, "w") as fn:
            fn.write(parsed_template)

