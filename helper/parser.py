# This file is part of osint.py program
# @lymbin 2021-2022

"""
Changelog:

-- 0.1 --
Initial release

"""
version = '0.1'


def parse_from_hostsearch(data: str):
    """
    Constructs a new WebPage object for the response,
    using the `BeautifulSoup` module to parse the HTML.

    :param data: dns's hostsearch result
        google.com,8.8.8.8
        
    return
        {
            "8.8.8.8": {
                "google.com" : {}
            }
        }
    """
    dataset = {}
    hosts = data.split('\n')
    for host in hosts:
        hosts_data = host.split(',')
        if len(hosts_data) > 1 and not dataset.get(hosts_data[1]):
            dataset[hosts_data[1]] = []
            dataset[hosts_data[1]].append({
                'host': hosts_data[0]
            })
    return dataset
