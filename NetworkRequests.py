import requests
import json
import random
import os

headers = {
    "accept": "application/json",
    "Authorization": os.getenv("token_TMDB")
}

def getRandomFilmsArray() -> list:
    random_integers = [random.randint(0, 50) for _ in range(3)]

    movies = []
    for page in random_integers:
        movies = movies + getRandomFilmArray(page)

    return movies

def getRandomFilmArray(page: int) -> list:
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&language=en-US&page={page}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    genres = getGenresNames()


    data = response.json()
    resultsFilms = data.get("results", [])  # Get the "results" from the JSON content

    for film in resultsFilms:
        film['genres'] = []
        filmGenres = film.get("genre_ids")
        for filmGenreId in filmGenres:
            for genre in genres:
                if filmGenreId == genre.get("id"):
                    film['genres'].append(genre)

        film.pop("genre_ids", None)

    return resultsFilms

def getGenresNames():
    url = f"https://api.themoviedb.org/3/genre/movie/list?language=en-US"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        genres = data.get("genres", [])

        return genres

    else:
        return []
