    

import autonomy as a
import requests
import json
import time
class Lido(a.Tool):
    

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
