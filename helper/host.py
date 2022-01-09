# This file is part of osint.py program
# @lymbin 2021-2022

import socket
from urllib.parse import urlparse
from .parser import parse_from_hostsearch
from .risk import RiskResolver


class Host:
    """
    Host is a object with results
    """

    def __init__(self, target: str):
        netloc = '{uri.netloc}'.format(uri=urlparse(target))
        if netloc != '':
            self.target = netloc
        else:
            self.target = '{uri.path}'.format(uri=urlparse(target))
        self.info = {}
        self.json = {'host': self.target,
                     'ip': '',
                     'risk_level': {
                         'score': 100,
                         'level': 'Low'
                     },
                     'risks': {
                         'critical': 0,
                         'high': 0,
                         'medium': 0,
                         'low': 0,
                         'exploits': 0
                     },
                     'technologies': [],
                     'cve_list': [],
                     'domains': []
                     }
        try:
            self.ip = socket.gethostbyname(self.target)
            self.dns = self.target + ',' + self.ip
            self.json['ip'] = self.ip
        except Exception as e:
            print('Failed to gethostbyname. Reason: %s' % e)

    """
    Parse hostsearch from dns
    :param data: dns's hostsearch result
    """
    def hostsearch(self, data: str):
        self.dns = data
        self.info = parse_from_hostsearch(self.dns)
        if len(data) > 1 and self.target not in self.info:
            self.info[self.target] = {
                'ip': self.ip
            }
            for hostname in self.info:
                if hostname == ('www.%s' % self.target):
                    del self.info[hostname]
                    break
        for hostname in self.info:
            ip = self.info[hostname]['ip']
            self.info[hostname] = {
                'ip': ip,
                'tech': {}
            }

    def generate_results(self):
        for hostname in self.info:
            domain = {'host': hostname,
                      'ip': self.info[hostname]['ip'],
                      'risk_level': {
                          'score': 100,
                          'level': 'Low'
                      },
                      'risks': {
                          'critical': 0,
                          'high': 0,
                          'medium': 0,
                          'low': 0,
                          'exploits': 0
                      },
                      'technologies': [],
                      'cve_list': []
                      }
            self._fill_domain(domain, self.info[hostname]['tech'])
            self.json['domains'].append(domain)

            for cve in domain['cve_list']:
                self.json['cve_list'].append(cve)
            for tech in domain['technologies']:
                if tech not in self.json['technologies']:
                    self.json['technologies'].append(tech)
            for risk in domain['risks']:
                self.json['risks'][risk] += domain['risks'][risk]

        self.json['risk_level'] = self.calc_risk(self.json['risks'], self.json['risks']['exploits'])

    def _fill_domain(self, domain, tech):
        for tec in tech:
            domain['technologies'].append(
                {
                    'name': tec,
                    'version': tech[tec]['version']
                }
            )
            if 'vulns' in tech[tec]:
                for vuln in tech[tec]['vulns']:
                    cve = {
                        'id': vuln['id'],
                        'cvss': vuln['cvss']
                    }
                    domain['cve_list'].append(cve)
                    severity = self.calc_severety(vuln)
                    domain['risks'][severity] += 1

                    if 'exploits' in vuln:
                        domain['risks']['exploits'] += len(vuln['exploits'])
        domain['risk_level'] = self.calc_risk(domain['risks'], domain['risks']['exploits'])
        return domain
    """
    Reformat tech item in json
    """
    def reformat_tech(self):
        for hostname in self.info:
            tech = self.info[hostname]['tech']
            for tec in tech:
                tech[tec]['version'] = ''
                tech[tec]['vulns'] = {}
                if tech[tec]['versions']:
                    tech[tec]['version'] = tech[tec]['versions'][0]
                del tech[tec]['versions']

    @staticmethod
    def calc_severety(cve):
        if 'cvss' in cve:
            return RiskResolver.calc_cve_severity(cve['cvss'])
        else:
            return RiskResolver.calc_cve_severity(cve)

    @staticmethod
    def calc_risk(risks, exploits):
        return RiskResolver.calc_risk(risks, exploits)
