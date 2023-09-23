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
        :param params: A dictionary with optional filters (chain, project, symbol, pool).
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

    """
    

    def call(self, chain: str = "ethereum", project:str = 'lido') -> None:
            """Initializes the state with the latest Lido APY."""
            url = "https://yields.llama.fi/pools"
            response = requests.get(url, timeout=10, params={'chain': chain, 'project': project})
            if response.status_code == 200:
                response_data = json.loads(response.text)
                data = response_data.get("data", [])
                lido_data = next(
                    (item for item in data if item.get("project") == project),
                    None,
                )
                if lido_data:
                    return  {
                        "apy": lido_data["apy"],
                        "market": project,
                        "asset": lido_data["symbol"],
                        "chain": lido_data["chain"],
                        "timestamp": time.time(),

                    }
                else:
                    return {'error': f'No data found for {project} Pool'}
            else:
                return {'error': f"Failed to fetch data from API -> Status code: {response.status_code}"}
