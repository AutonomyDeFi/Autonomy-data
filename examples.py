

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




