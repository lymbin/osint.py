# osint.py

This tool is might helpful for osint searches

## Usage

`osint.py --all google.com`

## dns.py

dns.py gets a dns info from domain using DNS Dumpster and HackerTarget.com IP tools.

This tool constructed over [dnsdmpstr](https://github.com/zeropwn/dnsdmpstr)

## tech.py

tech.py identifies technologies on websites from headers, meta, body, scripts and javascript code.

This is a custom implementation of [python-Wappalyzer](https://github.com/chorsley/python-Wappalyzer)

## grabber.py

grabber.py uses Nmap -sV for banner grabbing of all domains or subdomains.

Banner grabbing performs for 21, 22, 80 and 443 ports for now.

This tool constructed over [python3-nmap](https://github.com/nmmapper/python3-nmap) and [netcat.py](https://gist.github.com/leonjza/f35a7252babdf77c8421)(not implemented yet).
