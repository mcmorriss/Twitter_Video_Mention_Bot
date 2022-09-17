import tweepy
import requests
from apikeys import all_keys

# Setting up api key variables
api_key = all_keys[0]
api_secret = all_keys[1]
bearer_token = all_keys[2]
access_token = all_keys[3]
access_token_secret = all_keys[4]

# Initializing the client
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Waiting on developer access to be upgraded to 'Elevated' status to continue this project.
# OAuth 1.0a User Context
# auth = tweepy.OAuth1UserHandler(
#    api_key, api_secret,
#    access_token, access_token_secret
# )
# api = tweepy.API(auth)
#
# print(api.home_timeline())

# Getting the user_id of the bot.
user = client.get_user(id=None, username="vidmentionbot")
user_id = user.data.id
print("User id: ", user_id)

# Getting a list of mentions from the bot.
mentions = client.get_users_mentions(user_id)
tweet_id = mentions.data[0].id

# Getting the mention tweet and parent tweet.
tweet = client.get_tweet(tweet_id, expansions=["referenced_tweets.id"])
parent_tweet = tweet.includes["tweets"][0]
parent_tweet_id = parent_tweet.id
print(parent_tweet)

# Use this link to get a link to a Response object from the tweet.
# https://cdn.syndication.twimg.com/tweet?id=<tweet_id>
url = f'https://cdn.syndication.twimg.com/tweet?id={parent_tweet_id}'

# Full JSON response object.
res = requests.get(url).json()

# MP4 file containing the video stored in media variable.
media = res["video"]["variants"][0]['src']

print(media)