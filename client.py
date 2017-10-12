import threading
import socket

class client():
    def __init__(self):
        self.running = True
        self.server_host = '127.0.1.1'

    # connect client with the server to start chatting
    def run(self):
        # Create Client socket
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the Socket to server host and same port number
        self.my_socket.connect((self.server_host, 5555))
        # Receiving Messages from Server on separate thread
        threading.Thread(target=self.receive).start()
        while self.running:
            data = input()
            self.my_socket.send(data.encode())
            if data == 'exit':
                # Ending Chat
                self.kill()

    # Ending Chat
    def kill(self):
        self.running = False
        # Close chat socket
        self.my_socket.close()

    # Receive Messages from Server
    def receive(self):
        while self.running:
            data = self.my_socket.recv(1024).decode()
            if data in ['exit', '', None]:
                # Chat Ended by Server
                self.kill()
            else:
                print("server: " + data)

if __name__ == '__main__':
    my_client = client()
    my_client.run()