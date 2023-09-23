import requests 
import json
from typing import Optional, Dict, Any
import time

import os
from dotenv import load_dotenv
from web3 import Web3
import autonomy as a


class SwaggerInch(InchConnector):
    def get_gas_prices(self):
        """Connects to the 1Inch API for gas price

        """

        url = 'https://api.1inch.dev/gas-price/v1.4/1'
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.API_KEY}",
        }
        try:
            # Send a GET request to the API
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch data from 1Inch Gas Price API: {e}")
            return
    
        # Parse the JSON response
        response_data = response.json()
        json_blob = json.dumps(response_data, indent=4)  # Convert the Python dictionary to a JSON formatted string
        
        return json_blob
