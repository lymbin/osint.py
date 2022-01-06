# This file is part of osint.py program
# @lymbin 2021-2022

from .nmap import Nmap
from .netcat import Netcat

"""
Changelog:

-- 0.2 --
Netcat using by default

-- 0.1 --
Initial release

"""
version = '0.2'
ports = "21,22,80,443"


class Grabber:
    """
    Grabber is a banner grabbing tool for getting banner info from top ports
    Uses Nmap and Netcat modules
    """

    def __init__(self):
        self.engines = {
            'Nmap': Nmap,
            'Netcat': Netcat
        }
        self.target = ""

    def grab(self, target: str, mode="Netcat"):
        """
        Method to grab info from banners.
        As a default uses "Netcat" mode.
        Can use hard "Nmap" mode. It's a nmap's -sV scan.
        
        :param target:  target URL
        :param mode:    Grab mode. Can be "Nmap" or "Netcat"
        :Return: 
            `Dict`. dictionary with banners.
        """
        self.target = target
        print('Using %s' % mode)
        results = {mode: self.engines[mode]().grab(target, ports)}
        return results
