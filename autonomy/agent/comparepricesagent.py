import autonomy as a
import json
from typing import *

class Lending(a.Block):
    description = """
    An agent has tools and memory.
    """

    def __init__(self,
                tools: List[str]=['tool.compare_token_price', 'tool.swap'], 
                memory : dict= {} #TODO
                ):
        self.set_tools(tools)
        self.memory = memory
        self.model = a.block('llm.openai')()


    def prompt(self, task: str, memory: dict) -> str:


        prompt = f"""
        TASK/INTENT/QUESTION: 

        {task}
        
        TOOLS:

        {self.tool_info}

        HISTORY OF TOOLS USED:

        {memory}

        INSTRUCTIONS:

        Suggest ONE tool to use for this task. Return in the OUTPUT FORMAT., 
        if you dont know the tool, return it as None.
        Return the answer after the tool is used.     

        OUTPUT FORMAT:

        {{tool_name:str, tool_kwargs:dict, answer:str }} 

        ANSWER 
              
        ```json"""


        prompt = json.dumps(prompt)
        return prompt

    def call(self, task: str,
              memory : dict= {},
              max_tokens=1000, 
              min_steps = 2,
              max_steps:int=10,
              model = 'gpt-3.5-turbo-16k',
              step = 0 ) -> str:
        

        prompt = self.prompt(task=task, memory=memory)
        try:
            r = self.model.chat(prompt, model=model, max_tokens=max_tokens)
            r = r.strip()
            a.print(r)

            r = json.loads(r)
            step=step+1

        except Exception as e:
            r = {'error': f'Failed to chat with model {model}.'}
            a.print(e)

            print(f"Retrying with {max_steps} trials left.")
            return self.call(task=task, max_steps=max_steps, min_steps=min_steps, step=step)

        
        if r.get('answer', None) not in ['null', None] and step >= min_steps:
            result = r['answer']
            result = result.split()[0]
            result = self.call_tool('tool.swap', kwargs=dict(tokenin = 'ETH', token_out = 'USDC'))
            return result
        else:
            if 'tool_name' in r:
                self.call_tool(r['tool_name'], r['tool_kwargs'])
            if max_steps > 0:
                return self.call(task=task, memory=memory, min_steps=min_steps, max_steps=max_steps, step=step)
        return result

    def call_tool(self, name:str, kwargs:dict):
        a.print('[bold]Calling tool[/bold]', name, kwargs)
        result = self.tools[name].call(**kwargs)
        return result

    @classmethod
    def talk(cls,talk:str='What is the current gas price?', tools=None):
        self = cls(tools=tools)
        return self.call(talk)

    def set_tools(self, tools: List[str]):
        if tools == None:
            tools = a.tools()
        self.tools = {tool: a.get_tool(tool) for tool in tools}
        self.tool_info = {tool_name: tool.info() for tool_name, tool in self.tools.items()}
        return {'success': True, 'msg' : f"Set tools to {tools}"}

    




