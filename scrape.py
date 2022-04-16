"""
Tweet scraper script
"""

import os
from twint_utils import save_tweets_as_csv

FILENAME = 'tweets.csv'

if os.path.exists(FILENAME):
    os.remove(FILENAME)

search_query = {'Search': '#csed OR #csedu OR #teachcs', 'Limit': 10000, 'Output': FILENAME}
save_tweets_as_csv(**search_query)
