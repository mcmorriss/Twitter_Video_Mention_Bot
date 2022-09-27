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


# Waiting
# OAuth 1.0a User Context
auth = tweepy.OAuth1UserHandler(
   api_key, api_secret,
   access_token, access_token_secret
)
api = tweepy.API(auth)


user = client.get_user(id=None, username="vidmentionbot")
user_id = user.data.id

print("User id: ", user_id)

mentions = client.get_users_mentions(user_id)
tweet_id = mentions.data[0].id

print(mentions)
print(api.mentions_timeline()[0]._json["user"]["id"])

# Getting id of user who mentioned the bot.
mention_id = api.mentions_timeline()[0]._json["user"]["id_str"]
print(api.get_user(user_id=mention_id))

# Accessing media file associated with tweet.
tweet = client.get_tweet(tweet_id, expansions=["referenced_tweets.id"])
parent_tweet = tweet.includes["tweets"][0]
parent_tweet_id = parent_tweet.id
print(parent_tweet)

# Use this link to get a link to a Response object from the tweet.
# https://cdn.syndication.twimg.com/tweet?id=<tweet_id>
url = f'https://cdn.syndication.twimg.com/tweet?id={parent_tweet_id}'
res = requests.get(url).json()
media = res["video"]["variants"][0]['src']

print(media)


# Uploading media to twitter to get media id.
r = requests.get(media, allow_redirects=True)
open('vid_mention.mp4', 'wb').write(r.content)

media_object = api.media_upload(filename='vid_mention.mp4', chunked=True)

print(media_object.media_id)

# # Sending the direct message.
api.send_direct_message(recipient_id=mention_id,
                        text="Here is an MP4 file containing your video! Thanks ",
                        attachment_type="media",
                        attachment_media_id=media_object.media_id)
