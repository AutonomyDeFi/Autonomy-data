import requests 
import json
from typing import Optional, Dict, Any
import time

import os
from dotenv import load_dotenv
from web3 import Web3
import autonomy as a

load_dotenv()

import autonomy as a


class RocketPool(a.Tool):       
    description = """
        Connects to the Defillama API and allows the user to select which chain, project, symbol or pool they want. 
        :param params: A dictionary with optional filters (chain (first letter uppercase), project, symbol, pool).
        :return: Filtered list of pool data.

        Example input: 
        # Fetch data for a specific chain and project
        params = {
            "chain": "Ethereum",
            "project": "lido",
        }

        here is an input:
        rocket_pool_instance = RocketPool()
        result=rocket_pool_instance.call(project="rocket-pool", symbol="RETH")
        here is an example of the output that corresponds with the above input:
        [{'apy': 3.21066, 'market': 'rocket-pool', 'asset': 'RETH', 'chain': 'Ethereum', 'timestamp': 1695494506.412746}]
    """
    





    def call(self, chain: str = None, project: str = 'rocket-pool', symbol: str = None) -> dict:
            """Initializes the state with the latest rocket-pool APY."""
            url = "https://yields.llama.fi/pools"
            # Only include parameters that are not None in the request
            chain=str(chain).capitalize()
            params = {k: v for k, v in {'chain': chain, 'project': project, 'symbol': symbol}.items() if v is not None}
    
            response = requests.get(url, timeout=10, params=params)
            if response.status_code == 200:
                response_data = json.loads(response.text)
                data = response_data.get("data", [])
                
                # Filter data based on provided parameters
                filtered_data = [
                    item for item in data if 
                    (item.get("project") == project if project is not None else True) and 
                    (item.get("chain") == chain if chain is not None else True) and 
                    (item.get("symbol") == symbol if symbol is not None else True)
                ]
                
                if filtered_data:
                    results = []
                    for item in filtered_data:
                        results.append({
                            "apy": item["apy"],
                            "market": project,
                            "asset": symbol if symbol is not None else item["symbol"],
                            "chain": chain if chain is not None else item["chain"],
                            "timestamp": time.time(),
                        })
                    return results
                else:
                    return [{'error': f'No data found for the given parameters'}]
            else:
                return [{'error': f"Failed to fetch data from API -> Status code: {response.status_code}"}]

# if __name__ == "__main__":
#      rocket_pool_instance = RocketPool()
#      result=rocket_pool_instance.call(project="rocket-pool", symbol="RETH")
#      print(result)


