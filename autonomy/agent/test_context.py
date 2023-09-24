import json
from typing import List, Dict, Any

EXAMPLES ="""

    examples_dict = {
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
                    "output": "
                    (f"{token_address}: {price}"
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
        }

    }

"""
class ContextAgent:
    def __init__(self, model: str, tools: List[str], memory: dict):
        self.model = model
        self.tools = tools
        self.memory = memory

    def call(self, task: str, prompt: str) -> Dict[str, Any]:
        # Use the custom prompt along with the task to understand the context
        # For simplicity, we are returning a dummy context.
        print(f"ContextAgent Prompt: {prompt}")
        return {"context": "relevant context information"}

class TaskAgent:
    def __init__(self, model: str, tools: List[str], memory: dict):
        self.model = model
        self.tools = tools
        self.memory = memory

    def call(self, context: Dict[str, Any], prompt:str) -> List[Dict[str, Any]]:
        # Use the custom prompt along with the context to create tasks
        # For simplicity, we are returning dummy tasks.
        task_prompt = f"You are a task creation AI that uses the result of an execution agent to create new tasks with the following objective: {prompt}. These are some of the tools you can access: [
            'tool',
            'tool.compare_token_price',
            'tool.defillama',
            'tool.defillama.aave',
            'tool.swap',
            'tool.defillama.lido',
            'tool.defillama.rocketpool',
            'tool.get_best_apy',
            'tool.inch',
            'tool.inch.balances',
            'tool.inch.gasprice',
            'tool.inch.prices',
            'tool.read_file',
            'tool.write_file']
            Use the following examples to understand the types of tasks you can create and the tools you can access: {EXAMPLES}"

        print(f"TaskAgent Prompt: {prompt}")
        return [{"task_id": 1, "task_name": "Check gas price"}, {"task_id": 2, "task_name": "Swap Eth to USDC"}]

class ExecutionAgent:
    def __init__(self, model: str, tools: List[str], memory: dict):
        self.model = model
        self.tools = tools
        self.memory = memory

    def call(self, tasks: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
        # Use the custom prompt along with the tasks to execute them and return the results
        # For simplicity, we are returning dummy results.
        print(f"ExecutionAgent Prompt: {prompt}")
        results = []
        for task in tasks:
            results.append({"task_id": task["task_id"], "result": "Task executed successfully"})
        return results


# Initialize the agents
context_agent = ContextAgent(model="gpt-3.5-turbo", tools=[], memory={})
task_agent = TaskAgent(model="gpt-3.5-turbo", tools=[], memory={})
execution_agent = ExecutionAgent(model="gpt-3.5-turbo", tools=[], memory={})

# Define custom prompts
context_prompt = f"""
        TASK/INTENT/QUESTION: 

        {task}
        
        TOOLS:

        {self.tool_info}

        MEMORY:

        {memory}

        INSTRUCTIONS:
        Suggest 1 tool to use for this task. Return in the format, 
        if you dont know the tool, return it as None.
        Only RETURN THE ANSWER if you know it. Otherwise, return None.        

        OUTPUT FORMAT:
        {{tool_name:str, tool_kwargs:dict, answer:str = None}} 

        Here are some examples of an end-to-end workflow:

        {EXAMPLES}
    
        ANSWER       
        ```json""""
task_prompt = f"You are an task creation AI that uses the result of an execution agent to create new tasks with the following objective: {objective}, The last completed task has the result: {result}. This result was based on this task description: {task_description}. These are incomplete tasks: {', '.join(task_list)}. Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks. Return the tasks as an array. Use the following file to understand the types of tasks you can create and the tools you can access."

execution_prompt = "Execute the tasks and provide results."

# Call the agents in sequence with custom prompts
context = context_agent.call("Swap $100 of my Eth to USDC if gas is under $1", context_prompt)
tasks = task_agent.call(context, task_prompt)
print(tasks)
results = execution_agent.call(tasks, execution_prompt)
print(results)

# Print the results
print(json.dumps(results, indent=2))

