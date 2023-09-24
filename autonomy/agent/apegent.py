import autonomy as a
import json
from typing import *

class Apegent(a.Block):
    description = """
    An agent has tools and memory.
    """


    def __init__(self,
                model = 'llm.openai',
                tools=['tool.inch.prices', 'tool.defillama.aave'],
                memory = {}
                ):
        self.set_tools(tools)
        self.model = a.block(model)()
        self.memory = memory

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
        


    def call(self, task: str, max_steps=10, ) -> str:
        prompt = self.prompt(task=task)
        while max_steps > 0 :
            a.call('')
            r = self.model.chat(prompt)

            try:
                assert isinstance(r, str)
                r = json.loads(r)
            except Exception as e:
                return r         

            r['finish'] = r['finish'] or r['step'] > max_steps
            r['task'] = task
            a.print(r)
            if r['finish']:
                return r['answer']

            if r['action']['tool'] != None:
                tool = r['action']['tool']
                tool_kwargs = r['action']['kwargs']
                r['memory'][tool] = self.tool[tool](**tool_kwargs)

    
            max_steps -= 1

        return r['memory']
    



    @classmethod
    def test(cls):
        self = cls()
        self.call('what is the price of eth?')

     
    def set_tools(self, tools: List[str]):
        if tools == None:
            tools = a.tools()
        self.tools = {tool: a.block(tool)() for tool in tools}
        self.tool2info = {tool_name: tool.info() for tool_name, tool in self.tools.items()}
        return {'success': True, 'msg' : f"Set tools to {tools}"}
