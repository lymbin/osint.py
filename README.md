# osint.py

This tool is might helpful for osint searches

## Installation

`pip3 install -r requirements.txt`

`osint.py --init`

## Usage

`osint.py --all google.com`

## dns.py

dns.py gets a dns info from domain using DNS Dumpster and HackerTarget.com IP tools.

This tool constructed over [dnsdmpstr](https://github.com/zeropwn/dnsdmpstr)

## tech.py

tech.py identifies technologies on websites from headers, meta, body, scripts and javascript code.

This is a custom implementation of [python-Wappalyzer](https://github.com/chorsley/python-Wappalyzer) with new json updater and modern fixes.

Using technologies from [wappalyzer](https://github.com/AliasIO/wappalyzer)

## grabber.py

grabber.py uses Nmap -sV and Netcat for banner grabbing of all domains or subdomains.

grabber.py removed from --all

Banner grabbing performs for 21, 22, 80 and 443 ports for now.

This tool constructed over [python3-nmap](https://github.com/nmmapper/python3-nmap) and [netcat.py](https://gist.github.com/leonjza/f35a7252babdf77c8421).

## search.py

search.py uses Cve-Search tool for searching CVE for techs and banners.

[cve-search](https://github.com/cve-search/cve-search) need to be installed for use this feature. Also edit /search/config.ini and put path to your cve-search installtrion directory.

## exploit.py

exploit.py uses exploitdb and PoC-in-GitHub repos for searching exploits for CVEs.

ExploitDB engine uses modified [cve_searchsploit](https://github.com/andreafioraldi/cve_searchsploit) tool and [exploitdb](https://github.com/offensive-security/exploitdb) repo.

GithubExploits engine uses [PoC-in-GitHub](https://github.com/nomi-sec/PoC-in-GitHub) repo.

## docgen.py

docgen.py uses jinja2 to generating html with results
