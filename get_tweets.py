### Libraries 
import tweepy as ty 
import json 
from db_connection import get_db_connection
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

### Global variables 

KEYWORD = 'AI'
DS = datetime.now().strftime("%d/%m/%Y %H:%M")

### Class


class KeyManager:
    def __init__(self):
        """Load API keys from a config file."""
        self.keys = self.load_keys()

    def load_keys(self):
        """Fetch keys from environment variables first, fallback to config.json."""
        bearer_token = os.getenv("BEARER_TOKEN")  # Load from GitHub Secret

        if bearer_token:
            return {"BEARER_TOKEN": bearer_token}
         # Fallback to local config.json
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: config.json not found.")
            return {}  # Retorna um dicionário vazio em vez de None

class XApplication:
    def __init__(self, key_manager: KeyManager):
        """Initialize X API credentials using the provided key manager."""        
        self.bearer_token = key_manager.load_keys()['BEARER_TOKEN']
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
        
### Insert into database

def insert_tweets_into_db(keyword, tweets):
    """Insert only new tweets into the database."""
    if not tweets:
        print("No tweets to insert.")
        return
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()

        # Buscar tweets já armazenados no banco
        cur.execute("SELECT tweet_subject FROM raw.tweets_raw WHERE key_word = %s;", (keyword,))
        existing_tweets = {row[0] for row in cur.fetchall()}  # Criamos um conjunto com os tweets já armazenados

        # Filtrar apenas os tweets que ainda não foram armazenados
        new_tweets = [tweet for tweet in tweets if tweet not in existing_tweets]

        if not new_tweets:
            print("No new tweets to insert.")
            return

        insert_query = """
        INSERT INTO raw.tweets_raw (key_word, tweet_subject, ds)
        VALUES (%s, %s, %s);
        """
        
        data = [(keyword, tweet, DS) for tweet in new_tweets]

        cur.executemany(insert_query, data)
        conn.commit()
        
        print(f"Successfully inserted {len(new_tweets)} new tweets into the database!")
    
    except Exception as e:
        print(f"Error inserting tweets: {e}")
    
    finally:
        cur.close()
        conn.close()      
        
### Initialize class 

key_manager = KeyManager()
app = XApplication(key_manager)

fetcher = TweetFetcher(app)

tweets = fetcher.get_user_tweets(KEYWORD,count=10)
tweets
print('TWEETS - OK ')
# Insert into the database
insert_tweets_into_db(KEYWORD, tweets)

print('DATA INSERTED INTO DATABASE')



