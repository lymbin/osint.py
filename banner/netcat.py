# This file is part of osint.py program
# @lymbin 2021-2022

import socket


class Netcat:
    """ Python 'netcat like' module """

    def __init__(self):
        self.buff = ""
        self.target = ""
        self.ip = ""

    def connect(self, port):
        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, port))
        self.socket.settimeout(2)
        
    def read(self, port, length=1024):
        """ Read 1024 bytes off the socket """
        return self.socket.recv(length)

    def read_until(self, data):
        """ Read data into the buffer until we have data """
        while data not in self.buff:
            self.buff += self.socket.recv(1024)

        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]

        return rval

    def write(self, data):
        self.socket.send(data)

    def close(self):
        self.socket.close()

    def grab(self, target: str, ports="21,22") -> str:
        """
        Netcat's method to grab info from banners.
        
        :param target: target URL 
        :param ports: scan ports
        :Return: 
            `str`. row with banners.
        """
        results = ''
        self.ip = socket.gethostbyname(target)
        print('Scanning \'nc %s %s\'' % (self.ip, ports))
        ports_array = ports.split(',')
        
        for port in ports_array:
            try:
                self.connect(int(port))
                results = results + self.read(port)
                self.close()
            except Exception as e:
                print('%s on %s:%s' % (e, target, port))
            
        self.target = target
        return results
