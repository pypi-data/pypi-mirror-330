from mezo_agent.config import web3_instance, query_graph
from mezo_agent.token_utils import get_token_address_by_symbol  # ✅ Import from token_utils.py

def get_token_price(token_symbol: str) -> str:
    """
    Fetches the price of a given token in USD and ETH from the Goldsky subgraph.
    
    :param token_symbol: The token symbol (e.g., 'MUSD', 'WBTC').
    :return: A formatted string with the token price in USD and ETH.
    """
    if token_symbol.lower() == "btc":
        token_symbol = "wtbtc"

    try:
        token_address = get_token_address_by_symbol(token_symbol)  # ✅ Now correctly imported
    except Exception as e:
        return f"❌ Token lookup error: {e}"

    token_id = token_address.lower()
    query = f'''
    {{
      token(id: "{token_id}") {{
        id
        decimals
        derivedUSD
        derivedETH
      }}
    }}
    '''
    try:
        result = query_graph(query)
        token_data = result["data"]["token"]
        if token_data is None:
            return f"❌ Price data for token {token_symbol.upper()} not found."
        derivedUSD = token_data.get("derivedUSD", "N/A")
        derivedETH = token_data.get("derivedETH", "N/A")
        return f"✅ Price of {token_symbol.upper()}: {derivedUSD} USD, {derivedETH} ETH."
    except Exception as e:
        return f"❌ Failed to get price data: {e}"
