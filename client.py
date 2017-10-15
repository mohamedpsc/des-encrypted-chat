import threading
import socket
import pyDes
import string
import random

class client():
    def __init__(self):
        self.running = True
        self.server_host = '127.0.1.1'
        self.des_key = id_generator()

    # connect client with the server to start chatting
    def run(self):
        # Create Client socket
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the Socket to server host and same port number
        self.my_socket.connect((self.server_host, 5555))
        if self.hand_shake():
            # Initializing DES Encryption
            self.des = pyDes.des(self.des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
            # Receiving Messages from Server on separate thread
            threading.Thread(target=self.receive).start()
            while self.running:
                data = input()
                self.my_socket.send(self.des.encrypt(data))
                if data == 'exit':
                    # Ending Chat
                    self.kill()
        else:
            print("HandShake Failed.")

    # Ending Chat
    def kill(self):
        self.running = False
        # Close chat socket
        self.my_socket.close()

    # Receive Messages from Server
    def receive(self):
        while self.running:
            data = data = self.des.decrypt(self.my_socket.recv(1024))
            if data in ['exit', '', None]:
                # Chat Ended by Server
                self.kill()
            else:
                print("server: " + data)

    def hand_shake(self):
        # TODO GET Public Key of server
        # TODO Encrypt Des key using RCA Public key received from server and send it to the server
        return False

def id_generator(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    my_client = client()
    my_client.run()