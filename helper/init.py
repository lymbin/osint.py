# This file is part of osint.py program
# @lymbin 2021-2022

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from tech.updater import Updater
from .search_init import *
from .common import *

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'

def clear(packages_folder):
    clear_directory(packages_folder)

def setup(packages_folder):
    clear(packages_folder)
    setup_cve_search(packages_folder)
    clear(packages_folder)

def init(packages_folder):
    clear(packages_folder)
    init_cve_search(packages_folder)

def update(packages_folder):
    Updater.update()
    update_cve_search(packages_folder)
    
