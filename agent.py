class Agent():
    def __init__(self, 
                 name = 'agent', 
                 description = 'Describe what the agent does', 
                 tags = ['agent', 'defi'],
                 llm ='openai::gpt4',
                 tools = []):
        self.name = name
        self.description = description
        self.tags = tags 
        self.llm = llm
        self.tools = tools

    @classmethod
    def prompt2agent(cls, prompt:str)-> 'Agent':
        cls.find_tools(prompt, topk=5)

    @classmethod
    def find_tools(cls, prompt:str):
        #Get tools for agent 
        raise NotImplementedError

    