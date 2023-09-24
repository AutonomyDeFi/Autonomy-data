import autonomy as a
import json
from typing import *

class Agent(a.Block):
    description = """
    An agent has tools and memory.
    """

    def __init__(self,
                model:str='gpt-3.5-turbo',
                tools: List[str]=None,
                memory : dict= {} #TODO
                ):
        self.set_tools(tools)
        self.model = model
        self.memory = memory
        self.model = a.block('llm.openai')()


    def prompt(self, task: str, memory: dict) -> str:
        instruction = """

        """

        prompt = f"""
        Task: 
        {task}
        
        Tools:
        {self.tool_info}

        Memory (List[str]):
        {self.memory}

        Suggest ONE tool to use for this task. Return in the format, STOP to stop if you are SURE you have the right answer, or SKIP to skip this task.:

        ANSWER:
        {{tool_name:str, tool_kwargs:dict, stop:bool, answer:str, skip:bool}}

        '''json
        """

        prompt = json.dumps(prompt)
        return prompt

    def call(self, task: str,
              memory : dict= {},
              max_tokens=256, 
              max_trials:int=10,
              model='gpt-3.5-turbo') -> str:

        prompt = self.prompt(task=task, memory=memory)
        try:
            r = self.model.chat(prompt, model=model, max_tokens=max_tokens)
            a.print(r)
            r = json.loads(r)

        except Exception as e:
            print(e)
            r = {'error': f'Failed to chat with model {model}.'}
            if max_trials > 0:
                print(f"Retrying with {max_trials} trials left.")
                return self.call(task=task, max_trials=max_trials-1)
        if r['skip'] == True:
            return self.call(task=task, memory=memory, max_trials=max_trials-1)

        result = self.tools[r['tool_name']].call(**r['tool_kwargs'])
        memory['history'] = memory.get('history', []) + [result]
        if r['stop'] == False:
            return self.call(task=task, memory=memory, max_trials=max_trials-1)
        
        return result

    @classmethod
    def test(cls, tools=None):
        self = cls(tools=tools)
        return self.call('What is the current gas price?')

    def set_tools(self, tools: List[str]):
        if tools == None:
            tools = a.tools()
        self.tools = {tool: a.block(tool)() for tool in tools}
        self.tool_info = {tool_name: tool.info() for tool_name, tool in self.tools.items()}
        return {'success': True, 'msg' : f"Set tools to {tools}"}

    

