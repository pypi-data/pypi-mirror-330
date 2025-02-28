import os
import json
from dotenv import load_dotenv
from web3 import Web3
import importlib.resources as pkg_resources
import requests

# Load environment variables
load_dotenv()

USER_PROJECT_DIR = os.getcwd()
USER_ENV_PATH = os.path.join(USER_PROJECT_DIR, ".env")

if os.path.exists(USER_ENV_PATH):
    load_dotenv(USER_ENV_PATH)
else:
    print("⚠️ Warning: No `.env` file found in your project directory! Transactions requiring signing may fail.")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PRIVATE_KEY:
    print("⚠️ Warning: PRIVATE_KEY not set. Please create a `.env` file in your project with your keys.")
    PRIVATE_KEY = None  # Allow package to be installed but prevent transactions

# Mezo Testnet RPC and Web3 initialization
RPC_URL = "https://rpc.test.mezo.org"
web3_instance = Web3(Web3.HTTPProvider(RPC_URL))

#Graph endpoint
GRAPH_URL = "https://api.goldsky.com/api/public/project_cm48lsrzo0axx01tna6rb1ee9/subgraphs/exchange-v2-mezo/1.0.0/gn"

# Create Account Object
account = web3_instance.eth.account.from_key(PRIVATE_KEY)
sender_address = account.address

# mUSD Contract Setup using approve/allowance ABI
MUSD_ADDRESS = "0x637e22A1EBbca50EA2d34027c238317fD10003eB"
ERC20_ABI = json.loads(
    '[{"constant": true, "inputs": [{"name": "owner", "type": "address"}], '
    '"name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], '
    '"stateMutability": "view", "type": "function"},'
    '{"constant": false, "inputs": [{"name": "recipient", "type": "address"}, {"name": "amount", "type": "uint256"}],'
    '"name": "transfer", "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},'
    '{"constant": false, "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],'
    '"name": "approve", "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},'
    '{"constant": true, "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],'
    '"name": "allowance", "outputs": [{"name": "remaining", "type": "uint256"}], "stateMutability": "view", "type": "function"}]'
)

musd_contract = web3_instance.eth.contract(address=MUSD_ADDRESS, abi=ERC20_ABI)

#Query graph for token info
def query_graph(query: str) -> dict:
    """
    Queries the Goldsky GraphQL API for blockchain data.
    :param query: GraphQL query string.
    :return: JSON response as a dictionary.
    """
    response = requests.post(GRAPH_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GraphQL query failed with status code {response.status_code}")

# Wrapped BTC and Swap Router setup
WRAPPED_BTC_ADDRESS = "0xA460F83cdd9584E4bD6a9838abb0baC58EAde999"
ROUTER_ADDRESS = "0xC2E61936a542D78b9c3AA024fA141c4C632DF6c1"

# Load router ABI from a JSON file packaged with mezoAgent
with pkg_resources.open_text("mezo_agent.data", "new_router.json") as f:
    router_abi = json.load(f)

router_contract = web3_instance.eth.contract(address=ROUTER_ADDRESS, abi=router_abi)
