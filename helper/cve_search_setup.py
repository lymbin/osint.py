# This file is part of osint.py program
# @lymbin 2021-2022

import os
import distro

cve_search_name = 'cve-search'
requirements_system = 'requirements.system'
requirements = 'requirements.txt'

cve_search_git_path = 'https://github.com/cve-search/cve-search.git'

temp_folder = os.path.dirname(os.path.realpath(__file__))


class CVESearch:
    @staticmethod
    def setup():
        try:
            if not os.path.exists(os.path.join(temp_folder, cve_search_name)):
                print("Init temp cve-search repo")
                os.system("cd %s; git clone %s" % (temp_folder, cve_search_git_path))
            if distro.id() == 'kali' or distro.id() == 'ubuntu':
                _setup_cve_search_ubuntu(os.path.join(temp_folder, cve_search_name))
            else:
                print('Auto Setup supports Ubuntu-like systems only for now')
        except Exception as e:
            print('Failed to setup. Reason: %s' % e)


def _setup_cve_search_ubuntu(cve_search_folder):
    os.system('xargs sudo apt-get install -y < %s' % os.path.join(cve_search_folder, requirements_system))
    os.system('sudo pip3 install markupsafe --upgrade')
    os.system('sudo pip3 install -r %s' % os.path.join(cve_search_folder, requirements))
    os.system('wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -')
    os.system('echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list')
    os.system('sudo apt-get update')
    os.system('sudo apt-get install -y mongodb-org')
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl start mongod')
    os.system('sudo systemctl status mongod')
    os.system('sudo systemctl enable mongod')
