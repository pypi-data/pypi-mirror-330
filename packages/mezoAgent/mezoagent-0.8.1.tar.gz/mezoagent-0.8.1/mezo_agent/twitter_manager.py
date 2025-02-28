import os
import json

class TwitterManager:
    """
    Manages Twitter clients for MezoAgent characters.
    """

    def __init__(self, config_file="twitter_config.json"):
        """
        Initializes the Twitter Manager.

        :param config_file: The JSON file that stores character Twitter credentials.
        """
        self.config_file = config_file
        self.characters = {}
        self.load_characters()

    def load_characters(self):
        """
        Loads characters and their Twitter credentials from a JSON config file.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.characters = json.load(f)

    def save_characters(self):
        """
        Saves character Twitter credentials to a JSON config file.
        """
        with open(self.config_file, "w") as f:
            json.dump(self.characters, f, indent=4)

    def add_character(self, character_name: str, api_key: str, api_secret: str, access_token: str, access_secret: str, personality: str):
        """
        Registers a character with Twitter API credentials and starts their Twitter client.

        :param character_name: Name of the character.
        :param api_key: Twitter API Key.
        :param api_secret: Twitter API Secret Key.
        :param access_token: Twitter Access Token.
        :param access_secret: Twitter Access Token Secret.
        :param personality: Custom personality description for AI-generated tweets.
        """
        from mezo_agent.twitter_client import TwitterClient  # ✅ Move import inside the function

        if character_name in self.characters:
            print(f"❌ Character '{character_name}' already has a Twitter client.")
            return

        self.characters[character_name] = {
            "api_key": api_key,
            "api_secret": api_secret,
            "access_token": access_token,
            "access_secret": access_secret,
            "personality": personality
        }
        self.save_characters()
        print(f"✅ Character '{character_name}' registered for Twitter with personality!")

        # Start the Twitter client with personality
        TwitterClient(character_name, api_key, api_secret, access_token, access_secret, personality)

