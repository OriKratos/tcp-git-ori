import socket

class TCPClient:
    def __init__(self, host: str, port: int):
        self.host=host
        self.port=port

        self.client_socket=None
        def connect(self):

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client_socket.connect((self.host, self.port))

    def send_data(self, data: bytes) -> int:
        self.client_socket.sendall(data)
        return len(data)

    def receive_data(self, buffer_size: int) -> bytes:
        received = self.client_socket.recv(buffer_size)
        
        # נחזיר את הנתונים שהתקבלו כ-bytes.
        return received

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None