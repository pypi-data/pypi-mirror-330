from mezo_agent.characters import get_character_prompt  # Import character selection
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from .config import OPENAI_API_KEY

# Initialize OpenAI Chat Model
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

@tool
def mezo_character_chat(prompt: str, character: str = "DigAIJoe") -> str:
    """
    Generates a chatbot response based on the user's input and the selected AI character.
    
    :param prompt: User's input message.
    :param character: The character's name for personality selection.
    :return: AI-generated response.
    """
    personality_prompt = get_character_prompt(character)
    query = personality_prompt + "\n\nUser: " + prompt + "\n\nAnswer accordingly."
    response = llm.invoke(query)
    return response.content.strip()

