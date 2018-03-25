import os
import zipfile

from bs4 import BeautifulSoup
from requests import get


def get_subtitle(title, year, path=''):
    build_title = title.replace(' ', '%20')
    result = get('https://yts.am/api/v2/list_movies.jsonp?query_term=' + build_title)
    data = result.json()['data']
    movie_details = data['movies']

    slug_data = title.strip().replace(' ', '-').replace('\'', '').replace('.', '').lower() + '-' + year

    for movie in movie_details:
        print(movie)
        if slug_data == movie['slug'] and movie['imdb_code']:
            print(movie['imdb_code'])
            subtitle_result = get('http://www.yifysubtitles.com/movie-imdb/' + movie['imdb_code'])

            raw_html = BeautifulSoup(subtitle_result.content, 'html.parser')
            # print(raw_html)Harry Potter and the Half-Blood Prince
            tr_high_rating = raw_html.find_all('tr', {'class', 'high-rating'})
            for tr in tr_high_rating:
                # print(tr)
                # TODO: handle subtitles with no rating

                # Get the English subtitle with the highest rating
                td = tr.find('td', {'class', 'flag-cell'})
                # print(td)
                span = td.find('span', {'class', 'sub-lang'})
                if span.text == 'English':
                    td = tr.find('td', {'class', 'download-cell'})
                    a = td.find('a', {'class', 'subtitle-download'})
                    print(a['href'])
                    subtitle_link = get('http://www.yifysubtitles.com' + a['href'])

                    subtitle_html = BeautifulSoup(subtitle_link.content, 'html.parser')
                    zip_file_link = subtitle_html.find('a', {'class', 'btn-icon download-subtitle'})
                    print(zip_file_link['href'])


def get_subtitle_with_imdb_code(title, year, path=''):
    build_title = title.replace(' ', '%20')
    result = get('https://yts.am/api/v2/list_movies.jsonp?query_term=' + build_title)
    data = result.json()['data']
    movie_details = data['movies']

    slug_data = title.strip().replace(' ', '-').replace('\'', '').replace('.', '').lower() + '-' + year

    for movie in movie_details:
        # print(movie)
        if slug_data == movie['slug'] and movie['imdb_code']:
            # print(movie['imdb_code'])
            subtitle_result = get('http://www.yifysubtitles.com/movie-imdb/' + movie['imdb_code'])

            raw_html = BeautifulSoup(subtitle_result.content, 'html.parser')
            # print(raw_html)Harry Potter and the Half-Blood Prince
            tr_high_rating = raw_html.find_all('tr', {'class', 'high-rating'})
            for tr in tr_high_rating:
                # print(tr)
                # TODO: handle subtitles with no rating

                # Get the English subtitle with the highest rating
                td = tr.find('td', {'class', 'flag-cell'})
                # print(td)
                span = td.find('span', {'class', 'sub-lang'})
                if span.text == 'English':
                    td = tr.find('td', {'class', 'download-cell'})
                    a = td.find('a', {'class', 'subtitle-download'})
                    # print(a['href'])
                    subtitle_link = get('http://www.yifysubtitles.com' + a['href'])

                    subtitle_html = BeautifulSoup(subtitle_link.content, 'html.parser')
                    zip_file_link = subtitle_html.find('a', {'class', 'btn-icon download-subtitle'})
                    print(zip_file_link['href'])

                    subtitle_url = get(zip_file_link['href'])
                    filename = zip_file_link['href'].split('/')[-1]
                    print(filename)
                    subtitle_zipfile = open(filename, 'wb')
                    subtitle_zipfile.write(subtitle_url.content)
                    subtitle_zipfile.close()

                    unzipfile(filename)


def unzipfile(filename):
    zipref = zipfile.ZipFile(filename, 'r')
    zipref.extractall('.')
    zipref.close()

    os.remove(filename)


if __name__ == '__main__':
    # get_subtitle('Star Wars The Last Jedi', '2017')
    get_subtitle_with_imdb_code('Harry Potter and the Half-Blood Prince', '2009')
