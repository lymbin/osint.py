# This file is part of osint.py program
# @lymbin 2021-2023

import requests

hunter_base_endpoint = 'https://api.hunter.io/v2/{}'
email_count = "email-count"


class Hunter:
    def search(self, domain: str):
        return self.email_count(domain)

    def email_count(self, domain: str):
        params = {"domain": domain}
        r = requests.get(hunter_base_endpoint.format(email_count), params=params)
        try:
            data = r.json()['data']
        except KeyError:
            return "An error occurred."

        res = {"total": data['total']}
        return res
