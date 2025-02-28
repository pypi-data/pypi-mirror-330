import tweepy
import time
import random
from datetime import datetime, timedelta
from threading import Thread
from mezo_agent.config import load_dotenv
import os

# Load environment variables
load_dotenv()

class TwitterClient:
    """
    A modular Twitter client for MezoAgent that allows characters to tweet automatically with personality.
    """

    def __init__(self, character_name: str, api_key: str, api_secret: str, access_token: str, access_secret: str, personality: str):
        """
        Initializes the Twitter client for a given character.

        :param character_name: Name of the AI character.
        :param api_key: Twitter API Key.
        :param api_secret: Twitter API Secret Key.
        :param access_token: Twitter Access Token.
        :param access_secret: Twitter Access Token Secret.
        :param personality: Custom personality description for AI-generated tweets.
        """
        self.character_name = character_name
        self.personality = personality  # ✅ Store personality

        # Authenticate with Twitter API
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        # Schedule tweets
        self.schedule_tweets()

    def generate_tweet(self) -> str:
        """
        Generates a tweet using AI for the character based on its personality.
        This function can be modified to pull from AI-generated content.

        :return: A string containing the tweet.
        """
        tweet_templates = [
            f"{self.character_name} - {self.personality}: \"Thinking about the future of DeFi... 🚀\"",
            f"{self.character_name} - {self.personality}: \"GM! Stay bullish today. 🌞\"",
            f"{self.character_name} - {self.personality}: \"On-chain or it didn't happen! ⛓️\"",
            f"{self.character_name} - {self.personality}: \"Stacking sats and stacking wisdom. 💡\"",
            f"{self.character_name} - {self.personality}: \"Wen moon? HODL tight! 🌙\""
        ]
        return random.choice(tweet_templates)

    def post_tweet(self):
        """
        Posts a tweet for the character.
        """
        try:
            tweet_content = self.generate_tweet()
            self.api.update_status(tweet_content)
            print(f"✅ {self.character_name} tweeted: {tweet_content}")
        except Exception as e:
            print(f"❌ Failed to post tweet for {self.character_name}: {e}")

    def schedule_tweets(self):
        """
        Schedules tweets to be sent 5 times per 24-hour period.
        Runs in a separate thread to avoid blocking the main agent process.
        """
        def tweet_scheduler():
            while True:
                for _ in range(5):  # Post 5 tweets per day
                    self.post_tweet()
                    sleep_time = (24 * 60 * 60) // 5  # Spread tweets across 24 hours
                    print(f"⏳ Next tweet in {sleep_time // 60} minutes...")
                    time.sleep(sleep_time)

        thread = Thread(target=tweet_scheduler, daemon=True)
        thread.start()
