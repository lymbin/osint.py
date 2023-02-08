# This file is part of osint.py program
# @lymbin 2021-2023

from .hunter import Hunter

"""
-- 0.1 --
Initial release

"""
version = '0.1'


class Email:
    """
    Emai module using for search emails
    Uses hunter.io free search for email count
    """
    def __init__(self):
        self.engines = {
            'All': 'All',
            'Hunter': Hunter
        }
        self.hunter = Hunter()

    """
    Method to search emails.
    
    :param domain: domain name
    :param mode: Engine for search emails.
    :Return: 
    `str`. Row of emails in json
    """
    def search(self, domain: str, mode: str = 'Hunter'):
        print('Using %s email engine for searching %s emails' % (mode, domain))
        result = []

        if mode == 'All':
            print('Not implemented yet')
        elif mode == 'Hunter':
            result = self.hunter.search(domain)

        if not result:
            print('Nothing found')
        else:
            print("Found %d Exploit(s)" % len(result))

        return result
