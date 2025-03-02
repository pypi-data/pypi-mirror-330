import socket
import threading
import queue
import time


import numpy as np

class MessageQueue:
    def __init__(self, maxsize=100):
        """
        初始化消息队列
        
        :param maxsize: 队列的最大容量，默认为 10，设置为 0 表示队列大小无限制
        """
        self.queue = queue.Queue(maxsize=maxsize)

    def put(self, message):
        """将消息放入队列"""
        try:
            self.queue.put(message)  # 默认最多等待 5 秒
            print(f"Message added: {message}")
        except queue.Full:
            print("Queue is full, could not add message.")

    def get(self):
        """从队列中取出消息"""
        try:
            message = self.queue.get()  # 默认最多等待 5 秒
            print(f"取出消息: {message}")
            self.queue.task_done()
            return message
        except queue.Empty:
            print("Queue is empty, no message to retrieve.")
            return None

    def size(self):
        """返回队列中当前的消息数量"""
        return self.queue.qsize()

    def is_empty(self):
        """判断队列是否为空"""
        return self.queue.empty()

    def is_full(self):
        """判断队列是否已满"""
        return self.queue.full()

    def join(self):
        """阻塞直到队列中的所有任务都完成"""
        self.queue.join()
        print("All tasks are done.")


class TCPServer:
    def __init__(self, host='127.0.0.1', port=65432, maxsize=10):
        """
        初始化 TCPServer 实例
        
        :param host: 监听的 IP 地址，默认为 '127.0.0.1'
        :param port: 监听的端口，默认为 65432
        :param maxsize: 使用的消息队列最大容量
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.queue =  MessageQueue(maxsize)
        self.clients_list = []          # 存储客户端连接的 socket 对象

    def start_listening(self):
        """启动监听并等待客户端连接"""
        # 创建 TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 绑定到指定地址和端口
        self.server_socket.bind((self.host, self.port))
        
        # 开始监听客户端连接，最大连接数为 5
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}...")
        
        # 接受客户端连接
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected by {client_address}")
            # 启动新的线程来处理客户端请求
            threading.Thread(target=self.handle_client, args=(client_socket,client_address)).start()

    def handle_client(self, client_socket,client_address):
        """处理与客户端的通信"""
        
        try:
            print(f"New connection from {client_address}")
            # 接收客户端消息
            message = client_socket.recv(1024).decode()
            message = eval(message)
            self.queue.put(message)
            self.clients_list.append((client_socket, client_address,message['headers']['conversation_id']))
            print(f"Received message from {client_address}: {message}")           
        except Exception as e:
            print(f"Error with client {client_address}: {e}")

        
                
                
    def response(self,message):
        for index in range(len(self.clients_list)):
            if self.clients_list[index][2]==message['headers']['conversation_id']:
                client,client_address,_ = self.clients_list.pop(index)
                client.send(str(message).encode())
                print(f"Sent response to {client_address}: {message}")
                client.close()
                print(f"Connection with {client_address} closed.")
                
    def getAMessage(self):
        return self.queue.get()
    
    def is_empty(self):
        return self.queue.is_empty()
    
    def have_message(self):
        return self.queue.size()!=0
    
    def stop(self):
        """停止服务器"""
        if self.server_socket:
            self.server_socket.close()
            print("Server has been stopped.")


# 示例：启动一个 TCP 服务器并将收到的消息放入队列
if __name__ == '__main__':
    # 创建一个最大容量为 10 的消息队列
    message_queue = MessageQueue(maxsize=10)
    
    # 创建并启动 TCPServer 实例
    server = TCPServer()
    threading.Thread(target=server.start_listening).start()

    # 消费队列中的消息
    def consume_queue():
        while True:
            message = message_queue.get()
            if message:
                print(f"Consuming message: {message}")
            time.sleep(2)  # 模拟处理时间

    threading.Thread(target=consume_queue).start()
