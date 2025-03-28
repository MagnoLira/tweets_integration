### Libraries 
import pandas as pd 
import tweepy as ty 
import numpy as np
import json 
import requests

### Class


class KeyManager:
    def __init__(self):
        """Load API keys from a config file."""
        self.keys = self.load_keys()

    def load_keys(self):
        """Fetch keys from config.json."""
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: config.json not found.")
            return None

class XApplication:
    def __init__(self, key_manager: KeyManager):
        """Initialize X API credentials using the provided key manager."""
        self.bearer_token = key_manager.keys["BEARER_TOKEN"]  # Adicione essa chave no config.json
        self.client = ty.Client(bearer_token=self.bearer_token)

class TweetFetcher:
    def __init__(self, x_app: XApplication):
        """Initialize with XApplication credentials."""
        self.client = x_app.client

    def get_user_tweets(self, username, count=10):
        """Fetch recent tweets from a specific user using Tweepy (API v2)."""
        try:
            query = f"from:{username} -is:retweet"
            tweets = self.client.search_recent_tweets(query=query, max_results=count)

            if tweets.data:
                return [tweet.text for tweet in tweets.data]
            else:
                print("No tweets found.")
                return None
        except ty.TweepyException as e:
            print(f"Error: {e}")
            return None
        
### Initialize class 

key_manager = KeyManager()
app = XApplication(key_manager)

fetcher = TweetFetcher(app)
tweets = fetcher.get_user_tweets('AI',count=10)