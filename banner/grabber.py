# This file is part of osint.py program
# @lymbin 2021

from .nmap import Nmap

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'
ports = "21,22,80,443"

class Grabber:
    """
    Grabber is a banner grabbing tool for getting banner info from top ports
    Uses Nmap and Netcat modules
    """
    def __init__(self):
        self.engines = {
            'Nmap': Nmap
        }
        
    def grab(self, target: str, mode = "Nmap") -> str:
        """
        Method to grab info from banners.
        As a default uses hard "Nmap" mode. It's a nmap's -sV scan.
        
        :param target:  target URL
        :param mode:    Grab mode. Can be "Nmap" or "Netcat"
        :Return: 
            `str`. row with banners.
        """
        self.target = target
        print ('Using %s' % (mode))
        results = {}
        results[mode] = {}
        results[mode] = self.engines[mode]().grab(target, ports)
        return results
        