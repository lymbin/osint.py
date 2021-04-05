"""This File is part osint.py program"""
import argparse
import json
from Wappalyzer import Wappalyzer, WebPage

def get_parser() -> argparse.ArgumentParser:
    """Get the CLI `argparse.ArgumentParser`"""
    parser = argparse.ArgumentParser(description="tech.py")
    parser.add_argument('url', help='URL to analyze')
    parser.add_argument('--update', action='store_true', help='Use the latest technologies file downloaded from the internet')
    return parser

def main(args) -> None:
    wappalyzer = Wappalyzer.latest(update=args.update)
    webpage = WebPage.new_from_url(args.url)
    results = wappalyzer.analyze_with_versions_and_categories(webpage)
    print(json.dumps(results))

if __name__ == '__main__':
    main(get_parser().parse_args())