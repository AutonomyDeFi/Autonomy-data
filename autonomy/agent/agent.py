import autonomy as a
import json
from typing import *

class Agent(a.Block):
    description = """
    An agent has tools and memory.
    """

    def __init__(self,
                tools=None,
                memory = {} #TODO
                ):
        self.set_tools(tools)
        self.memory = memory
        self.model = a.block('llm.openai')()


    def prompt(self, task: str) -> str:
        instruction = """
        Your goal is to use the tools and memory to answer the question.
        - To use a tool, call it by filling our the tool and kwargs fields in the 'action'.
        - You can use the memory to store information while you work. BE CONSICE AS WE ARE LIMITED TO 1000 CHARACTERS.
        - When you are done, set the 'finish' field to True and the answer field to your answer.
        """

        prompt = {
            'task': task,
            'tools': self.tool2info,
            'memory': self.memory,
            'answer': None,
            'action': {'tool': None, 'kwargs': {}},
            'instructions': instruction,
            'finish': False,
            'step': 0
        }

        prompt = json.dumps(prompt)
        return prompt

    def call(self, task: str, max_steps=10, max_tokens=10, model='gpt-3.5-turbo') -> str:


        prompt = self.prompt(task=task)
        r = self.model.chat(prompt, model=model, max_tokens=max_tokens)
        return r

    @classmethod
    def test(cls):
        self = cls()
        return self.call('what is the price of eth?')

    def set_tools(self, tools: List[str]):
        if tools == None:
            tools = a.tools()
        self.tools = {tool: a.block(tool)() for tool in tools}
        self.tool2info = {tool_name: tool.info() for tool_name, tool in self.tools.items()}
        return {'success': True, 'msg' : f"Set tools to {tools}"}

    

