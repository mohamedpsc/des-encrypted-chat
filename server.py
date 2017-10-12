import socket
import threading


class server():
        def __init__(self):
            self.running = True

        # Start running the server
        def run(self):
            # Create server socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind the Socket to a puclic host
            self.socket.bind((socket.gethostname(), 5555))
            # Max Number of connections allowed is 1
            self.socket.listen(1)
            # Accepting connection from client
            self.client_socket, self.client_addr = self.socket.accept()
            # Receiving Messages from client on separate thread
            threading.Thread(target=self.receive).start()
            # Sending Messages as well as connection is still active
            while self.running:
                data = input()
                # Ending Chat
                if data != '':
                    self.client_socket.send(data.encode())
                if data == 'exit':
                    self.kill()

        # Ending Chat
        def kill(self):
            self.running = False
            # Close chat socket
            self.client_socket.close()

        # Receive Messages from client
        def receive(self):
            while self.running:
                data = self.client_socket.recv(1024).decode()
                if data in ['exit', '', None]:
                    # Chat Ended by Client
                    self.kill()
                else:
                    print("client: " + data)


if __name__ == '__main__':
    my_server = server()
    my_server.run()