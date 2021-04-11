# This file is part of osint.py program
# @lymbin 2021

import argparse
import json
import socket

from tech.tech import Tech
from dns.dns import Dns
from helper.parser import parse_from_hostsearch

version = '0.2'

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
        
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="osint.py")
    parser.add_argument('url', help='URL to analyze')
    
    #common args
    parser.add_argument('--all', action='store_true', help='Full osint for url')
    parser.add_argument('--dns', action='store_true', help='DNS scan only')
    parser.add_argument('--tech', action='store_true', help='Tech scan only')
    parser.add_argument('-o', '--output', type=str, help='File for output')
    
    #tech args
    parser.add_argument('--update', action='store_true', help='Use the latest technologies file downloaded from the internet')
    return parser

def main(args) -> None:
    print('---------------')
    print(" osint.py v%s" % (version))
    print('---------------')
    
    host = Host(args.url)
    
    if args.all or args.dns:
        print('Getting dns for %s' % (args.url))
        results = Dns().analyze(args.url)
        if results == False:
            print("Error in parsing dns records")
            host.hostsearch(host.dns)
        else:
            host.hostsearch(results)
        print('---------------')
    else:
       host.hostsearch(host.dns)
    
    if args.all or args.tech:
        for ip in host.info: 
            for host_info in host.info[ip]:
                print('Getting tech for %s' % (host_info['host']))
                results = Tech(update=args.update).analyze(host_info['host'])
                host_info['tech'] = results
                print('---------------')
    
    print('\nResults:')
    print(host.info)

if __name__ == '__main__':
    main(get_parser().parse_args())