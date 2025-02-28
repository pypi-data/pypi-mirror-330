from web3.exceptions import Web3Exception
from langchain.tools import tool
from .config import web3_instance, sender_address, account, musd_contract
from .parsing import extract_transaction_details

@tool
def mezo_agent_transaction_btc(transaction_prompt: str) -> str:
    """
    Sends BTC on Mezo Matsnet. Parses a transaction request and executes the transfer.
    """
    transaction_details = extract_transaction_details(transaction_prompt)

    if isinstance(transaction_details, str):  # Handle errors
        return transaction_details

    amount = float(transaction_details["amount"])
    currency = transaction_details["currency"].lower()
    recipient = transaction_details["recipient"]

    if currency != "btc":
        return "❌ This function only supports BTC transactions."

    # Convert amount to Wei (BTC uses 18 decimals on Mezo Matsnet)
    amount_wei = web3_instance.to_wei(amount, "ether")

    # Check sender's BTC balance
    sender_balance = web3_instance.eth.get_balance(sender_address)
    sender_balance_btc = web3_instance.from_wei(sender_balance, "ether")

    if sender_balance < amount_wei:
        return f"❌ Insufficient BTC balance! You have {sender_balance_btc} BTC but need {amount} BTC."

    # Fetch nonce and gas price
    nonce = web3_instance.eth.get_transaction_count(sender_address, 'pending')
    gas_price = web3_instance.eth.gas_price
    gas_limit = web3_instance.eth.estimate_gas({"to": recipient, "value": amount_wei, "from": sender_address})

    tx = {
        "to": recipient,
        "value": amount_wei,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": 31611,  # Mezo Testnet Chain ID
    }

    try:
        # Sign and send the transaction
        signed_tx = account.sign_transaction(tx)
        tx_hash = web3_instance.eth.send_raw_transaction(signed_tx.raw_transaction)
        return f"✅ BTC Transaction Successful! Hash: {tx_hash.hex()}"
    except Web3Exception as e:
        return f"❌ BTC Transaction Failed: {str(e)}"
    
@tool
def mezo_agent_musd_transaction(transaction_prompt: str) -> str:
    """
    Sends mUSD on Mezo Matsnet. Parses a transaction request and executes the transfer.

    The transaction_prompt should contain details including the amount, the currency 
    (which must be "mUSD"), and the recipient's wallet address.
    """
    transaction_details = extract_transaction_details(transaction_prompt)

    if isinstance(transaction_details, str):  # Handle errors during extraction
        return transaction_details

    amount = float(transaction_details["amount"])
    currency = transaction_details["currency"].lower()
    recipient = transaction_details["recipient"]

    if currency != "musd":
        return "❌ This function only supports mUSD transactions."

    # Convert the mUSD amount to its smallest unit (assumes 18 decimals, similar to ETH)
    amount_token = web3_instance.to_wei(amount, "ether")

    try:
        # Fetch nonce and gas price for the sender
        nonce = web3_instance.eth.get_transaction_count(sender_address, 'pending')
        gas_price = web3_instance.eth.gas_price

        # Estimate gas required for the token transfer
        gas_limit = musd_contract.functions.transfer(recipient, amount_token).estimate_gas({
            'from': sender_address
        })
    except Exception as e:
        return f"❌ Failed to prepare mUSD transaction: {str(e)}"

    # Build the transaction for the token transfer
    tx = musd_contract.functions.transfer(recipient, amount_token).build_transaction({
        'chainId': 31611,  # Mezo Testnet Chain ID
        'from': sender_address,
        'nonce': nonce,
        'gas': gas_limit,
        'gasPrice': gas_price
    })

    try:
        # Sign and send the transaction
        signed_tx = account.sign_transaction(tx)
        tx_hash = web3_instance.eth.send_raw_transaction(signed_tx.raw_transaction)
        return f"✅ mUSD Transaction Successful! Hash: {tx_hash.hex()}"
    except Web3Exception as e:
        return f"❌ mUSD Transaction Failed: {str(e)}"