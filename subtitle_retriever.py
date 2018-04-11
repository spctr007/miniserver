import os
import zipfile

from bs4 import BeautifulSoup
from requests import get, ConnectionError


def get_subtitle(title, year, path=''):
    build_title = title.replace(' ', '%20')
    try:

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
                tbody = raw_html.find('tbody')
                tr_high_rating = tbody.find_all('tr', {'class', 'high-rating'})

                # Get the subtitle with no high rating.
                if len(tr_high_rating) == 0:
                    tr_high_rating = tbody.find_all('tr')
                    for tr in tr_high_rating:
                        # Get the English subtitle
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
                            # print(zip_file_link['href'])
                            subtitle_url = get(zip_file_link['href'])
                            filename = zip_file_link['href'].split('/')[-1]
                            print(filename)

                            # Save the zip file in the local drive.
                            subtitle_zip_file = open(filename, 'wb')
                            subtitle_zip_file.write(subtitle_url.content)
                            subtitle_zip_file.close()

                            # unzip the file.
                            unzip_file(filename, path)
                            break
                else: # retrieve subtitle with high rating.
                    for tr in tr_high_rating:
                        # print(tr)
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
                            # print(zip_file_link['href'])
                            subtitle_url = get(zip_file_link['href'])
                            filename = zip_file_link['href'].split('/')[-1]
                            print(filename)

                            # Save the zip file in the local drive.
                            subtitle_zip_file = open(filename, 'wb')
                            subtitle_zip_file.write(subtitle_url.content)
                            subtitle_zip_file.close()

                            # unzip the file.
                            unzip_file(filename, path)
                            break
    except ConnectionError:
        print("No connection. Cannot retrieve subtitle.")


def unzip_file(filename, path='.'):
    zipref = zipfile.ZipFile(filename, 'r')
    zipref.extractall(path)
    zipref.close()

    os.remove(filename)


if __name__ == '__main__':
    get_subtitle('Star Wars The Last Jedi', '2017')
    # get_subtitle_with_imdb_code('')
    get_subtitle('Undercover Grandpa', '2017') #tt3891538
