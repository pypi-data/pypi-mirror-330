import time
from langchain.tools import tool
from .config import (
    web3_instance,
    sender_address,
    account,
    PRIVATE_KEY,
    musd_contract,
    ROUTER_ADDRESS,
    router_contract,
    MUSD_ADDRESS,
    WRAPPED_BTC_ADDRESS
)
from .parsing import extract_swap_details

def approve_if_needed(token_contract, amount_wei):
    """
    Checks if the router has enough allowance to spend tokens.
    If not, sends an approval transaction.
    """
    current_allowance = token_contract.functions.allowance(sender_address, ROUTER_ADDRESS).call()
    if current_allowance < amount_wei:
        print(f"Current allowance ({current_allowance}) is less than required ({amount_wei}). Approving...")
        nonce = web3_instance.eth.get_transaction_count(sender_address)
        gas_price = web3_instance.eth.gas_price
        approve_tx = token_contract.functions.approve(ROUTER_ADDRESS, amount_wei).build_transaction({
            "from": sender_address,
            "nonce": nonce,
            "gas": 50000,
            "gasPrice": gas_price,
        })
        signed_tx = web3_instance.eth.account.sign_transaction(approve_tx, PRIVATE_KEY)
        tx_hash = web3_instance.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3_instance.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status != 1:
            raise Exception("Approval transaction failed.")
        print(f"Approval successful. TX Hash: {tx_hash.hex()}")
    else:
        print("Sufficient allowance already set.")

@tool
def mezo_agent_swap_musd_btc(prompt: str) -> str:
    """
    Swaps mUSD for Wrapped BTC using the Dumpy Swap router.
    
    This tool extracts swap details from the prompt, approves the router if needed,
    and executes the swap transaction.
    
    The prompt should specify the mUSD amount to swap.
    """
    swap_details = extract_swap_details(prompt)
    if isinstance(swap_details, str):
        return swap_details

    try:
        amount_musd = float(swap_details["amount"])
    except KeyError as e:
        return f"❌ Missing key in swap details: {str(e)}"

    # For demonstration, we use a dummy minimum Wrapped BTC amount.
    min_wrapped_btc = 0.000000000000001  # in BTC

    # Convert amounts to Wei (assuming 18 decimals)
    amount_musd_wei = int(amount_musd * 10**18)
    min_wrapped_btc_wei = int(min_wrapped_btc * 10**18)
    deadline = int(time.time()) + 600  # 10 minutes from now

    # Approve the router to spend mUSD if needed
    try:
        approve_if_needed(musd_contract, amount_musd_wei)
    except Exception as e:
        return f"❌ Approval failed: {str(e)}"

    # Define the swap path: mUSD -> Wrapped BTC
    path = [MUSD_ADDRESS, WRAPPED_BTC_ADDRESS]

    nonce = web3_instance.eth.get_transaction_count(sender_address)
    gas_price = web3_instance.eth.gas_price

    try:
        swap_tx = router_contract.functions.swapExactTokensForTokens(
            amount_musd_wei,        # mUSD amount
            min_wrapped_btc_wei,     # Minimum Wrapped BTC to receive
            path,                   # Swap path
            sender_address,         # Recipient address
            deadline                # Transaction deadline
        ).build_transaction({
            "from": sender_address,
            "nonce": nonce,
            "gasPrice": gas_price,
        })
    except Exception as e:
        return f"❌ Failed to build swap transaction: {str(e)}"

    # Estimate gas and add a buffer
    try:
        estimated_gas = web3_instance.eth.estimate_gas(swap_tx)
        swap_tx["gas"] = estimated_gas + 10000
    except Exception as e:
        swap_tx["gas"] = 250000  # Fallback gas limit

    try:
        signed_swap_tx = web3_instance.eth.account.sign_transaction(swap_tx, PRIVATE_KEY)
        tx_hash = web3_instance.eth.send_raw_transaction(signed_swap_tx.raw_transaction)
    except Exception as e:
        return f"❌ Swap transaction failed: {str(e)}"

    receipt = web3_instance.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        return f"❌ Swap transaction failed. Receipt: {receipt}"
    
    return f"✅ Swap Successful! TX Hash: {tx_hash.hex()}"