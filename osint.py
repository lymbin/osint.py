# This file is part of osint.py program
# @lymbin 2021-2022

import argparse
import json
import socket
import sys
import time

from threading import Thread
from progress.spinner import Spinner

from tech.tech import Tech
from dns.dns import Dns
from banner.grabber import Grabber
from search.search import Search
from exploit.exploit import Exploit
from helper.parser import parse_from_hostsearch
from helper import packages

version = '0.6'
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
        self.target = target
        self.info = {}
        self.dns = target + ',' + socket.gethostbyname(self.target)

    """
    Parse hostsearch from dns
    :param data: dns's hostsearch result
    """

    def hostsearch(self, data: str):
        self.dns = data
        self.info = parse_from_hostsearch(self.dns)

    def gettech(self):
        for ip in self.info:
            for ip_host in self.info[ip]:
                ip_host['search'] = {}
                if 'tech' in ip_host:
                    tech = ip_host['tech']
                    for tec in tech:
                        ip_host['search'][tec] = {}
                        ip_host['search'][tec]['version'] = ''
                        if tech[tec]['versions']:
                            ip_host['search'][tec]['version'] = tech[tec]['versions'][0]
                if 'banner' in ip_host:
                    banner = ip_host['banner']
                    for engine in banner:
                        for port in banner[engine]['ports']:
                            if 'product' in port['service']:
                                ip_host['search'][port['service']['product']] = {}
                                ip_host['search'][port['service']['product']]['version'] = ''
                                if 'version' in port['service']:
                                    ip_host['search'][port['service']['product']]['version'] = port['service'][
                                        'version']


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
    parser.add_argument('-f', '--file', type=str, help='File with CVE list')

    # output args
    parser.add_argument('-o', '--output', type=str, help='File for output')

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
            and not args.debug and not args.init and not args.update and not args.setup:
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
        print('Getting dns for %s' % args.url)
        results = Dns().analyze(args.url)
        if not results:
            print("Error in parsing dns records")
            host.hostsearch(host.dns)
        else:
            host.hostsearch(results)
        print('---------------')
    else:
        host.hostsearch(host.dns)

    if args.all or args.tech:
        for ip in host.info:
            for ip_host in host.info[ip]:
                print('Getting tech for %s' % (ip_host['host']))
                results = Tech().analyze(ip_host['host'])
                ip_host['tech'] = results
                print('---------------')

    if args.banner:
        for ip in host.info:
            for ip_host in host.info[ip]:
                print('Getting banner for %s' % (ip_host['host']))

                progress_state = 'RUNNING'
                thread = Progress()
                thread.start()

                results = Grabber().grab(ip_host['host'])

                progress_state = 'FINISHED'
                thread.join()

                ip_host['banner'] = results
                print('\n---------------')

    if args.all or args.search:
        host.gettech()
        search = Search()
        for ip in host.info:
            for ip_host in host.info[ip]:
                for tech in ip_host['search']:
                    tech_ver = ip_host['search'][tech]['version']
                    if tech_ver != '':
                        print('Running cve-search for %s:%s' % (tech, tech_ver))
                        search_result = search.search(tech, tech_ver)
                        if search_result:
                            ip_host['search'][tech]['vuln'] = search_result
        print('---------------')

    if args.all or args.exploit:
        sploit = Exploit()
        if args.cve != '':
            print(sploit.search(args.cve))
        print('---------------')

    print('\nResults:')
    print(json.dumps(host.info))


if __name__ == '__main__':
    main(get_parser())
