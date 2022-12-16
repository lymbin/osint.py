# This file is part of osint.py program
# @lymbin 2021-2022

from tech.tech import Tech
from exploit.exploit import Exploit
from search.search import Search

from .cve_search_setup import CVESearch

"""
Changelog:

-- 0.2 --
Removed setup

-- 0.1 --
Initial release

"""
version = '0.2'


def clear():
    Tech.clear()
    Exploit.clear()
    Search.clear()


def init(force):
    if force:
        clear()
    CVESearch.setup()
    Tech.init()
    Exploit.init()
    Search.init()


def update():
    Tech.update()
    Exploit.update()
    Search.update()
