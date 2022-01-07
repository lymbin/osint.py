# This file is part of osint.py program
# @lymbin 2021-2022


def parse_from_hostsearch(data: str):
    """
    Constructs a new WebPage object for the response,
    using the `BeautifulSoup` module to parse the HTML.

    :param data: dns's hostsearch result
        google.com,8.8.8.8
        
    return
        {
            "google.com": {
                "8.8.8.8" : {}
            }
        }
    """
    dataset = {}
    hosts = data.split('\n')
    for host in hosts:
        hosts_data = host.split(',')
        if len(hosts_data) > 1 and not dataset.get(hosts_data[1]):
            dataset[hosts_data[0]] = {
                'ip': hosts_data[1]
            }
    return dataset
