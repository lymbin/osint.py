# This file is part of osint.py program
# @lymbin 2021-2022

import argparse
import json
import socket
import sys
import time
import re

from threading import Thread
from progress.spinner import Spinner
from urllib.parse import urlparse

from tech.tech import Tech
from dns.dns import Dns
from banner.grabber import Grabber
from search.search import Search
from exploit.exploit import Exploit
from helper.parser import parse_from_hostsearch
from helper.risk import RiskResolver
from helper import packages


version = '0.6.2'
progress_state = 'RUNNING'


class Progress(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global progress_state
        time.sleep(1)
        spinner = Spinner('Loading ')
        while progress_state != 'FINISHED':
            time.sleep(0.1)
            spinner.next()


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
        self.info = {'host': self.target,
                     'info': {}}
        try:
            self.dns = self.target + ',' + socket.gethostbyname(self.target)
        except Exception as e:
            print('Failed to gethostbyname. Reason: %s' % e)

    """
    Parse hostsearch from dns
    :param data: dns's hostsearch result
    """
    def hostsearch(self, data: str):
        self.dns = data
        self.info['info'] = parse_from_hostsearch(self.dns)

    def calc_risk(self):
        if 'risks' in self.info:
            exploits = 0
            if 'exploits' in self.info['risks']:
                exploits = self.info['risks']['exploits']
            self.info['risk_level'] = RiskResolver.calc_risk(self.info['risks'], exploits)

    def calc_severety(self, vulns):
        for vuln in vulns:
            risk_level = RiskResolver.calc_cve_severity(vuln['cvss'])
            if 'risks' not in self.info:
                self.info['risks'] = {}
            if risk_level not in self.info['risks']:
                self.info['risks'][risk_level] = 1
            else:
                self.info['risks'][risk_level] = self.info['risks'][risk_level] + 1

    def found_exploits(self, count):
        if 'risks' in self.info:
            self.info['risks']['exploits'] = count

    """
    Reformat tech item in json
    """
    def reformat_tech(self):
        info = self.info['info']
        for hostname in info:
            if 'tech' in info[hostname]:
                tech = info[hostname]['tech']
                for tec in tech:
                    tech[tec]['version'] = ''
                    if tech[tec]['versions']:
                        tech[tec]['version'] = tech[tec]['versions'][0]
                    del tech[tec]['versions']


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="osint.py")
    parser.add_argument('url', nargs='?', help='URL to analyze')

    # commands args
    parser.add_argument('-a', '--all', action='store_true', help='Full osint for url')
    parser.add_argument('--dns', action='store_true', help='DNS scan only')
    parser.add_argument('--tech', action='store_true', help='Tech scan only')
    parser.add_argument('--banner', action='store_true', help='Banner grabbing only')
    parser.add_argument('--search', action='store_true', help='CVE Search only')
    parser.add_argument('--exploit', action='store_true', help='Search Exploits only')

    # searchsploit args
    parser.add_argument('--cve', type=str, help='CVE')

    # output args
    parser.add_argument('--docx', action='store_true', help='Generate docx for output')
    parser.add_argument('-t', '--template', type=str, default='test', help='Template for docx. Get template name or full path')

    # helper args
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    parser.add_argument('--update', action='store_true',
                        help='Use the latest technologies and categories downloaded from the internet. '
                             'Also updates cve and exploits dbs.')
    parser.add_argument('--init', action='store_true',
                        help='Initial setup for clean installation of cve_search, searchsploit and more')
    parser.add_argument('--setup', action='store_true',
                        help='Automate setup all necessary system packages, like mongodb or redis')
    parser.add_argument('--force', action='store_true', help='Force init. Removes all git data and download it again.')

    return parser


def main(parser) -> None:
    global progress_state
    print('---------------')
    print(" osint.py v%s" % version)
    print('---------------')

    args = parser.parse_args()

    if not args.all and not args.dns and not args.tech and not args.banner and not args.search and not args.exploit \
            and not args.init and not args.update and not args.setup:
        print('No mode selected')
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.setup:
        print('Setup')
        packages.setup()
        print('---------------')

    if args.init:
        print('Initializing')
        packages.init(args.force)
        print('\n---------------')

    if args.update:
        print('Updating')
        packages.update()
        print('---------------')

    if not args.url:
        if args.update or args.init or args.setup:
            sys.exit(1)
        print('No URL selected')
        parser.print_help(sys.stderr)
        sys.exit(1)

    host = Host(args.url)

    if args.all or args.dns:
        print('Getting dns for %s' % host.target)
        results = Dns().analyze(host.target)
        if not results:
            print("Error in parsing dns records")
            host.hostsearch(host.dns)
        else:
            host.hostsearch(results)
        print('---------------')
    else:
        host.hostsearch(host.dns)

    if args.all or args.tech:
        for hostname in host.info['info']:
            print('Getting tech for %s' % hostname)
            results = Tech().analyze(hostname)
            host.info['info'][hostname]['tech'] = results
            print('---------------')
        host.reformat_tech()

    if args.banner:
        for hostname in host.info['info']:
            print('Getting banner for %s' % hostname)

            progress_state = 'RUNNING'
            thread = Progress()
            thread.start()

            results = Grabber().grab(hostname)

            progress_state = 'FINISHED'
            thread.join()

            host.info['info'][hostname]['banner'] = results
            print('\n---------------')

    if args.all or args.search:
        if args.all or args.tech:
            search = Search()
            search_optimizer = {}
            for hostname in host.info['info']:
                tech = host.info['info'][hostname]['tech']
                for tec in tech:
                    tech_ver = tech[tec]['version']
                    if tech_ver != '':
                        search_optimizer_tech_version = '%s v%s' % (tec, tech_ver)
                        if search_optimizer_tech_version not in search_optimizer:
                            search_optimizer[search_optimizer_tech_version] = {}
                            print('Running cve-search for %s:%s' % (tec, tech_ver))
                            search_result = search.search(tec, tech_ver)
                            if search_result:
                                search_optimizer[search_optimizer_tech_version]['search'] = search_result
                                tech[tec]['vulns'] = search_result
                                host.calc_severety(tech[tec]['vulns'])
                        elif 'search' in search_optimizer[search_optimizer_tech_version]:
                            print('Results of cve-search for %s:%s found' % (tec, tech_ver))
                            tech[tec]['vulns'] = search_optimizer[search_optimizer_tech_version]['search']
                            host.calc_severety(tech[tec]['vulns'])
        else:
            print('Search mode works only with Tech mode together')
        print('---------------')

    if args.all or args.exploit:
        print('Searching exploits')
        sploit = Exploit()
        exploit_optimizer = {}
        exploit_count = 0
        if args.all or args.search:
            for hostname in host.info['info']:
                tech = host.info['info'][hostname]['tech']
                for tec in tech:
                    if 'vulns' in tech[tec]:
                        for vuln in tech[tec]['vulns']:
                            if re.match(r'CVE-\d{4}-\d{4,7}', vuln['id']):
                                if vuln['id'] not in exploit_optimizer:
                                    exploit_optimizer[vuln['id']] = {}
                                    sploit_result = sploit.search(vuln['id'])
                                    if sploit_result:
                                        exploit_optimizer[vuln['id']]['search'] = sploit_result
                                        vuln['exploits'] = sploit_result
                                        exploit_count = exploit_count + len(vuln['exploits'])
                                elif 'search' in exploit_optimizer[vuln['id']]:
                                    print('Results of searching exploits for %s found' % vuln['id'])
                                    vuln['exploits'] = exploit_optimizer[vuln['id']]['search']
                                    exploit_count = exploit_count + len(vuln['exploits'])
            host.found_exploits(exploit_count)
        if args.cve is not None:
            if re.match(r'CVE-\d{4}-\d{4,7}', args.cve):
                print(sploit.search(args.cve))
            else:
                print('Wrong CVE format')
        print('---------------')

    if args.all or args.search:
        host.calc_risk()

    print('\nResults:')
    print(json.dumps(host.info))


if __name__ == '__main__':
    main(get_parser())
