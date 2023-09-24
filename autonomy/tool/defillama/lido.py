    

import autonomy as a
import requests
import json
import time
class Lido(a.Tool):
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
        lido_instance = Lido()
        result=lido_instance.call(project="lido")
        here is an example of the output that corresponds with the above input:

        [{'apy': 3.6, 'market': 'lido', 'asset': 'STETH', 'chain': 'Ethereum', 'timestamp': 1695494321.673901},
        {'apy': 4.18, 'market': 'lido', 'asset': 'STMATIC', 'chain': 'Polygon', 'timestamp': 1695494321.673903},
        {'apy': 6.51, 'market': 'lido', 'asset': 'STSOL', 'chain': 'Solana', 'timestamp': 1695494321.6739042}]

    """

    

    def call(self, chain: str = None, project: str = 'lido', symbol: str = None) -> dict:
            """Initializes the state with the latest lido APY."""
            url = "https://yields.llama.fi/pools"
            # Only include parameters that are not None in the request
            if chain!=None:
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

if __name__ == "__main__":
     lido_instance = Lido()
     result=lido_instance.call(chain="ethereum")
     print(result)
