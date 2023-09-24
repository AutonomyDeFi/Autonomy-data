import autonomy as a
import json
from typing import *

class Agent(a.Block):
    description = """
    An agent has tools and memory.
    """

    def __init__(self,
                model='gpt-3.5-turbo', 
                tools=None,
                memory = {} #TODO
                ):
        self.set_tools(tools)
        self.model = model
        self.memory = memory
        self.model = a.block('llm.openai')()


    def prompt(self, task: str) -> str:
        instruction = """

        """


        prompt = f"""
        Task: {task}
        
        Tools:
        {self.tool_info}

        Memory:
        {self.memory}


        Suggest ONE tool to use for this task. Return in the format:

        ANSWER:
        {{tool_name:str, tool_kwargs:dict)}}

        '''json
        """


        prompt = json.dumps(prompt)
        return prompt

    def call(self, task: str,
              max_tokens=256, 
              max_trials:int=3) -> str:

        try:
            prompt = self.prompt(task=task)
            r = self.model.chat(prompt, model=self.model, max_tokens=max_tokens)
            r = json.loads(r.split('ANSWER:')[1].strip())
            result = self.tools[r['tool_name']].call(**r['tool_kwargs'])
        except Exception as e:
            result = {'success': False, 'msg': f"Error: {e}"}
            if 
            a.print(result)

        return result

    @classmethod
    def test(cls, tools=['tool.defillama.aave']):
        self = cls(tools=tools)
        return self.call('What is the situation with ethereum on aave?')

    def set_tools(self, tools: List[str]):
        if tools == None:
            tools = a.tools()
        self.tools = {tool: a.block(tool)() for tool in tools}
        self.tool_info = {tool_name: tool.info() for tool_name, tool in self.tools.items()}
        return {'success': True, 'msg' : f"Set tools to {tools}"}

    

