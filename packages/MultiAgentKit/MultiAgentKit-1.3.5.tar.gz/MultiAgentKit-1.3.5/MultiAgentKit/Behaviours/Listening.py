
from abc import abstractmethod
from MultiAgentKit.Behaviours.Base import CyclicBehaviour
from MultiAgentKit.utilities.TCPServer import TCPServer
import time
import threading

class Listening(CyclicBehaviour):
    def __init__(self,agent):
        super().__init__(agent,1)
        self.tcpserver = TCPServer('127.0.0.1',agent.act_listener_port)
        self.message = ''
        threading.Thread(target=self.tcpserver.start_listening).start()
        print("Agent {} 开启行为监听，port:{}".format(agent.agent_name,agent.act_listener_port))
    
    def run(self):
        while True:
            time.sleep(self.time)
            if self._haveMessage():
                self.message = self._getMessage()
                self.action()
    @abstractmethod
    def action(self):
        '''
        Function
        --------
        针对收到的消息self.message进行处理。
        '''
        pass
    def _getMessage(self):
        return self.tcpserver.queue.get()
    
    def _haveMessage(self):
        return self.tcpserver.have_message()
        
    def actionUnitWait(self,agent,key):        
        while (getattr(agent,key) == True):
            time.sleep(1)