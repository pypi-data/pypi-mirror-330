from MultiAgentKit.utilities.tool import print_error

class DFAgent:
    def __init__(self,system_host):
        self.host = system_host
        
        self.server_list = {
            #'outbound': ['127.0.0.1:11402'],
            #'transport': ['127.0.0.1:11301']
        }
    def registerForDfService(self,dfserver_name_list,dfserver_port):
        for i in range(len(dfserver_name_list)):
            if dfserver_name_list[i] in self.server_list.keys():
                self.server_list[dfserver_name_list[i]].append(self.host+":"+str(dfserver_port))
            else:
                self.server_list[dfserver_name_list[i]] = [self.host+":"+str(dfserver_port)]
    def logOutOfDfService(self,dfserver_name,ip_port):
        if ip_port in self.server_list[dfserver_name]:
            self.server_list[dfserver_name].remove(ip_port)
        else:
            print_error("服务对象未注册，注销失败！")
    def SearchDFAgent(self,dfserver_name):
        if dfserver_name in self.server_list.keys():
            return self.server_list[dfserver_name]
        else:
            return []
        
