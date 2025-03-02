import socket

class TCPClient:
    def __init__(self, ip='127.0.0.1', port=65432):
        """
        初始化 TCPClient 实例
        
        :param host: 服务器的 IP 地址，默认为 '127.0.0.1'
        :param port: 服务器的端口，默认为 65432
        """
        self.host = ip
        self.port = port
        self.client_socket = None

    def connect(self):
        """连接到 TCP 服务器"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print(f"Failed to connect to {self.host}:{self.port}")
            return False
        return True

    def send_message(self, message):
        """发送消息到服务器"""
        if self.client_socket:
            try:
                self.client_socket.sendall(str(message).encode())  # 发送数据
                print(f"Sent: {message}")
            except BrokenPipeError:
                print("Connection lost. Unable to send message.")

    def receive_message(self):
        """接收来自服务器的消息"""
        if self.client_socket:
            try:
                data = self.client_socket.recv(1024)  # 接收数据
                if data:
                    print(f"Received from server: {data.decode()}")
                    return data.decode()
                else:
                    print("No response from server.")
            except ConnectionResetError:
                print("Connection was reset by the server.")
        
    
    def close(self):
        """关闭与服务器的连接"""
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")

# 示例：连接到服务器并发送消息
if __name__ == '__main__':
    client = TCPClient('127.0.0.1',10301)

    # 连接到服务器
    if client.connect():
        # 发送消息
        message = "move-1,2,3"
        client.send_message(message)
        
        # 接收服务器的响应
        client.receive_message()
        
        # 关闭连接
        client.close()
