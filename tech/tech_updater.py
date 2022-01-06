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


class TechUpdater:
    """
    Updater is a modified python-Wappalyzer wrapper.
    """

    @staticmethod
    def update_technologies(packages_folder):
        should_update = True
        _files = ''
        _files = TechUpdater.find('technologies.json', packages_folder)
        if _files:
            technologies_file = pathlib.Path(_files.pop())
            last_modification_time = datetime.fromtimestamp(technologies_file.stat().st_mtime)
            if datetime.now() - last_modification_time < timedelta(hours=2):
                should_update = False

        # Get the lastest file
        if should_update:
            temp_dir = os.path.join(packages_folder, 'techDir')
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
                    tech_part_file = os.path.join(temp_dir, '%s.json' % (c))
                    with open(tech_part_file, 'w') as tfile:
                        tfile.write(tech_file.text)
                    files.append(tech_part_file)

                if os.path.exists(os.path.join(packages_folder, 'technologies.json')):
                    os.remove(os.path.join(packages_folder, 'technologies.json'))

                TechUpdater.merge_json_files(files, os.path.join(packages_folder, 'technologies.json'))
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
    def update_categories(packages_folder):
        should_update = True
        _files = ''
        _files = TechUpdater.find('categories.json', packages_folder)
        if _files:
            categories_file = pathlib.Path(_files.pop())
            last_modification_time = datetime.fromtimestamp(categories_file.stat().st_mtime)
            if datetime.now() - last_modification_time < timedelta(hours=2):
                should_update = False

        if should_update:
            try:
                cat_file = requests.get(
                    'https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/categories.json')
                if os.path.exists(os.path.join(packages_folder, 'categories.json')):
                    os.remove(os.path.join(packages_folder, 'categories.json'))
                with open(os.path.join(packages_folder, 'categories.json'), 'w') as tfile:
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

    @staticmethod
    def update(packages_folder):
        TechUpdater.update_technologies(packages_folder)
        TechUpdater.update_categories(packages_folder)

    @staticmethod
    def init(packages_folder):
        pass
