from web3.exceptions import Web3Exception
import json
from mezo_agent.config import web3_instance, sender_address, account
from mezo_agent.parsing import extract_transaction_details
from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY
from langchain.tools import tool

@tool
def mezo_agent_safe_mode_btc_transaction(prompt: str) -> str:
    """
    Sends BTC on Mezo Matsnet with a Human-in-the-Loop confirmation step.

    1) Parses user prompt for transaction details.
    2) Calls LLM to provide a verbose explanation of the transaction data.
    3) Shows both raw data and LLM explanation to the user.
    4) ALWAYS prompts the user for confirmation before broadcasting.
    
    NOTE: Because this function is decorated with @tool, it can only take a
          single string argument (prompt). The confirm_before_sending parameter
          has been removed to avoid LangChain's TypeError.
    """

    # 1) Parse transaction details
    transaction_details = extract_transaction_details(prompt)
    if isinstance(transaction_details, str):
        return transaction_details  # Return parsing error if any

    amount = float(transaction_details["amount"])
    currency = transaction_details["currency"].lower()
    recipient = transaction_details["recipient"]

    if currency != "btc":
        return "❌ This function only handles BTC transactions."

    # 2) Convert to Wei (Mezo uses 18 decimals for BTC)
    amount_wei = web3_instance.to_wei(amount, "ether")

    # 3) Build transaction (do NOT send yet)
    nonce = web3_instance.eth.get_transaction_count(sender_address)
    gas_price = web3_instance.eth.gas_price
    gas_limit = web3_instance.eth.estimate_gas({"to": recipient, "value": amount_wei, "from": sender_address})

    tx_data = {
        "to": recipient,
        "value": amount_wei,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": 31611,  # Mezo Testnet chain ID
    }

    # 4) Generate LLM Explanation
    analysis_prompt = f"""
You are given the following transaction data on Mezo Matsnet:
- Recipient: {recipient}
- Amount (BTC): {amount}
- Gas Price: {gas_price}
- Gas Limit: {gas_limit}
- Nonce: {nonce}
- Chain ID: 31611 (Mezo Testnet)

Explain these details in a user-friendly way, covering:
1. The purpose of each field (nonce, gas, etc.).
2. Potential fees (approximate cost) or any known risks.
3. A short summary of what will happen if the user confirms.

Use a concise and helpful tone.
"""
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    analysis_response = llm.invoke(analysis_prompt)
    explanation_text = analysis_response.content if analysis_response else "❌ LLM explanation unavailable."

    # 5) ALWAYS confirm with the user before sending
    print("\n--- BTC Transaction Data ---")
    print(json.dumps(tx_data, indent=2))
    print("----------------------------")

    print("\n--- LLM Analysis ---")
    print(explanation_text)
    print("--------------------")

    choice = input("Do you want to proceed with this BTC transaction? [y/n]: ").strip().lower()
    if choice != 'y':
        return "❌ Transaction aborted by user."

    # 6) Sign & send
    try:
        signed_tx = account.sign_transaction(tx_data)
        tx_hash = web3_instance.eth.send_raw_transaction(signed_tx.rawTransaction)
        return f"✅ BTC transaction successful! Hash: {tx_hash.hex()}"
    except Web3Exception as e:
        return f"❌ Transaction failed: {str(e)}"

