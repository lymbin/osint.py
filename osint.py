"""This File is part osint.py program"""
import argparse
import json
from tech.tech import Tech

version = '0.1'

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="osint.py")
    parser.add_argument('url', help='URL to analyze')
    
    #tech args
    parser.add_argument('--update', action='store_true', help='Use the latest technologies file downloaded from the internet')
    return parser

def main(args) -> None:
    print('---------------')
    print(" osint.py v%s" % (version))
    print('---------------')
    print('Getting tech for %s' % (args.url))
    results = Tech(update=args.update).analyze(args.url)
    print(results)

if __name__ == '__main__':
    main(get_parser().parse_args())