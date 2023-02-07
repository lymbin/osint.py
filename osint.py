# This file is part of osint.py program
# @lymbin 2021-2022

import argparse
import json
import sys
import re
import os

from tech.tech import Tech
from dns.dns import Dns
from banner.grabber import Grabber
from search.search import Search
from exploit.exploit import Exploit
from helper.host import Host
from helper.progress import Progress
from helper import packages
from docgen.docgen import Html

version = '0.7.1'


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
    parser.add_argument('--report', action='store_true', help='Generate report for output')
    parser.add_argument('-t', '--template', type=str, default='test',
                        help='Template for report(html). Get template name or full path')
    parser.add_argument('-o', '--output', type=str, default='', help='File to output')

    # helper args
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    parser.add_argument('--update', action='store_true',
                        help='Use the latest technologies and categories downloaded from the internet. '
                             'Also updates cve and exploits dbs.')
    parser.add_argument('--init', action='store_true',
                        help='Initial setup for clean installation of cve_search, searchsploit and more')
    parser.add_argument('--force', action='store_true', help='Force init. Removes all git data and download it again.')

    return parser


def main(parser) -> None:
    print('------------------------------')
    print(" osint.py v%s by @lymbin" % version)
    print('------------------------------')

    args = parser.parse_args()

    if not args.all and not args.dns and not args.tech and not args.banner and not args.search and not args.exploit \
            and not args.init and not args.update:
        print('No mode selected')
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.init:
        print('Initializing')
        packages.init(args.force)
        print('\n------------------------------')

    if args.update:
        print('Updating')
        packages.update()
        print('------------------------------')

    if not args.url:
        if args.update or args.init:
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
        print("Done")
        print('------------------------------')
    else:
        host.hostsearch(host.dns)

    if args.all or args.tech:
        for hostname in host.info:
            print('Getting tech for %s' % hostname)
            results = Tech().analyze(hostname)
            host.info[hostname]['tech'] = results
            print("Done")
            print('------------------------------')
        host.reformat_tech()

    if args.banner:
        for hostname in host.info:
            print('Getting banner for %s' % hostname)

            thread = Progress()
            thread.state('RUNNING')
            thread.start()

            results = Grabber().grab(hostname)

            thread.state('FINISHED')
            thread.join()

            host.info[hostname]['banner'] = results
            print("Done")
            print('\n------------------------------')

    if args.all or args.search:
        if args.all or args.tech:
            search = Search()
            search_optimizer = {}
            for hostname in host.info:
                tech = host.info[hostname]['tech']
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
                            print('---------------')
                        elif 'search' in search_optimizer[search_optimizer_tech_version]:
                            print('Results of cve-search for %s:%s found' % (tec, tech_ver))
                            tech[tec]['vulns'] = search_optimizer[search_optimizer_tech_version]['search']
                            print('---------------')
        else:
            print('Search mode works only with Tech mode together')
        print("Done")
        print('------------------------------')

    if args.all or args.exploit:
        print('Searching exploits')
        sploit = Exploit()
        exploit_optimizer = {}
        if args.all or args.search:
            for hostname in host.info:
                tech = host.info[hostname]['tech']
                for tec in tech:
                    for vuln in tech[tec]['vulns']:
                        vuln['exploits'] = {}
                        if re.match(r'CVE-\d{4}-\d{4,7}', vuln['id']):
                            if vuln['id'] not in exploit_optimizer:
                                exploit_optimizer[vuln['id']] = {}
                                sploit_result = sploit.search(vuln['id'])
                                if sploit_result:
                                    exploit_optimizer[vuln['id']]['search'] = sploit_result
                                    vuln['exploits'] = sploit_result
                            elif 'search' in exploit_optimizer[vuln['id']]:
                                print('Results of searching exploits for %s found' % vuln['id'])
                                vuln['exploits'] = exploit_optimizer[vuln['id']]['search']
        if args.cve is not None:
            if re.match(r'CVE-\d{4}-\d{4,7}', args.cve):
                print(sploit.search(args.cve))
            else:
                print('Wrong CVE format')
        print("Done")
        print('------------------------------')

    host.generate_results()
    print('\nResults:')
    print(json.dumps(host.json))

    if args.report:
        doc_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), host.target)
        if not os.path.exists(doc_path):
            os.mkdir(doc_path)
        html = Html(version, doc_path, args.template)
        html.check_path(host.target)
        html.generate(args.template, host.json)


if __name__ == '__main__':
    main(get_parser())
