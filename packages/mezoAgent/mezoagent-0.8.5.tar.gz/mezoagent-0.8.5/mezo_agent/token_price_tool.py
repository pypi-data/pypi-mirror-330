from langchain.tools import tool
from mezo_agent.config import query_graph
from mezo_agent.parsing import extract_price_details
from mezo_agent.utils import get_token_price  # ✅ Correct import

@tool
def mezo_agent_token_price_tool(price_prompt: str) -> str:
    """
    Queries the price of a specified token in USD and ETH on Mezo Matsnet.

    :param price_prompt: User query containing the token symbol.
    :return: Token price details.
    """
    details = extract_price_details(price_prompt)

    if isinstance(details, str):  # Handle extraction errors
        return details

    token_symbol = details.get("token_symbol")
    if not token_symbol:
        return "❌ Could not extract token symbol for price query."

    try:
        # Get the token price
        return get_token_price(token_symbol)
    except Exception as e:
        return f"❌ Failed to fetch token price: {str(e)}"

