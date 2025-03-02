from abc import abstractmethod
from MultiAgentKit.Behaviours.Base import CyclicBehaviour
from MultiAgentKit.utilities.TCPClient import TCPClient

class Communication(CyclicBehaviour):
    def __init__(self,agent):
        super().__init__(agent,1)
        self.condition = False
        self.service_name = ""
        self.message = ""
        self.selector_type = 'greedy'
        self.providers_list_final = []
        self.response = ""               # 接收到的信息
    
    def action(self):    
        self.bind()                     # 绑定数据
        if (self.condition):
            print("监测到标志位触发！查找DF服务:{}".format(self.service_name))
            self.searchDFServiceProviders()   # 搜索所有DF提供者
            if self.providers_list_final:
                self.selector()                   # 选择某一DF提供者
                self.someOperations()            # 对结果进行一些操作
                self.variableReset()              # 重置标志位
            else:
                print("没有找到{} DF服务提供商！".format(self.service_name))
            
        
    @abstractmethod      
    def bind(self):
        '''
            Function
            --------
            你需要在该方法中，你需要绑定condition、service_name、message以及selector_type四个变量的值。
        '''
        pass
    
    @abstractmethod
    def someOperations(self):
        '''
        Function
        --------
        在这个方法，你需要构建接收者provider、发送的信息message、以及返回值response进行处理。通过函数Call_special(provider,message,mess_type)。这个过程将发生在标志位重置之前。
        '''
        pass
    
    @abstractmethod    
    def variableReset(self):
        '''
        Function
        --------
        在该方法中，你需要对重置操作进行定义。
        '''
        pass
    def searchDFServiceProviders(self):
        '''
        Function
        --------
        在该方法中，你需要搜索对应的DF提供者列表。
        '''
        self.providers_list_final = self.agent.df_agent.SearchDFAgent(self.service_name)
        
    def selector(self):
        '''
        Function
        --------
        在该方法中，你需要选择某一个DF提供者。
        '''
        if (self.selector_type == 'greedy'):
            self.provider = self.providers_list_final[0]

    def callSpecial(self,provider,message):
        '''
        Function
        --------
        在该方法中，你需要调用provider提供的服务。
        '''
        print("Agent {} 发送消息给地址{}".format(self.agent.agent_name,provider))
        ip,port = provider.split(':') 
        tcpclient = TCPClient(ip,int(port))
        tcpclient.connect()
        tcpclient.send_message(message)
        self.response = tcpclient.receive_message()
        print('Agent {} 接收到地址{}的消息:{}'.format(self.agent.agent_name,provider,self.response))
        tcpclient.close()
        
