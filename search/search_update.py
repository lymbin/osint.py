# This file is part of osint.py program
# @lymbin 2021-2022

import os
import configparser

cve_search_name = 'cve-search'
sbin_name = 'sbin'
db_mgmt_cpe_dictionary = 'db_mgmt_cpe_dictionary.py'
db_mgmt_json = 'db_mgmt_json.py'
db_updater = 'db_updater.py'

cve_search_git_path = 'https://github.com/cve-search/cve-search.git'

class SearchUpdater:
    def update(packages_folder):
        if not os.path.exists(os.path.join(packages_folder, cve_search_name)):
            SearchUpdater.init(packages_folder)
        try:
            db_updater_path = os.path.join(packages_folder, cve_search_name, sbin_name, db_updater)
            print('Update cve-search database')
            os.system('%s -v' % db_updater_path)
        except Exception as e:
            print('Failed to update. Reason: %s' % e)

    def init(packages_folder):
        try:
            print ("Init cve-search repo")
            if not os.path.exists(os.path.join(packages_folder, cve_search_name)):
                os.system("cd %s; git clone %s" % (packages_folder, cve_search_git_path))
            
            db_mgmt_cpe_dictionary_path = os.path.join(packages_folder, cve_search_name, sbin_name, db_mgmt_cpe_dictionary)
            db_mgmt_json_path = os.path.join(packages_folder, cve_search_name, sbin_name, db_mgmt_json)
            db_updater_path = os.path.join(packages_folder, cve_search_name, sbin_name, db_updater)
            
            print('Populating cve-search database')
            os.system('%s -p' % db_mgmt_cpe_dictionary_path)
            os.system('%s -p' % db_mgmt_json_path)
            print('Update cve-search database')
            os.system('%s -c' % db_updater_path)
        except Exception as e:
            print('Failed to init. Reason: %s' % e)