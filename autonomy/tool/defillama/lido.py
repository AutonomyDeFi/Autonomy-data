    

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

    """

    

    def call(self, chain: str = 'Ethereum', project: str = 'lido') -> dict:
            """Initializes the state with the latest lido APY."""
            url = "https://yields.llama.fi/pools"
            # Only include parameters that are not None in the request
            if chain!=None:
                chain=str(chain).capitalize()
            params = {k: v for k, v in {'chain': chain, 'project': project}.items() if v is not None}
    
            response = requests.get(url, timeout=10, params=params)
            if response.status_code == 200:
                response_data = json.loads(response.text)
                data = response_data.get("data", [])
                
                # Filter data based on provided parameters
                filtered_data = [
                    item for item in data if 
                    (item.get("project") == project if project is not None else True) and 
                    (item.get("chain") == chain if chain is not None else True)  
                ]
                
                if filtered_data:
                    results = []
                    for item in filtered_data:
                        results.append({
                            "apy": item["apy"],
                            "market": project,
                            "chain": chain if chain is not None else item["chain"],
                            "timestamp": time.time(),
                        })
                    return results
                else:
                    return [{'error': f'No data found for the given parameters'}]
            else:
                return [{'error': f"Failed to fetch data from API -> Status code: {response.status_code}"}]

# if __name__ == "__main__":
#      lido_instance = Lido()
#      result=lido_instance.call(chain="ethereum")
#      print(result)
