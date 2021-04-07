"""This File is part osint.py program"""
import argparse
import json
from tech.tech import Tech

def get_parser() -> argparse.ArgumentParser:
    """Get the CLI `argparse.ArgumentParser`"""
    parser = argparse.ArgumentParser(description="osint.py")
    parser.add_argument('url', help='URL to analyze')
    parser.add_argument('--update', action='store_true', help='Use the latest technologies file downloaded from the internet')
    return parser

def main(args) -> None:
    results = Tech(update=args.update).analyze(args.url)
    print(results)

if __name__ == '__main__':
    main(get_parser().parse_args())