from abc import ABC,abstractmethod
import socket
import time

class Behaviour(ABC):
    def __init__(self,agent):
        self.agent = agent
    @abstractmethod    
    def run(self):
        pass
    @abstractmethod
    def action(self):  
        pass

class CyclicBehaviour(Behaviour):
    def __init__(self,agent,time = 1):
        super().__init__(agent)
        self.time = time
    def run(self):
        while True:
            time.sleep(self.time)
            self.action()

class OneshotBehaviour(Behaviour):
    def run(self):
        self.action()

    
class Behaviours_TCP():
    def __init__(self,agent):
        self.agent = agent
        #self.run()
    def run(self):
        # 创建一个 TCP 套接字
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 获取本地 IP 地址和端口号
        host = '127.0.0.1'
        port = 6000
        
        # 绑定到指定的 IP 地址和端口号
        server_socket.bind((host, port))
        
        # 开始监听客户端连接
        server_socket.listen(5)  # 5 是监听队列的大小
        
        print(f"Server listening on {host}:{port}...")
        
        while True:
            # 接受客户端连接
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            
            # 向客户端发送数据
            client_socket.sendall(b"Hello, you are connected to the server!\n")
            
            # 接收来自客户端的数据
            data = client_socket.recv(1024)  # 接收最多 1024 字节
            print(f"Received from client: {data.decode()}")
            self.agent.data = int(data.decode())
            print("self.agent.data ->{}\n".format(self.agent.data))
            # 关闭与客户端的连接
            client_socket.close()

class Behaviours_Print():
    def __init__(self,agent):
        print('print')
        self.agent = agent
        self.old_data = agent.data
        #self.run()
    def run(self):
        while True:
            if self.agent.data != self.old_data:
                print("self.agent.data have changed! and new data is {}".format(self.agent.data))
                self.old_data = self.agent.data