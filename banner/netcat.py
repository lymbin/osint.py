# This file is part of osint.py program
# @lymbin 2021

import socket

class Netcat:
    """ Python 'netcat like' module """
    def __init__(self, ip, port):
        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length = 1024):
        """ Read 1024 bytes off the socket """

        return self.socket.recv(length)
 
    def read_until(self, data):
        """ Read data into the buffer until we have data """

        while not data in self.buff:
            self.buff += self.socket.recv(1024)
 
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]
 
        return rval
 
    def write(self, data):
        self.socket.send(data)
    
    def close(self):
        self.socket.close()
        
    def grab(self, target: str, ports = "21,22") -> str:
        """
        Nmap's method to grab info from banners.
        
        :param target: target URL 
        :param ports: scan ports
        :Return: 
            `str`. row with banners.
        """
        self.target = target
        results = ''
        return (results)
        