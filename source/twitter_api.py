import config
import twitter
import json
import requests
from pprint import pprint
from flask import jsonify
import time
from opencage.geocoder import OpenCageGeocode
from textblob import TextBlob


def generate_heatmap_data(movie_title):
    opencage_api_key = config.OPENCAGE_API_KEY
    geocoder = OpenCageGeocode(opencage_api_key)
    twitter_api = twitter.Api(consumer_key=config.TWITTER_CONSUMER_KEY,
                              consumer_secret=config.TWITTER_CONSUMER_SECRET,
                              access_token_key=config.TWITTER_ACCESS_TOKEN_KEY,
                              access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET)
    search_results = twitter_api.GetSearch(
        term=movie_title, include_entities=True, count=10)
    coordinates = []
    positive_tweets = []
    # Get location of tweets by using user's location
    for result in search_results:
        pprint(result)
        analysis = TextBlob(result.text)
        print(analysis.sentiment)
        if analysis.sentiment[0] > 0:
            # print('Positive')
            positive_tweets.append(result.text)

        user = twitter_api.GetUser(user_id=result.user.id)
        pprint(user.location)
        if not user.location:
            continue
        else:
            location = geocoder.geocode(user.location)  # get lat long

            if(not location):
                continue
            else:
                # pprint(location[0]['geometry']['lat'])
                # pprint(location[0]['geometry']['lng'])
                coordinates.append(
                    {"lat": location[0]['geometry']['lat'],
                     "lng": location[0]['geometry']['lng'],
                     "count": 5})

            time.sleep(1)
        print("--------------------------------------------------------------------------------------------")
    return [coordinates, positive_tweets]


# generate_heatmap_data("Andhadhun")
