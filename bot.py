import requests
from config import kpUnofficial_api, telegram_api, youtube_api

headers = {
        'X-API-KEY': kpUnofficial_api
}
params = {}
youtube_params = {}

youtube_api_key = youtube_api

class Movie:
    def __init__(self, id, rating, nameRu, nameEn, countries, genres):
        self.id = str(id)
        self.rating = float(rating)
        self.nameRu = nameRu
        self.nameEn = nameEn
        self.countries = countries
        self.genres = genres


def page_amount(response):

        total = response.json()['total']
        if total % 10 == 0:
                pages = total // 10
        else: pages = (total // 10) + 1
        return pages

def parse(movie, data):
    genres = []
    countries = []
    for i in movie['countries']:
        countries.append(i['country'])
    for i in movie['genres']:
        genres.append(i['genre'])
    data['movies'].append(Movie(movie["filmId"], movie["rating"], movie["nameRu"], movie["nameEn"], countries, genres))
    return data['movies']

async def run(data):
    releases_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/releases'
    params['year'] = data['year']
    params['month'] = data['month']
    movie_list = requests.get(releases_url,  headers=headers, params=params)
    for page in range (2, page_amount(movie_list) + 1):
        for movie in movie_list.json()['releases']:
                if movie['rating'] and movie['rating'] >= float(data['rating']):
                    if movie['genres'] and data['genre'] :
                        for i in movie['genres']:
                            if data['genre'] in i['genre']:
                                for i in range(len(movie_list.json())):
                                    data['movies'] = parse(movie, data)
                                    break
                    else:
                        for i in range(len(movie_list.json())):
                            data['movies'] = parse(movie, data)
                            break
        params['page'] = page
        movie_list = requests.get(releases_url, headers=headers, params=params)
    params['page'] = 1
    return data


def get_movie_url_year_name(id):
    film_url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/' + id
    movie_info = requests.get(film_url, headers=headers)
    url = movie_info.json()['webUrl']
    year = movie_info.json()['year']
    name = movie_info.json()['nameRu']
    return url, year, name

async def get_trailer(id):                                                                        # выбрать одну функцию из двух
    youtube_req = 'https://www.googleapis.com/youtube/v3/search'
    notNeeded, year, name = get_movie_url_year_name(id)
    youtube_params['q'] = f'{name} {year} трейлер'
    youtube_params['key'] = youtube_api
    youtube_params['maxResults'] = '1'
    youtube_params['type'] = 'video'
    youtube_params['videoDuration'] = 'short'
    youtube_params['videoEmbeddable'] = 'true'
    trailer_response = requests.get(youtube_req, params=youtube_params)
    trailer_id = trailer_response.json()['items'][0]['id']['videoId']
    video_url = 'https://www.youtube.com/watch?v=' + trailer_id
    return video_url

def get_kp_trailer(mov_id):                                                                     # выбрать одну функцию из двух
    kp_trailer_req = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/' + mov_id + '/videos'
    trailer_response = requests.get(kp_trailer_req, headers=headers)
    url = trailer_response.json()['items'][0]['url']
    return url
