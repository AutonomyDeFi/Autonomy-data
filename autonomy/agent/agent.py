import autonomy as a
import json
from typing import *

class Agent(a.Block):
    description = """
    An agent has tools and memory.
    """

    def __init__(self,
                model:str='gpt-3.5-turbo-16k',
                tools: List[str]=None,
                memory : dict= {} #TODO
                ):
        self.set_tools(tools)
        self.model = model
        self.memory = memory
        self.model = a.block('llm.openai')()


    def prompt(self, task: str, memory: dict) -> str:


        prompt = f"""
        TASK/INTENT/QUESTION: 

        {task}
        
        TOOLS:

        {self.tool_info}

        MEMORY:

        {memory}

        INSTRUCTIONS:
        Suggest ONE tool to use for this task. Return in the format, 
        if you dont know the tool, return it as None.
        Only RETURN THE ANSWER if you know it. Otherwise, return None.        

        OUTPUT FORMAT:
        {{tool_name:str, tool_kwargs:dict, answer:str = None}} 

        ANSWER       
        ```json"""

        prompt = json.dumps(prompt)
        return prompt

    def call(self, task: str,
              memory : dict= {},
              max_tokens=1000, 
              min_steps = 2,
              max_steps:int=10,
              model='gpt-3.5-turbo-instruct',
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

        if 'answer' in r and step > min_steps:
            return r['answer']
        result = self.tools[r['tool_name']].call(**r['tool_kwargs'])
        history = {'tool': r['tool_name'],'result': result}
        memory['history'] = memory.get('history', []) + [history]
        if max_steps > 0:
            return self.call(task=task, memory=memory, min_steps=min_steps, step=step)
        

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

    

