import yaml
from MultiAgentKit.Agent.DFAgent import DFAgent
import numpy as np
import os
class MAS():
    def __init__(self,system_ymal,agents_floder,agents_class_list):
        '''
        Function
        --------
        Initialize a multi-agent system.

        Parameters
        ----------
        system_ymal : str
            MAS yaml file path
        agents_floder : str
            Agent configuration folder path
        custom_agents_class : list
            _description_
        '''
        self.agents = []
        self.initSystem(system_ymal)
        self.initAgents(agents_floder,agents_class_list)
        
        self.agents_name = []
        self.agents_name_dict = {}
        self.agents_name_dict_reverse = {}
        self.agents_name_dict_reverse_list = []
    
    def initSystem(self,system_ymal):
        self.system_config = yaml.safe_load(open(system_ymal,encoding='utf-8'))
        self.__dict__.update(self.system_config)
        self.port_used_matrix = np.full(self.system_agents_port_range[1]-self.system_agents_port_range[0],False,dtype=bool)  #Agent listening port usage
        self.agent_df = DFAgent(self.system_host)
        
    def initAgents(self, agents_floder, agents_class_list):
        '''
        Function
        --------
        Initialize the agent class instance.

        Parameters
        ----------
        agents_floder : str
            Folder path to store agent configuration files
        agents_class_list : str
            List of agent classes to be instantiated, passed in by the user, must including all possible agent classes
        '''
        agent_instances = []

        # 获取文件夹中的所有YAML文件
        for filename in os.listdir(agents_floder):
            if filename.endswith(".yaml"):  # 只处理 YAML 文件
                file_path = os.path.join(agents_floder, filename)
                
                # 读取和解析 YAML 配置文件
                with open(file_path, 'r',encoding='utf-8') as file:
                    try:
                        config = yaml.safe_load(file)
                        
                        # 获取 agent_type 字段
                        agent_type = config.get('agent_type')

                        # 根据 agent_type 查找对应的类
                        agent_class = next((cls for cls in agents_class_list if cls.__name__ == agent_type), None)
                        
                        if agent_class:
                            # 实例化并保存到列表
                            index = np.where(self.port_used_matrix == False)[0][0]
                            self.port_used_matrix[index] = True
                            self.agents.append(agent_class(file_path,self.agent_df,self.system_agents_port_range[0]+index))
                        else:
                            print(f"Warning: No class found for agent_type '{agent_type}' in file {filename}")
                    except yaml.YAMLError as e:
                        print(f"Error reading YAML file {filename}: {e}")
        