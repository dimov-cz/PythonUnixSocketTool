import socket
import select

class UnixSocketClient:
    socket_file = None
    sock = None
    
    def __init__(self, socket_file):
        self.socket_file = socket_file
        self.open()
    
    def isConnected(self):
        return self.sock != None
        
    def open(self) -> bool:
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.connect(self.socket_file)
            self.sock.settimeout(3)
            
            return True
        except:
            self.sock = None
            return False
        
    def close(self):
        try:
            self.sock.close()
            self.sock = None
        except:
            pass
    
    def write(self, message):
        if not self.isConnected():
            return False
        try:
            Domoticz.Debug("Writing: " + message)        
            self.sock.send(message.encode('utf-8'))
            return True
        except:
            Domoticz.Error("Write to socket failed, closing socket")
            self.close()
            return False
    
    def read(self, buffer_size=1024):
        if not self.isConnected():
            return None
        try:
            readable, writable, exceptional = select.select([self.sock], [], [], 0)
            if (self.sock in readable):
                msg = self.sock.recv(buffer_size).decode('utf-8')
                if not msg:
                    raise Exception("Read failed")
                return msg
        except:
            Domoticz.Error("Read from socket failed, closing socket")
            self.close()
            return None
