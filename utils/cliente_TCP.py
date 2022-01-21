from typing import Union

import socket

class Socket_NodeRed:

    MAX_MESSAGE_LENGTH = 1024   

    def __init__(self, sock : socket = None, name : str = '', timeout : int = 1 ) -> int:
        self.timeout   = timeout
        self.connected = False 
        self.name      = name 
        if sock is None:
            try:
                socket.setdefaulttimeout(timeout)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as e:
                print( e )
                self.sock = -1 
        else:
            self.sock = sock
    
    def is_alive(self) -> bool:
        return self.connected 

    def connect(self, host : str, port : int ) -> int:
        try:    
            self.sock.connect((host, port))
            self.connected = True 
        except socket.error as e : 
            print( "Socket {} connection timeout. Verify connection".format(self.__str__()) )
            self.connected = False 
            
    def send(self, msg : Union[str, bytes]):
        if type(msg) == str: msg = msg.encode() 
        if self.connected: 
            totalsent = 0
            while totalsent < len(msg):
                sent = self.sock.send( msg[totalsent:] )
                if sent == 0:
                    print( "socket connection broken" )
                    self.connected = False
                totalsent = totalsent + sent
        else: 
            print('Socket disconnected') 

    def receive(self):
        if self.connected:
            try:    
                rec = self.sock.recv( self.MAX_MESSAGE_LENGTH ) 
            except socket.error as e : 
                print('Error ', e )
                rec = -1 
            return rec.decode()
        else: 
            print('Socket disconnected' ) 

    def __str__(self) -> str:
        print( self.name )
    
    def close(self): 
        self.sock.close() 