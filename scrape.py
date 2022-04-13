"""
Tweet scraper script
"""

from twint_utils import save_tweets_as_csv

search_query = {'Search': '#csed OR #csedu OR #teachcs', 'Limit': 10000, 'Output': 'tweets.csv'}
save_tweets_as_csv(**search_query)
