import requests
import urllib.parse
import config


def search_movie(movie_name):

    base_url = 'https://api.themoviedb.org/3/search/movie'
    query = {'api_key': config.MOVIEDB_API_KEY, 'language': 'en-US',
             'query': movie_name, 'page': '1', 'include_adult': 'false'}

    query_string = urllib.parse.urlencode(query)
    print(query_string)
    url = base_url+'?'+query_string
    responses = requests.get(url)
    response = responses.json()

    if not response['results']:
        return []
    else:
        return response['results'][0]
