# This file is part of osint.py program
# @lymbin 2021

import nmap3

version_arg = "-sV"

class Nmap:
    """
    Nmap banner grabbing module
    """
    def filter(self, xmlroot):
        """
        Custom filter of nmap3's filter_top_ports. Removed a lot of useless (for us) stuff
        Given the xmlroot return the all the ports that are open from that tree
        """ 
        try:
            port_result_dict = {}
            
            scanned_host = xmlroot.find("host")
            # stats = xmlroot.attrib
            
            if scanned_host:
            # for host in scanned_host:
                address = scanned_host.find("address").get("addr")
                # port_result_dict[address]={} # A little trick to avoid errors
                
                port_result_dict["osmatch"] = self.nmap.parser.parse_os(scanned_host)
                port_result_dict["ports"] = self.nmap.parser.parse_ports(scanned_host)
                # port_result_dict["hostname"] = self.nmap.parser.parse_hostnames(scanned_host)
                # port_result_dict["macaddress"] = self.nmap.parser.parse_mac_address(scanned_host)
                # port_result_dict["state"] = self.nmap.parser.get_hostname_state(scanned_host)
                # Removed useless stats and runtime
                # port_result_dict["stats"]=stats
                # port_result_dict["runtime"]=self.parse_runtime(xmlroot)
            
        except Exception as e:
            raise(e)
        else:
            return port_result_dict
            
    def grab(self, target: str, ports = "21,22") -> str:
        """
        Nmap's method to grab info from banners.
        
        :param target: target URL 
        :param ports: scan ports
        :Return: 
            `str`. row with banners.
        """
        self.target = target
        self.nmap = nmap3.Nmap()
        
        port_scan = "-p {ports} --open".format(ports=ports)
        print ('Scanning \'nmap %s %s %s\'' % (target, version_arg, port_scan))
        
        xml_root = self.nmap.scan_command(target=target, arg=version_arg, args=port_scan)
        results = self.filter(xml_root)
        
        return (results)
        