import requests 
import json
from typing import Optional, Dict, Any
import time

import os
from dotenv import load_dotenv
from web3 import Web3
import autonomy as a


class Inch:
    def __init__(self, 
                 api_key: Optional[str] = '1INCH_API_KEY',
                etherscan_api_key: Optional[str] = 'ETHERSCAN_API_KEY',
                url: Optional[str] = "https://api.1inch.dev/price/v1.1/1"
                
                 ):
        load_dotenv()
        self.api_key = os.getenv(api_key, api_key)
        self.etherscan_api_key=os.getenv(etherscan_api_key, etherscan_api_key)
        self.url = url

    def get_whitelisted_token_prices(self):
        
        response = requests.get(self.url,  headers={'Authorization': f'Bearer {self.api_key}'})
        if response.status_code == 200:
            prices = response.json()
            print("Prices for whitelisted tokens:")
            for token_address, price in prices.items():
                print(f"{token_address}: {price}")
        else:
            print("Failed to fetch token prices.")

    def get_requested_token_prices(self, tokens:list[str]):

        payload = {
            "tokens": tokens
        }

        response = requests.post(self.url, json=payload)
        if response.status_code == 200:
            prices = response.json()
            print("Prices for requested tokens:")
            for token_address, price in prices.items():
                print(f"{token_address}: {price}")
        else:
            print("Failed to fetch token prices.")

    def get_prices_for_addresses(self,addresses):
        url = f"{self.url}{','.join(addresses)}"

        response = requests.get(url,  headers={'Authorization': f'Bearer {self.API_KEY}'})
        if response.status_code == 200:
            prices = response.json()
            print("Prices for requested tokens:")
            response = {}
            for token_address, price in prices.items():
                response[token_address] = price
        else:
            response =  {"error": f"Failed to fetch token prices. Error code: {response.status_code}"}

        return response
    

class BalanceAPI(InchConnector):
    """Gets the balances of a wallet address
    """
    def __init__(self,wallet_address):
        InchConnector.__init__(self)
        self.url = "https://api.1inch.dev/balance"
        
        self.wallet_address=wallet_address

    def get_token_balances(self, wallet_address):
        endpoint = f'https://api.1inch.dev/balance/v1.2/1/balances/{wallet_address}'
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.API_KEY}",
        }
        
        try:
            # Send a GET request to the API
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch data from 1Inch Balance API: {e}")
            return
    
        # Parse the JSON response
        response_data = response.json()
        json_blob = json.dumps(response_data, indent=4)  # Convert the Python dictionary to a JSON formatted string
        
        return json_blob
    def test_balance_function():
        wallet_address = '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8'
        connector = BalanceAPI(wallet_address)

        token_balances = connector.get_token_balances(wallet_address)

        if token_balances:
            print(f"Token balances for wallet address {wallet_address}:")
            token_balances_dict = json.loads(token_balances)
            with open('token_balances.txt', 'w') as file:
                # Write the wallet address and token balances to the file
                file.write(f"Token balances for wallet address {wallet_address}:\n")
                for token, balance in token_balances_dict.items():
                    balance_line = f"{token}: {balance}\n"
                    # print(balance_line)
                    file.write(balance_line)
        else:
            print("Token balance fetch failed. Please check your wallet address.")


class PortfolioAPI(InchConnector):
    def __init__(self):
        InchConnector.__init__(self)

    def get_token_prices(self, chain_id, contract_address, currency, from_timestamp, to_timestamp):
        endpoint = 'https://api.1inch.dev/portfolio/v2/token_prices/time_range'
        payload = {
            'chain_id': chain_id,
            'contract_address': contract_address,
            'currency': currency,
            'granularity': 'day',
            'from_timestamp': from_timestamp,
            'to_timestamp': to_timestamp
        }
        response = requests.post(endpoint, json=payload, headers={'Authorization': f'Bearer {self.API_KEY}'})
        return response.json().get('prices', [])

    def calculate_absolute_profit(self,chain_id, from_timestamp, to_timestamp, addresses):
        endpoint = 'https://api.1inch.dev/portfolio/v2/pnl/tokens_pnl/absolute_profit_by_portfolio_timerange'
        payload = {
            'chain_id': chain_id,
            'from_timestamp': from_timestamp,
            'to_timestamp': to_timestamp,
            'addresses': addresses
        }
        response = requests.post(endpoint, json=payload, headers={'Authorization': f'Bearer {self.API_KEY}'})
        return response.json()

    def execute_swap(src, dst, amount, from_sender, slippage=1.0):
        endpoint = 'https://api.1inch.dev/swap/v5.2/1/swap'
        payload = {
            'src': src,
            'dst': dst,
            'amount': amount,
            'from': from_sender,
            'slippage': slippage
        }
        response = requests.post(endpoint, json=payload, headers={'Authorization': f'Bearer {self.API_KEY}'})
        return response.json()

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
    
class SwapAPI(InchConnector):
    def __init__(self, chainId, web3RpcUrl):
        InchConnector.__init__(self)
        self.chainId = chainId
        self.url = f"https://api.1inch.dev/swap/v5.2/{chainId}"
        self.web3RpcUrl = web3RpcUrl
        self.web3 = Web3(web3RpcUrl)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.API_KEY}",
        }
    # Construct full API request URL
    def apiRequestUrl(self, methodName, queryParams):
        return f"{self.apiBaseUrl}{methodName}?{'&'.join([f'{key}={value}' for key, value in queryParams.items()])}"

    # Function to check token allowance
    def checkAllowance(self, tokenAddress, walletAddress):
        url = self.apiRequestUrl("/approve/allowance", {"tokenAddress": tokenAddress, "walletAddress": walletAddress})
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data.get("allowance")
    
    # async def broad_cast_raw_transaction(self, raw_transaction):
    #     data = json.dumps({"rawTransaction": raw_transaction})
    #     #broadcast to rpc w webtpy
    #     #
    #     response = await requests.post(self.url, data=data, headers=self.headers)
        
    #     if response.status_code == 200:
    #         res_json = response.json()
    #         return res_json.get("transactionHash")
    #     else:
    #         response.raise_for_status()

    # Sign and post a transaction, return its hash
    async def signAndSendTransaction(self,transaction, private_key):
        signed_transaction = self.web3.eth.account.signTransaction(transaction, private_key)
        #broadcast to rpc w web3py
        return await self.web3.send_raw_transaction(self, signed_transaction.rawTransaction)

    # Prepare approval transaction, considering gas limit
    async def buildTxForApproveTradeWithRouter(self, token_address, wallet_address, amount=None)-> Dict[str, Any]:
        # Assuming you have defined apiRequestUrl() function to construct the URL
        url = self.apiRequestUrl("/approve/transaction", {"tokenAddress": token_address, "amount": amount} if amount else {"tokenAddress": token_address})
        response = requests.get(url, headers=self.headers)
        transaction = response.json() 

        # Estimate gas limit
        wallet_address = wallet_address
        gas_limit = self.web3.eth.estimateGas(transaction, from_address=wallet_address)
        #TODO Check return type
        return {**transaction, "gas": gas_limit}
    
if __name__ == "__main__":
    # Create an instance of InchConnector
    # connector = SpotPrice()
    
    # Test get_whitelisted_token_prices
    # connector.get_whitelisted_token_prices()
    

    # Test get_prices_for_addresses
    # addresses_to_fetch = ["0x111111111117dc0aa78b770fa6a738034120c302", "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"]
    # connector.get_prices_for_addresses(addresses_to_fetch)

    # wallet_key = "0x3705f3abf7b66a80bc0f8e768cae572d7a16557b97d95314ebcee383da459c95"
    # wallet_address = "0xde0E8FCFb71Bfd049325deAf90e5B33D4F6C5BF1"
    
    # api = OrderBookAPI(wallet_key, wallet_address)
    
    # # Replace with an actual contract address
    # contract_address = "0x1111111254EEB25477B68fb85Ed929f73A960582"
    
    # # Test get_contract_abi method
    # contract_abi = api.get_contract_abi(contract_address)
    # print("Contract ABI:", contract_abi)
    
    # # Test create_contract_instance method with the obtained ABI
    # contract_instance = api.create_contract_instance(contract_address)
    # print("Contract Instance:", contract_instance)
    # connector = InchConnector()

    # print(GasPrice.get_gas_prices(connector))

    # chain_id = 1  # Mainnet Ethereum
    # contract_address_eth = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'  # Example: Ethereum (ETH)
    # contract_address_dai = '0x6B175474E89094C44Da98b954EedeAC495271d0F'  # Example: DAI stablecoin
    # currency = 'usd'
    # from_timestamp = 1625097600  # Example: July 1, 2021
    # to_timestamp = 1627776000    # Example: July 31, 2021
    # addresses = [contract_address_eth, contract_address_dai]

    # # Get token prices
    # eth_prices = PortfolioAPI.get_token_prices(chain_id, contract_address_eth, currency, from_timestamp, to_timestamp)
    # dai_prices = PortfolioAPI.get_token_prices(chain_id, contract_address_dai, currency, from_timestamp, to_timestamp)

    # print("Ethereum Prices:")
    # print(eth_prices)
    # print("DAI Prices:")
    # print(dai_prices)

    # # Calculate absolute profit
    # profit_data = PortfolioAPI.calculate_absolute_profit(chain_id, from_timestamp, to_timestamp, addresses)
    # absolute_profit = profit_data.get('absolute_profit', 0)
    # profit_currency = profit_data.get('currency', 'USD')

    # print(f"Absolute Profit: {absolute_profit} {profit_currency}")

    # # Execute a token swap
    # from_token_address = contract_address_eth
    # to_token_address = contract_address_dai
    # amount_to_swap = 1.0  # Replace with the desired amount to swap
    # user_address = '0xYourAddress'  # Replace with the user's Ethereum address

    # swap_result = PortfolioAPI.execute_swap(from_token_address, to_token_address, amount_to_swap, user_address)
    # print("Swap Result:")
    # print(swap_result)





    # def get_token_balances(wallet_address):
    #     endpoint = f'https://api.1inch.dev/balance/v1.2/1/balances/{wallet_address}'
    #     response = requests.get(endpoint)

    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         print(f"Failed to fetch token balances. Error code: {response.status_code}")
    #         return None


    # wallet_address = '0x0a2648aD71b4d80b08323dDa7e8AA412356C072b'
    # token_balances = get_token_balances(wallet_address)

    # if token_balances:
    #     print(f"Token balances for wallet address {wallet_address}:")
    #     for token, balance in token_balances.items():
    #         print(f"{token}: {balance}")
    # else:
    #     print("Token balance fetch failed. Please check your wallet address.")

    BalanceAPI.test_balance_function()