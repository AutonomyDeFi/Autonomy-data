import autonomy as a

class Agent(a.Block):

    def __init__(self,
                llm = 'openai::gpt4',
                tools=[]
                ):
        self.name = name
        self.description = description
        self.tags = tags
        self.llm = llm
        self.tools = tools


    def call(self, prompt:str) -> str:
        return {
            'prompt': prompt,
            'response': 'This is a base agent that does nothing.',
            'history': []
            }

    # prompt tooling 


    @classmethod
    def find_tools(cls, prompt:str):
        raise NotImplementedError

    @classmethod
    def prompt2agent(cls, prompt:str) -> 'Agent':
        cls.find_tools(prompt, topk=5)

