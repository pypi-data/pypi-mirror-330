from mezo_agent.config import query_graph, web3_instance

def get_token_address_by_symbol(symbol: str) -> str:
    """
    Fetches the token contract address dynamically from the Goldsky subgraph.
    :param symbol: Token symbol (e.g., 'MUSD', 'WBTC').
    :return: Ethereum checksum address of the token.
    """
    if symbol.lower() == "btc":
        symbol = "wtbtc"

    query_all = '''
    {
      tokens(first: 100) {
        id
        symbol
      }
    }
    '''
    data = query_graph(query_all)
    tokens = data.get("data", {}).get("tokens", [])

    matching_tokens = [t for t in tokens if t["symbol"].lower() == symbol.lower()]
    
    if matching_tokens:
        token_address = matching_tokens[0]["id"]
        checksum_address = web3_instance.to_checksum_address(token_address)
        print(f"✅ Token {symbol} found at address: {checksum_address}")  # Debugging
        return checksum_address
    else:
        available_symbols = [t["symbol"] for t in tokens]
        raise Exception(f"❌ Token '{symbol}' not found. Available: {', '.join(available_symbols)}")
