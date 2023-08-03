from datetime import datetime
from itertools import count
import os
from datetime import datetime, timezone
import logging

import tweepy

logger = logging.getLogger("twitter")

data = [
    {
        "edit_history_tweet_ids": ["1659558201040203777"],
        "id": "1659558201040203777",
        "text": "so many time with out using twitter, this is a test",
    },
    {
        "edit_history_tweet_ids": ["1659558198649470977"],
        "id": "1659558198649470977",
        "text": "@LangChainAI  has tons of more stuff on it, making our lives so much easier when developing LLM powered applications and IMO is the go to open source framework for developing LLM applications. \nhttps://t.co/Il4HMgDVcI",
    },
    {
        "edit_history_tweet_ids": ["1659558196577443840"],
        "id": "1659558196577443840",
        "text": "great day time to lean pytorch",
    },
    {
        "edit_history_tweet_ids": ["1659558193217896452"],
        "id": "1659558193217896452",
        "text": "kanlgkarrussel was amazing love their music, best artist in the world!",
    },
    {
        "edit_history_tweet_ids": ["1659558190843846657"],
        "id": "1659558190843846657",
        "text": "best desicion going to stereo picnic",
    },
]

# v1.1 api version
auth = tweepy.OAuthHandler(
    os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET")
)
auth.set_access_token(
    os.environ.get("TWITTER_ACCESS_TOKEN"), os.environ.get("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# v2 api version
twitter_client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOCKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET"),
)


def scrape_user_tweets_v1(username, num_tweets=5):
    """Scrapes a Twitter usere's original tweets (i.e. not retwwets or replies) and returns a list of dictionaries.
    each dictionary has three fields: "time_posted" (relative to nown), "text" and "usl".
    """
    tweets = api.user_timeline(screen_name=username, count=num_tweets)

    tweet_list = []

    for tweet in tweets:
        if "RT @" not in tweet.text and not tweet.text.startswith("@"):
            tweet_dict = {}
            tweet_dict["time_posted"] = str(
                datetime.now(timezone.utc) - tweet.created_at
            )
            tweet_dict["text"] = tweet.text
            tweet_dict[
                "url"
            ] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            tweet_list.append(tweet_dict)

    return tweet_list


def scrape_user_tweets_v2(username, num_tweets=5):
    """Scrapes a Twitter usere's original tweets (i.e. not retwwets or replies) and returns a list of dictionaries.
    each dictionary has three fields: "time_posted" (relative to nown), "text" and "usl".
    """

    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_user_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )
    tweet_list = []

    for tweet in tweets.data:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
        tweet_list.append(tweet_dict)

    return tweet_list


def scrape_user_tweets(username, num_tweets=5):
    """Scrapes a Twitter users's original tweets (i.e., not retweets or
    replies) and returns them as a list of dictionaries.Each dictionary has
    three fields: "time_posted" (relative to now), "text", and "url".
    """

    tweet_list = []
    for tweet in data:
        if "RT @" not in tweet["text"] and not tweet["text"].startswith("@"):
            tweet_dict = {
                "text": tweet["text"],
                "url": f"https://twitter.com/{username}/status/{tweet['id']}",
            }
            tweet_list.append(tweet_dict)
    return tweet_list


if __name__ == "__main__":
    print(scrape_user_tweets(username="@jhpiedrahitao"))
