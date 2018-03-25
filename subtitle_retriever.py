from bs4 import BeautifulSoup
from requests import get

FILENAME = 'medium-cover.jpg'


def retrieve_image_from_url(title, year, path):
    build_title = title.replace(' ', '%20')
    result = get('https://yts.am/api/v2/list_movies.jsonp?query_term=' + build_title)
    data = result.json()['data']
    movie_details = data['movies']

    for movie in movie_details:
        if movie['imdb_code']:
            # print(movie['imdb_code'])
            subtitle_result = get('http://www.yifysubtitles.com/movie-imdb/' + movie['imdb_code'])

            raw_html = BeautifulSoup(subtitle_result.content, 'html.parser')
            # print(raw_html)
            tr = raw_html.find('tr', {'class', 'high-rating'})
            # TODO: handle subtitles with no rating

            # Get the English subtitle with the highest rating
            td = tr.find('td', {'class', 'flag-cell'})
            span = td.find('span', {'class', 'sub-lang'})
            if span.text == 'English':
                td = tr.find('td', {'class', 'download-cell'})
                a = td.find('a', {'class', 'subtitle-download'})
                print(a['href'])
                subtitle_link = get('http://www.yifysubtitles.com' + a['href'])

                subtitle_html = BeautifulSoup(subtitle_link.content, 'html.parser')
                zip_file_link = subtitle_html.find('a', {'class', 'btn-icon download-subtitle'})
                print(zip_file_link['href'])


if __name__ == '__main__':
    retrieve_image_from_url('Star Wars The Last Jedi', '2017', '')
