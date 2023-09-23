
import autonomy as a

class Inch:
    def __init__(self):
        self.API_KEY = os.getenv("1INCH_API_KEY")
        self.ETHERSCAN_API_KEY=os.getenv("ETHERSCAN_API_KEY")
class SpotPrice(InchConnector):
            print("Failed to fetch token prices.")
class BalanceAPI(InchConnector):
            print("Token balance fetch failed. Please check your wallet address.")


class PortfolioAPI(InchConnector):
        return response.json()

class SwaggerInch(InchConnector):
        return json_blob
    
class SwapAPI(InchConnector):
        return {**transaction, "gas": gas_limit}
    