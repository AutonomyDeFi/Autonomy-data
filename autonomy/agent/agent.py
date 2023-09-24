import autonomy as a
import json
from typing import *

EXAMPLES={
    "example1": {
        "natural_lang_input": "Swap $100 of my Eth to USDC if gas is under $1",
        "tasks": {
            "1": {
                "task": "Check 1 inch gas",
                "tool_name": "tool.inch.gasprice",
                "output": "Gas price retrieved"
            },
            "2": {
                "task": "If the price <$1, use Swap Tool for $100",
                "tool_name": "tool.swap",
                "output": "Swap executed"
            }
        },
        "final_output": "0xc07215bf4af1ce282280c18e7470cba57fb83138b4df62fb0d4ded9133e61d93"
    },
    "example2": {
        "natural_lang_input": "Here is $100. Get me the highest staking APY on my USDC.",
        "tasks": {
            "1": {
                "task": "Use Balance agent to check my balance and make sure I have USDC",
                "tool_name": "tool.inch.balances",
                "output": "Balance checked, USDC available"
            },
            "2": {
                "task": "Ask DeFi llama to check the APYs for lido",
                "tool_name": "tool.lido",
                "output": "APY retrieved for lido"
            },
            "3": {
                "task": "Ask DeFi llama to check the APYs for rocket-pool",
                "tool_name": "tool.rocket-pool",
                "output": "APY retrieved for rocket-pool"
            },
            "4": {
                "task": "Use highest APY tool to get APY",
                "tool_name": "tool.get_best_apy",
                "output": "Highest APY retrieved"
            }
        },
        "final_output": "0xc07215bf4af1ce282280c18e7470cba57fb83138b4df62fb0d4ded9133e61d93"
    }, 
    "example3": {
        "natural_lang_input": "Split $50 between Rocketpool and Lido",
        "tasks": {
            "1": {
                "task": "Ask the Balance agent how much USDC the user has",
                "tool_name": "tool.inch.balances",
                "output": "Balance checked, USDC available"
            },
            "2": {
                "task": "Ask DeFi llama to check the APYs for lido",
                "tool_name": "tool.lido",
                "output": "APY retrieved for lido"
            },
            "3": {
                "task": "Stake half the money ($25) with Rocketpool",
                "tool_name": "tool.rocket-pool-stake",
                "output": "Transaction Hash"
            },
            "4": {
                "task": "Stake half the money ($25) with Lido",
                "tool_name": "tool.lido-stake",
                "output": "Transaction hash"
            }
        },
        "final_output": "2 Transaction Hashes"
    }, 
    "example4": {
        "natural_lang_input": "Check the price of all my tokens, sell the cheapest one, and buy the more expensive one",
        "tasks": {
            "1": {
                "task": "Get the balances of all tokens in a user's wallet",
                "tool_name": "tool.inch.balances",
                "output": "json_blob of balances"
            },
            "2": {
                "task": "Send in the token addresses and get the prices of all tokens",
                "tool_name": "tool.Inch.get_requested_token_prices",
                "output": """(f"{token_address}: {price}"""
            },
            "3": {
                "task": "Find the cheapest token",
                "tool_name": "tool.cheapest_token",
                "output": "Token symbol"
            },
            "4": {
                "task": "Sell the cheapest token",
                "tool_name": "tool.swap",
                "output": "Transaction Hash"
            },
            "5": {
                "task": "Buy the more expensive token",
                "tool_name": "tool.swap",
                "output": "Transaction hash"
            }
        },
        "final_output": "2 Transaction Hashes"
    },
    "example5": {
            "natural_lang_input": "compare the token price between USDC and ETH and buy the cheapest one",
            "tasks": {
                "1": {
                    "task": "Compare the price of USDC and ETH and find which one is higher",
                    "tool_name": "tool.compare_token_price",
                    "output": "token name"
                },
                "2": {
                    "task": "Buy the cheapest token which is the input of the previous task",
                    "input": "task1 tool name",
                    "tool_name": "tool.swap",
                    "output": "Transaction Hash"
                },
            },
            "final_output": "Transaction Hash"
        }

}

class Agent(a.Block):
    description = """
    An agent has tools and memory.
    """

    def __init__(self,
                tools: List[str]=None,
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

        MEMORY:

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

        a.print(memory, r)
        if r.get('answer', None) not in ['null', None] and step >= min_steps:
            return r['answer']
        if 'tool_name' in r:
            a.print('[bold]Calling tool[/bold]', r['tool_name'], r['tool_kwargs'])

            result = self.tools[r['tool_name']].call(**r['tool_kwargs'])
            memory[r['tool_name']] =  {'tool': r['tool_name'],
                                        'result': result, 
                                        'kwargs': r['tool_kwargs']}
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

    

