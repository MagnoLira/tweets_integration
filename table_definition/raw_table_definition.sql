create_table_query = """
CREATE TABLE IF NOT EXISTS raw.tweets_raw (
    key_word VARCHAR(255),                    
    tweet_subject TEXT,
    ds VARCHAR(255)
);
"""

### key_word is the search parameter
### tweet_subject is the subject of the tweet
### ds is when the data was inserted on the table 