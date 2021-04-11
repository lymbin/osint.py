# This file is part of osint.py program
# @lymbin 2021

import argparse
import json
from tech.tech import Tech
from dns.dns import Dns

version = '0.2'

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
    
    if args.all or args.dns:
        print('Getting dns for %s' % (args.url))
        results = Dns().analyze(args.url)
        print(results)
        
    if args.all or args.tech:
        print('Getting tech for %s' % (args.url))
        results = Tech(update=args.update).analyze(args.url)
        print(results)
        

if __name__ == '__main__':
    main(get_parser().parse_args())