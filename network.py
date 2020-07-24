import socket
import pickle

class Network:
    def __init__(self, HEADER=64, PORT=5000, FORMAT='utf-8', DISCONNECT_MSG='!DISCONNECT', \
                ip_add=None, is_server=False, max_connections=1):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.header = HEADER
        self.server = socket.gethostbyname(socket.gethostname()) if not ip_add else ip_add
        self.port = PORT
        self.addr = (self.server, self.port)
        self.format = FORMAT
        self.disconnect_msg = DISCONNECT_MSG

        self.is_server = is_server
        self.max_connections = max_connections
        self.current_connections = 0

        if self.is_server: 
            self.sock.bind(self.addr)
            self.listen()
        else: 
            self.sock.connect(self.addr)
    
    def send(self, /, conn=None, data=None, broadcast=False, reconnect=False):
        try:
            pickled_data = pickle.dumps(data)
            pickled_data_len = len(pickled_data)

            send_length = str(pickled_data_len).encode(self.format)
            send_length += b' ' * (self.header - len(send_length))

            if self.is_server:
                if broadcast:
                    conn.sendall(send_length)
                    conn.sendall(pickled_data)
                else:
                    conn.send(send_length)
                    conn.send(pickled_data)
            else:
                if reconnect: self.sock.connect(self.addr)
                self.sock.send(send_length)
                self.sock.send(pickled_data)
        except socket.error as e:
            print(e)

    def recv(self, /, conn=None):
        try:
            if self.is_server:
                recv_len_bytes = conn.recv(self.header)
            else:
                recv_len_bytes = self.sock.recv(self.header)
            recv_len = recv_len_bytes.decode(self.format)
            recv_len = int(recv_len)
            if self.is_server:
                return pickle.loads(conn.recv(recv_len))
            else:
                return pickle.loads(self.sock.recv(recv_len))
        except socket.error as e:
            print(e)

    def listen(self):
        if self.is_server:
            try:
                self.sock.listen(self.max_connections)
                print(f'[SERVER] Server is listening on {self.addr}')
            except socket.error as e:
                print(e)
    
    def accept(self):
        if self.is_server:
            try:
                print(f'[SERVER] Waiting for connections ({self.current_connections} / {self.max_connections})')
                s = self.sock.accept()
                self.current_connections += 1
                print(f'[SERVER] Connections ({self.current_connections} / {self.max_connections})')
                return s
            except socket.error as e:
                print(e)