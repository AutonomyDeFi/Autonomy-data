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

class DefiLlama(a.Tool):       
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

        here is an example of the output:

        [
            {
                'chain': 'Ethereum',
                'project': 'lido',
                'symbol': 'STETH',
                'tvlUsd': 13856337621,
                'apyBase': 3.6,
                'apyReward': None,
                'apy': 3.6,
                'rewardTokens': None,
                'pool': '747c1d2a-c668-4682-b9f9-296708a3dd90',
                'apyPct1D': 0,
                'apyPct7D': 0,
                'apyPct30D': -0.4,
                'stablecoin': False,
                'ilRisk': 'no',
                'exposure': 'single',
                'predictions': {
                    'predictedClass': 'Stable/Up',
                    'predictedProbability': 56.00000000000001,
                'binnedConfidence': 1
                },
                'poolMeta': None,
                'mu': 4.55354,
                'sigma': 0.04797,
                'count': 509,
                'outlier': False,
                'underlyingTokens': [
                    '0x0000000000000000000000000000000000000000'
                ],
                'il7d': None,
                'apyBase7d': None,
                'apyMean30d': 3.70763,
                'volumeUsd1d': None,
                'volumeUsd7d': None,
                'apyBaseInception': None
            }
        ]
        here is an input:    
        dl_instance = DefiLlama()
        result=dl_instance.call(chain="ethereum", project="compound")

        here is an example of the output that corresponds with the above input:

        [{'apy': 0.03383, 'market': 'compound', 'asset': 'WETH', 'chain': 'Ethereum', 'timestamp': 1695495056.3511412}
        {'apy': 0.02071, 'market': 'compound', 'asset': 'WBTC', 'chain': 'Ethereum', 'timestamp': 1695495056.351143}
        {'apy': 2.44336, 'market': 'compound', 'asset': 'USDC', 'chain': 'Ethereum', 'timestamp': 1695495056.351143}
        {'apy': 3.59457, 'market': 'compound', 'asset': 'USDT', 'chain': 'Ethereum', 'timestamp': 1695495056.351143}
        {'apy': 4.04343, 'market': 'compound', 'asset': 'DAI', 'chain': 'Ethereum', 'timestamp': 1695495056.3511438}
        {'apy': 0.00237, 'market': 'compound', 'asset': 'BAT', 'chain': 'Ethereum', 'timestamp': 1695495056.3511438}
        {'apy': 0.18519, 'market': 'compound', 'asset': 'UNI', 'chain': 'Ethereum', 'timestamp': 1695495056.351145}
        {'apy': 0.01424, 'market': 'compound', 'asset': 'SUSHI', 'chain': 'Ethereum', 'timestamp': 1695495056.351145}
        {'apy': 0.03629, 'market': 'compound', 'asset': 'LINK', 'chain': 'Ethereum', 'timestamp': 1695495056.351145}
        {'apy': 0.01553, 'market': 'compound', 'asset': 'COMP', 'chain': 'Ethereum', 'timestamp': 1695495056.351146}
        {'apy': 0.62444, 'market': 'compound', 'asset': 'ZRX', 'chain': 'Ethereum', 'timestamp': 1695495056.351146}
        {'apy': 0.08457, 'market': 'compound', 'asset': 'AAVE', 'chain': 'Ethereum', 'timestamp': 1695495056.351146}
        {'apy': 1.75703, 'market': 'compound', 'asset': 'TUSD', 'chain': 'Ethereum', 'timestamp': 1695495056.351147}
        {'apy': 0.32905, 'market': 'compound', 'asset': 'MKR', 'chain': 'Ethereum', 'timestamp': 1695495056.351147}
        {'apy': 0.00256, 'market': 'compound', 'asset': 'YFI', 'chain': 'Ethereum', 'timestamp': 1695495056.351147}
        {'apy': 0.45049, 'market': 'compound', 'asset': 'USDP', 'chain': 'Ethereum', 'timestamp': 1695495056.3511481}]
    """

    def call(self, chain: str = None, project: str = None, symbol: str = None) -> dict:
        """Initializes the state with the latest Defillama Pool Data."""
        url = "https://yields.llama.fi/pools"
        # Only include parameters that are not None in the request
        chain=str(chain).capitalize()

        params = {k: v for k, v in {'chain': chain.capitalize(), 'project': project, 'symbol': symbol}.items() if v is not None}

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
                        "market": project if project is not None else item["project"],
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
#      dl_instance = DefiLlama()
#      result=dl_instance.call(chain="ethereum", project="compound")
#      print(result)
