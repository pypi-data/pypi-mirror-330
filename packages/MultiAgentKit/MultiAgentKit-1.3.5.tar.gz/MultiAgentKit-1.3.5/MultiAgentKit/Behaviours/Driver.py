from MultiAgentKit.Behaviours.Base import CyclicBehaviour
from abc import abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MultiAgentKit.Agent.Agent import Agent
    
class Driver(CyclicBehaviour):
    def __init__(self,agent: 'Agent'):
        super().__init__(agent,1)
        self.agent = agent
        self.condition = False
        self.order = ""
        self.message = ""
        self.selector_type = 'greedy'
        self.providers_list_final = []
        self.response = ""               # 接收到的信息
    
    def action(self):    
        self.bind()                     # 绑定数据
        if (self.condition):
            print("Agent {} 正在执行{}指令驱动底层运动... ...".format(self.agent.agent_name,self.order.strip()))
            self._Sender()
            self.variableReset()              # 重置标志位

                
            
        
        
    @abstractmethod   
    def bind(self):
        '''
            Function
            --------
            你需要在该方法中，你需要绑定condition、order四个变量的值。
        '''
        pass

    def _Sender(self):
        self.agent.device_connetction.send_message(self.order)
        self.agent.device_connetction.receive_message()
        print("Agent {} 的{}指令执行结束!".format(self.agent.agent_name,self.order.strip()))
    
    @abstractmethod    
    def variableReset(self):
        '''
        Function
        --------
        在该方法中，你需要对重置操作进行定义。
        '''
        pass
    
        

