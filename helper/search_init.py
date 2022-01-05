# This file is part of osint.py program
# @lymbin 2021-2022

import os
import git
import distro

cve_search_name = 'cve-search'
sbin_name = 'sbin'

db_mgmt_cpe_dictionary = 'db_mgmt_cpe_dictionary.py'
db_mgmt_json = 'db_mgmt_json.py'
db_updater = 'db_updater.py'

requirements_system = 'requirements.system'
requirements = 'requirements.txt'

cve_search_git_path = 'https://github.com/cve-search/cve-search.git'


def setup_cve_search(thirdparty_folder):
    try:
        git.Git(thirdparty_folder).clone(cve_search_git_path)
        if distro.id() == 'kali' or distro.id() == 'ubuntu':
            setup_cve_search_ubuntu(thirdparty_folder)
        else:
            print('Auto Setup supports Ubuntu-like systems only for now')
    except Exception as e:
        print('Failed to setup. Reason: %s' % e)


def setup_cve_search_ubuntu(thirdparty_folder):
    os.system('xargs sudo apt-get install -y < %s' % os.path.join(thirdparty_folder, cve_search_name, requirements_system))
    os.system('sudo pip3 install -r %s' % os.path.join(thirdparty_folder, cve_search_name, requirements))
    os.system('wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -')
    os.system('echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list')
    os.system('sudo apt-get update')
    os.system('sudo apt-get install -y mongodb-org')
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl start mongod')
    os.system('sudo systemctl status mongod')
    os.system('sudo systemctl enable mongod')


def init_cve_search(folder):
    try:
        git.Git(folder).clone(cve_search_git_path)
        
        db_mgmt_cpe_dictionary_path = os.path.join(folder, cve_search_name, sbin_name, db_mgmt_cpe_dictionary)
        db_mgmt_json_path = os.path.join(folder, cve_search_name, sbin_name, db_mgmt_json)
        db_updater_path = os.path.join(folder, cve_search_name, sbin_name, db_updater)
        
        print('Populating cve-search database')
        os.system('%s -p' % db_mgmt_cpe_dictionary_path)
        os.system('%s -p' % db_mgmt_json_path)
        print('Update cve-search database')
        os.system('%s -c' % db_updater_path)
    except Exception as e:
        print('Failed to init. Reason: %s' % e)
