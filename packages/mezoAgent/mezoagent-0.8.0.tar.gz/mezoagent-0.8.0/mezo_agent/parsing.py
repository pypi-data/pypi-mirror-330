from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY

# Define the expected response schema for extracting transaction details
response_schemas = [
    ResponseSchema(name="amount", description="The amount of cryptocurrency to transfer."),
    ResponseSchema(name="currency", description="The cryptocurrency (BTC or mUSD)."),
    ResponseSchema(name="recipient", description="The recipient's wallet address."),
]

# Initialize the structured output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Instantiate the ChatOpenAI LLM
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# Prepare the prompt template
prompt_template = PromptTemplate(
    template="Extract transaction details from this request:\n{input}\n{format_instructions}",
    input_variables=["input"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)

def extract_transaction_details(prompt: str):
    """
    Uses LLM to extract structured transaction details from user input.
    """
    formatted_prompt = prompt_template.format(input=prompt)
    response = llm.invoke(formatted_prompt)

    try:
        return output_parser.parse(response.content)
    except Exception as e:
        return f"❌ Failed to extract transaction details: {str(e)}"
    

swap_response_schemas = [
    ResponseSchema(name="amount", description="The amount of mUSD to swap."),
    ResponseSchema(name="from_currency", description="The token to swap from (should always be 'mUSD')."),
    ResponseSchema(name="to_currency", description="The token to receive (should always be 'BTC')."),
    ResponseSchema(name="router_address", description="The Dumpy Swap router address for executing the swap."),
]
swap_output_parser = StructuredOutputParser.from_response_schemas(swap_response_schemas)

swap_prompt_template = PromptTemplate(
    template=(
        "Extract swap transaction details from this request:\n{input}\n\n"
        "- The token to swap from should always be 'mUSD'.\n"
        "- The token to receive should always be 'BTC'.\n"
        "- The router address should always be '0xC2E61936a542D78b9c3AA024fA141c4C632DF6c1'.\n\n"
        "{format_instructions}"
    ),
    input_variables=["input"],
    partial_variables={"format_instructions": swap_output_parser.get_format_instructions()},
)

def extract_swap_details(prompt: str):
    formatted_prompt = swap_prompt_template.format(input=prompt)
    response = llm.invoke(formatted_prompt)
    try:
        return swap_output_parser.parse(response.content)
    except Exception as e:
        return f"Failed to extract swap details: {str(e)}"
    
#Balance check parsing 

balance_response_schema = [
    ResponseSchema(name="token_symbol", description="The token symbol to check the balance for (e.g., 'MUSD').")
]

balance_output_parser = StructuredOutputParser.from_response_schemas(balance_response_schema)

balance_prompt_template = PromptTemplate(
    template="""Output a JSON object with the following key:
- token_symbol: (string) The token symbol for which to check the balance (e.g., "MUSD").

Extract this detail from the following query:
{input}

Your output must be a valid JSON object with no additional text.
""",
    input_variables=["input"],
)

def extract_balance_details(prompt: str):
    formatted_prompt = balance_prompt_template.format(input=prompt)
    response = llm.invoke(formatted_prompt)
    print("LLM raw balance response:", response.content)
    try:
        return balance_output_parser.parse(response.content)
    except Exception as e:
        return f"Failed to extract balance details: {str(e)}"
    
#Price parsing 
price_response_schema = [
    ResponseSchema(name="token_symbol", description="The token symbol to check the price for (e.g., 'LIMPETH').")
]
price_output_parser = StructuredOutputParser.from_response_schemas(price_response_schema)

price_prompt_template = PromptTemplate(
    template="""Output a JSON object with the following key:
- token_symbol: (string) The token symbol for which to check the price (e.g., "LIMPETH").

Extract this detail from the following request:
{input}

Your output must be a valid JSON object with no additional text.
""",
    input_variables=["input"],
)

def extract_price_details(prompt: str):
    """
    Parses a price query and extracts the token symbol.
    
    :param prompt: User input asking for a token price.
    :return: Dictionary containing the token symbol or an error message.
    """
    formatted_prompt = price_prompt_template.format(input=prompt)
    response = llm.invoke(formatted_prompt)
    print("LLM raw price response:", response.content)  # Debugging
    try:
        return price_output_parser.parse(response.content)
    except Exception as e:
        return f"❌ Failed to extract price details: {str(e)}"
