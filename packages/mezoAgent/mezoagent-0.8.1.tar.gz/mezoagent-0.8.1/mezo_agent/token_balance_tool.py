from langchain.tools import tool
from mezo_agent.config import web3_instance, sender_address, ERC20_ABI
from mezo_agent.parsing import extract_balance_details
from mezo_agent.token_utils import get_token_address_by_symbol  

@tool
def mezo_agent_token_balance_tool(balance_prompt: str) -> str:
    """
    Queries the wallet balance for a specified token on Mezo Matsnet.

    :param balance_prompt: User query containing the token symbol.
    :return: Token balance for the sender's address.
    """
    details = extract_balance_details(balance_prompt)

    if isinstance(details, str):  # Handle extraction errors
        return details

    token_symbol = details.get("token_symbol")
    if not token_symbol:
        return "❌ Could not extract token symbol for balance query."

    try:
        # Get the contract address dynamically
        token_address = get_token_address_by_symbol(token_symbol)
        print(f"✅ Using token address: {token_address}")  # Debugging

        token_contract = web3_instance.eth.contract(address=token_address, abi=ERC20_ABI)

        # Fetch balance
        balance_wei = token_contract.functions.balanceOf(sender_address).call()
        balance = web3_instance.from_wei(balance_wei, "ether")
        return f"✅ {token_symbol.upper()} Balance: {balance}"
    except Exception as e:
        return f"❌ Failed to fetch balance: {str(e)}"

