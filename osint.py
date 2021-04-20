# This file is part of osint.py program
# @lymbin 2021

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
from helper.parser import parse_from_hostsearch

version = '0.3'
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
       
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="osint.py")
    parser.add_argument('url', help='URL to analyze')
    
    #common args
    parser.add_argument('--all', action='store_true', help='Full osint for url')
    parser.add_argument('--dns', action='store_true', help='DNS scan only')
    parser.add_argument('--tech', action='store_true', help='Tech scan only')
    parser.add_argument('--banner', action='store_true', help='Banner grabbing only')
    parser.add_argument('-o', '--output', type=str, help='File for output')
    
    #tech args
    parser.add_argument('--update', action='store_true', help='Use the latest technologies file downloaded from the internet')
    return parser

def main(parser) -> None:
    global progress_state
    print('---------------')
    print(" osint.py v%s" % (version))
    print('---------------')
    
    args = parser.parse_args()
    host = Host(args.url)
    
    if not args.dns and not args.tech and not args.banner:
        print('No mode selected') 
        parser.print_help(sys.stderr)
        sys.exit(1)
    
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
            for ip_host in host.info[ip]:
                print('Getting tech for %s' % (ip_host['host']))
                results = Tech(update=args.update).analyze(ip_host['host'])
                ip_host['tech'] = results
                print('---------------')
                
    if args.all or args.banner:
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
    
    print('\nResults:')
    print(json.dumps(host.info))

if __name__ == '__main__':
    main(get_parser())