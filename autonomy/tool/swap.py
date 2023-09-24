import autonomy as a    


class SwapTool(a.Tool):
    description = """
    Connects to the 1Inch API to swap tokens.
    """

    def call(self, tokenin: str = 'ETH', token_out: str = 'USDC', amount: int = 100):
        self.tokenin = tokenin
        self.token_out = token_out
        self.amount = amount
