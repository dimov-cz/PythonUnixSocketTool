import socket
import os
import select
import logging

class UnixSocketServer:
    socket_file = None
    sock = None
    clients = []
    
    def __init__(self, socket_file):
        self.socket_file = socket_file

        
    def open(self) -> bool:
        # remove the socket file if it already exists
        if os.path.exists(self.socket_file):
            os.remove(self.socket_file)
        # create a Unix domain socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # bind the socket to the file path
        self.sock.bind(self.socket_file)
        # listen for incoming connections
        self.sock.listen(5)
        self.sock.setblocking(False)
        return True
        
    def close(self):
        try:
            self.sock.close()
            self.sock = None
        except:
            pass
    def serviceLoop(self):
        try:
            client, addr = self.sock.accept()
            logging.info(f"Connection from #{client.fileno()}")
            self.clients.append(client)
            self.invite(client)
        except socket.error as e:
            pass
    
    def write(self, client, message):
        client.send(message.encode('utf-8'))
        
    def writeAll(self, message):
        for client in self.clients:
            self.write(client, message)
    
    def read(self, buffer_size=1024):
        read_list = self.clients
        readable, _, _ = select.select(self.clients, [], [], 0)
        
        for client in readable:
            try:
                msg = client.recv(buffer_size).decode('utf-8')
                if not msg:
                    raise Exception("Read failed")
                logging.debug(f"Received from #{client.fileno()}: {msg}")
                return client, msg
            except Exception as e:
                logging.info(f"Closing #{client.fileno()}")
                self.clients.remove(client)
        return None, None
    
    def invite(self, client):
        logging.info(f"Connected #{client.fileno()}...")
        #self.write(client, "Hello, world!\n")
        pass