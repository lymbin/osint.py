# This file is part of osint.py program
# @lymbin 2021-2022

import os
import pathlib
import logging
import requests
import shutil
import json
from string import ascii_lowercase
from datetime import datetime, timedelta

logger = logging.getLogger(name="python-Updater")

class Updater:
    """
    Updater is a modified python-Wappalyzer wrapper.
    """
        
    @staticmethod
    def update():
        Updater.update_technologies()
        Updater.update_categories()
        
    @staticmethod
    def update_technologies():
        should_update = True
        _files = ''
        _files = Updater.find('technologies.json', pathlib.Path(__file__).parent.resolve())
        if _files:
            technologies_file = pathlib.Path(_files.pop())
            last_modification_time = datetime.fromtimestamp(technologies_file.stat().st_mtime)
            if datetime.now() - last_modification_time < timedelta(hours=2):
                should_update = False

        # Get the lastest file
        if should_update:
            temp_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'techDir')
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            files = []
            try:
                tech_file = requests.get(
                'https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/technologies/_.json')
                tech_part_file = os.path.join(temp_dir, '_.json')
                with open(tech_part_file, 'w') as tfile:
                    tfile.write(tech_file.text)
                files.append(tech_part_file)
                
                for c in ascii_lowercase:
                    tech_file = requests.get(
                    'https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/technologies/%s.json' % (c))
                    tech_part_file = os.path.join(temp_dir, '%s.json' %(c))
                    with open(tech_part_file, 'w') as tfile:
                        tfile.write(tech_file.text)
                    files.append(tech_part_file)
                
                if os.path.exists(os.path.join(pathlib.Path(__file__).parent.resolve(), 'technologies.json')):
                    os.remove(os.path.join(pathlib.Path(__file__).parent.resolve(), 'technologies.json')) 
                
                Updater.merge_json_files(files, os.path.join(pathlib.Path(__file__).parent.resolve(), 'technologies.json'))
                logger.info("python-Updater technologies.json file updated")

            except Exception as err:  # Or loads default
                logger.error(
                    "Could not download latest Wappalyzer technologies.json file because of error : '{}'. Using "
                    "default. ".format(
                        err))
            try:
                shutil.rmtree(temp_dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        else:
            logger.info(
                "python-Updater technologies.json file not updated because already update in the last 24h")
                
                
    @staticmethod
    def update_categories():
        should_update = True
        _files = ''
        _files = Updater.find('categories.json', pathlib.Path(__file__).parent.resolve())
        if _files:
            categories_file = pathlib.Path(_files.pop())
            last_modification_time = datetime.fromtimestamp(categories_file.stat().st_mtime)
            if datetime.now() - last_modification_time < timedelta(hours=2):
                should_update = False
        
        if should_update:       
            try:
                cat_file = requests.get(
                'https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/categories.json')
                if os.path.exists(os.path.join(pathlib.Path(__file__).parent.resolve(), 'categories.json')):
                    os.remove(os.path.join(pathlib.Path(__file__).parent.resolve(), 'categories.json')) 
                with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'categories.json'), 'w') as tfile:
                    tfile.write(cat_file.text)
                    
                
            except Exception as err:  # Or loads default
                logger.error(
                    "Could not download latest Wappalyzer technologies.json file because of error : '{}'. Using "
                    "default. ".format(
                        err))
                
    @staticmethod
    def find(name, path):
        result = []
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        return result

    @staticmethod
    def merge_json_files(files, filename):
        result = {}
        for file in files:
            with open(file, 'r') as infile:
                json_file = json.load(infile)
                for key, value in json_file.items():
                    result[key] = value
        
        with open(filename, 'w') as output_file:
            json.dump(result, output_file, indent=4)

