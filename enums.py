from web3 import Web3

TOKEN_TO_ADDRESS = {
  "base": {
      "WETH": Web3.to_checksum_address("0x4200000000000000000000000000000000000006"),
      "USDT": Web3.to_checksum_address("0xC2C527C0CACF457746Bd31B2a698Fe89de2b6d49"),
      "USDC": Web3.to_checksum_address("0x07865c6E87B9F70255377e024ace6630C1Eaa37F"),
      "WBTC": Web3.to_checksum_address("0xC04B0d3107736C32e19F1c62b2aF67BE61d63a05"),
      "LINK": Web3.to_checksum_address("0x326C977E6efc84E512bB9C30f76E30c160eD06FB"),
      "LDO": Web3.to_checksum_address("0x56340274fB5a72af1A3C6609061c451De7961Bd4"),
      "rETH": Web3.to_checksum_address("0x178E141a0E3b34152f73Ff610437A7bf9B83267A"),
      "APT": Web3.to_checksum_address("0xd7A89a8DD20Cb4F252c7FB96B6421b37d82cE506")
  }
  }
COMPOUND_TOKEN_TO_ADDRESS ={
      "cUSDCv3": Web3.to_checksum_address("0x3EE77595A8459e93C2888b13aDB354017B198188"),
      "cWETHv3": Web3.to_checksum_address("0x9A539EEc489AAA03D588212a164d0abdB5F08F5F"),
      "USDC": Web3.to_checksum_address("0x07865c6E87B9F70255377e024ace6630C1Eaa37F"),
      "WBTC": Web3.to_checksum_address("0xAAD4992D949f9214458594dF92B44165Fb84dC19"),
      "WETH": Web3.to_checksum_address("0x42a71137C09AE83D8d05974960fd607d40033499")
}



