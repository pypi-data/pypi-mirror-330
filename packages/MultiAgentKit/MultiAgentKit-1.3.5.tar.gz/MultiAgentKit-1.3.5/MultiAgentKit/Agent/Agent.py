import threading
import yaml
from MultiAgentKit.utilities.TCPClient import TCPClient
from MultiAgentKit.utilities.tool import print_error
from MultiAgentKit.utilities.Common_Protocol import Protocol_Common
import time 
class Agent:
    def __init__(self,ymal_file,df_agent,act_listener_port):
        self.df_agent = df_agent
        self.act_listener_port = act_listener_port
        with open(ymal_file, 'r',encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.__dict__.update(self.config)
        if hasattr(self, 'device'):
            while not self.connectDevice(): time.sleep(1)
        self.protocol_common = Protocol_Common()
        print('Agent {}初始化完成!'.format(self.agent_name))
        
    
    def connectDevice(self)->bool:
        """连接设备"""
        self.device_connetction =  TCPClient(self.device['ip'],self.device['port'])
        if self.device_connetction.connect():
            print("Agent {}连接设备成功!".format(self.agent_name))
            return True
        else:
            print_error("Agent {}连接设备失败!等待重新连接...".format(self.agent_name))
            return False

    def startBehaviours(self, target_method):
        """封装线程启动和等待的方法"""
        thread = threading.Thread(target=target_method.run)
        thread.start()
        #thread.join()
    
    def __exit__(self):
        self.device_connetction.close()


if __name__ == '__main__':
    agent = Agent()